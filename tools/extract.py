# -*- coding: utf-8 -*-
"""
Extrai a base de dados da wiki a partir da instalacao real do modpack.

Le, nesta ordem de precedencia (o ultimo vence):
  1. os 167 jars em mods/
  2. o datapack do pack em kubejs/data/
  3. defaultconfigs / patchouli_books do pack

Gera em data/:
  names.json      id -> display name (en_us)
  recipes.json    lista normalizada de receitas
  tags.json       tag -> membros expandidos
  icons/          atlas.png + atlas.json (posicoes)
  agricraft.json  plantas, mutacoes, solos
  bees.json       especies, mutacoes, combs, flowers
  rituals.json    livro proprio + circle magic
  books.json      paginas de guidebook indexadas
  overlay.json    operacoes KubeJS que alteram receitas
  mods.json       metadados dos mods
"""
import os, io, re, json, zipfile, collections, sys

INST = r"C:\Users\PC\curseforge\minecraft\Instances\Reclamation - Reclaim the World"
MODS = os.path.join(INST, "mods")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "data"))

os.makedirs(OUT, exist_ok=True)


def log(*a):
    print(*a, flush=True)


def jload(raw):
    """Tolerante a BOM e comentarios estilo // que alguns mods deixam."""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig", "replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^\s*//.*$", "", raw, flags=re.M)
        return json.loads(cleaned)


def write(name, obj):
    p = os.path.join(OUT, name)
    with io.open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    log(f"  -> {name}  ({os.path.getsize(p)/1024:.0f} KB)")


# ---------------------------------------------------------------- jars

VANILLA = r"C:\Users\PC\curseforge\minecraft\Install\versions\1.20.1\1.20.1.jar"


def jar_list():
    mods = [os.path.join(MODS, f) for f in sorted(os.listdir(MODS)) if f.endswith(".jar")]
    # o jar vanilla vem primeiro: e a base que os mods sobrepoem
    return ([VANILLA] if os.path.exists(VANILLA) else []) + mods


JARS = jar_list()
log(f"jars: {len(JARS)} (vanilla: {'sim' if os.path.exists(VANILLA) else 'NAO ENCONTRADO'})")


# ---------------------------------------------------------------- nomes

LANG_ID = re.compile(r"^(item|block|fluid|entity)\.([a-z0-9_]+)\.(.+)$")

# registries que nao sao item/block mas aparecem em receitas (fluidos, gases,
# pigmentos) ou dao nome a conteudo da wiki (especies de abelha, rituais, crops)
AUX_LANG = re.compile(
    r"^(fluid_type|gas|slurry|infuse_type|pigment|chemical|species|ritual|crop)"
    r"\.([a-z0-9_]+)\.([a-z0-9_/.]+)$")
AUX_LABEL = {
    "fluid_type": "fluido", "gas": "gas", "slurry": "slurry",
    "infuse_type": "infusao", "pigment": "pigmento", "chemical": "quimico",
    "species": "especie", "ritual": "ritual", "crop": "cultivo",
}


def extract_names():
    names, entity, misc, aux = {}, {}, {}, {}
    for jp in JARS:
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                if not (n.startswith("assets/") and n.endswith("/lang/en_us.json")):
                    continue
                try:
                    d = jload(z.read(n))
                except Exception:
                    continue
                for k, v in d.items():
                    if not isinstance(v, str):
                        continue
                    # nomes-template ("Alchemical Sulfur %s"): tenta a chave
                    # irma .source, senao descarta e deixa o fallback derivar
                    if "%" in v:
                        sub = d.get(k + ".source")
                        if isinstance(sub, str) and "%" not in sub:
                            v = re.sub(r"%(?:\d+\$)?s", sub, v).strip()
                        else:
                            continue
                    m = LANG_ID.match(k)
                    if not m:
                        a = AUX_LANG.match(k)
                        if a and "." not in a.group(3):
                            akind, ans, apath = a.groups()
                            aux.setdefault(f"{ans}:{apath}",
                                           {"n": v, "k": AUX_LABEL[akind]})
                        else:
                            misc[k] = v
                        continue
                    kind, ns, path = m.groups()
                    ident = f"{ns}:{path.replace('.', '/')}"
                    if kind == "entity":
                        entity[ident] = v
                    else:
                        # block e item colidem de proposito: mesmo nome
                        names.setdefault(ident, v)
    return names, entity, misc, aux


# ---------------------------------------------------------------- tags

def extract_tags():
    raw = collections.defaultdict(lambda: {"values": [], "replace": False})

    def absorb(kind, ns, path, d):
        key = f"{kind}:{ns}:{path}"
        if d.get("replace"):
            raw[key]["values"] = []
            raw[key]["replace"] = True
        for v in d.get("values", []):
            if isinstance(v, dict):
                v = v.get("id")
            if v:
                raw[key]["values"].append(v)

    pat = re.compile(r"^data/([a-z0-9_.-]+)/tags/([a-z_]+)/(.+)\.json$")
    for jp in JARS:
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                m = pat.match(n)
                if not m:
                    continue
                ns, kind, path = m.groups()
                kind = kind.rstrip("s")
                if kind not in ("item", "block", "fluid", "entity_type"):
                    continue
                try:
                    absorb(kind, ns, path, jload(z.read(n)))
                except Exception:
                    pass

    # datapack do pack sobrepoe
    dp = os.path.join(INST, "kubejs", "data")
    for root, _, files in os.walk(dp):
        for f in files:
            if not f.endswith(".json"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, dp).replace("\\", "/")
            m = re.match(r"^([a-z0-9_.-]+)/tags/([a-z_]+)/(.+)\.json$", rel)
            if not m:
                continue
            ns, kind, path = m.groups()
            kind = kind.rstrip("s")
            if kind not in ("item", "block", "fluid", "entity_type"):
                continue
            try:
                absorb(kind, ns, path, jload(io.open(full, "rb").read()))
            except Exception:
                pass

    # expande referencias #tag
    resolved = {}

    def resolve(key, seen=None):
        if key in resolved:
            return resolved[key]
        seen = seen or set()
        if key in seen:
            return []
        seen.add(key)
        out = []
        kind = key.split(":", 1)[0]
        for v in raw.get(key, {}).get("values", []):
            if v.startswith("#"):
                out.extend(resolve(f"{kind}:{v[1:]}", seen))
            else:
                out.append(v)
        out = sorted(set(out))
        resolved[key] = out
        return out

    for k in list(raw):
        resolve(k)

    # os jars trazem tags citando itens de mods ausentes (ilikewood, byg...):
    # sem podar, um chip "qualquer X" mostraria contagem e icone irreais
    try:
        known = set(json.load(io.open(os.path.join(OUT, "names.json"),
                                      encoding="utf-8")))
        for k, v in resolved.items():
            resolved[k] = [x for x in v if x in known]
    except Exception:
        pass

    # chave publica sem o prefixo de tipo, item tem prioridade
    flat = {}
    for k, v in resolved.items():
        kind, rest = k.split(":", 1)
        if kind == "item" or rest not in flat:
            flat[rest] = v
    return flat


# ---------------------------------------------------------------- receitas

RESULT_KEYS = ("result", "output", "results", "outputs", "output_item",
               "resultItem", "primary_output", "main_output",
               "mainOutput", "secondaryOutput", "fluidOutput", "gasOutput",
               "chanceResult", "drops", "outputItem", "resultItems")
IGNORE_KEYS = {"type", "conditions", "category", "group", "show_notification",
               "cookingtime", "experience", "energy", "processingTime",
               "duration", "time", "mana", "cost", "level", "tier",
               "bookshelf:load_conditions", "fabric:load_conditions",
               "sourceCost", "color", "sound", "weight"}

# receitas cujo resultado nao e um item: guardamos o que elas produzem de fato
SPECIAL_OUT = (
    ("enchantment", "ench"),
    ("entity", "entity"),
    ("brew", "brew"),
    ("effect", "effect"),
    ("tome_type", "item"),
)


# ---- condicoes: o pack so tem 169 mods, mas os jars trazem receitas de
# compatibilidade para mods ausentes (ilikewood, byg, biomesoplenty...).
# Sem avaliar as condicoes, a wiki mostraria milhares de receitas fantasma.

_MODIDS = None


def installed_modids():
    global _MODIDS
    if _MODIDS is not None:
        return _MODIDS
    ids = {"minecraft", "forge", "kubejs", "c"}
    for jp in JARS:
        try:
            with zipfile.ZipFile(jp) as z:
                if "META-INF/mods.toml" in z.namelist():
                    toml = z.read("META-INF/mods.toml").decode("utf-8", "replace")
                    ids.update(re.findall(r'modId\s*=\s*"([^"]+)"', toml))
        except Exception:
            pass
    _MODIDS = ids
    return ids


def eval_condition(c, known_items=None):
    """True = a receita vale neste pack. Desconhecido -> True (nao remove)."""
    if not isinstance(c, dict):
        return True
    t = c.get("type", "")
    if t.endswith("mod_loaded"):
        return c.get("modid") in installed_modids()
    if t.endswith(":not"):
        return not eval_condition(c.get("value"), known_items)
    if t.endswith(":and"):
        return all(eval_condition(x, known_items) for x in c.get("values", []))
    if t.endswith(":or"):
        return any(eval_condition(x, known_items) for x in c.get("values", []))
    if t.endswith("item_exists"):
        if known_items is None:
            return True
        vals = c.get("values") or ([c["item"]] if isinstance(c.get("item"), str) else [])
        return all(v in known_items for v in vals)
    if t.endswith("false"):
        return False
    if t.endswith("true"):
        return True
    return True


def conditions_pass(d, known_items=None):
    for key in ("conditions", "bookshelf:load_conditions"):
        conds = d.get(key)
        if isinstance(conds, list) and not all(
                eval_condition(c, known_items) for c in conds):
            return False
    return True


def refs_in(node, out):
    """Coleta recursivamente qualquer {'item':..} / {'tag':..} / string de id."""
    if isinstance(node, dict):
        if "item" in node and isinstance(node["item"], str):
            out.append(("item", node["item"], node.get("count", node.get("amount", 1))))
            return
        if "tag" in node and isinstance(node["tag"], str):
            out.append(("tag", node["tag"], node.get("count", node.get("amount", 1))))
            return
        if "id" in node and isinstance(node["id"], str) and ":" in node["id"] \
           and "type" not in node:
            out.append(("item", node["id"], node.get("count", node.get("amount", 1))))
            return
        for k, v in node.items():
            if k in IGNORE_KEYS:
                continue
            refs_in(v, out)
    elif isinstance(node, list):
        for v in node:
            refs_in(v, out)
    elif isinstance(node, str):
        if re.fullmatch(r"[a-z0-9_.-]+:[a-z0-9_./-]+", node):
            out.append(("item", node, 1))


KNOWN_ITEMS = None


def norm_recipe(rid, d, source):
    if not isinstance(d, dict):
        return []
    if not conditions_pass(d, KNOWN_ITEMS):
        return []
    rtype = d.get("type")

    # forge:conditional embrulha receitas reais
    if rtype == "forge:conditional":
        out = []
        for i, sub in enumerate(d.get("recipes", [])):
            inner = sub.get("recipe")
            if not inner:
                continue
            conds = sub.get("conditions")
            if isinstance(conds, list) and not all(
                    eval_condition(c, KNOWN_ITEMS) for c in conds):
                continue
            out.extend(norm_recipe(f"{rid}#{i}", inner, source))
        return out
    if not rtype:
        return []
    # tipo sem namespace e valido no MC e assume minecraft:
    if ":" not in rtype:
        rtype = "minecraft:" + rtype

    results, ing = [], []
    for k in RESULT_KEYS:
        if k in d:
            refs_in(d[k], results)
    rest = {k: v for k, v in d.items() if k not in RESULT_KEYS}
    refs_in(rest, ing)

    def dedup(seq):
        seen, out = set(), []
        for kind, ident, cnt in seq:
            key = (kind, ident)
            if key in seen:
                continue
            seen.add(key)
            out.append({"k": kind[0], "id": ident, "n": cnt if isinstance(cnt, int) else 1})
        return out

    rec = {
        "id": rid,
        "t": rtype,
        "in": dedup(ing),
        "out": dedup(results),
        "src": source,
    }

    # resultado nao-item (encantamento, entidade, brew...)
    if not rec["out"]:
        for key, kind in SPECIAL_OUT:
            v = d.get(key)
            if isinstance(v, str):
                rec["outk"] = kind
                rec["outv"] = v
                break
            if isinstance(v, dict) and isinstance(v.get("type"), str):
                rec["outk"] = kind
                rec["outv"] = v["type"]
                break

    return [rec]


def extract_recipes():
    recipes = []
    pat = re.compile(r"^data/([a-z0-9_.-]+)/recipes?/(.+)\.json$")
    for jp in JARS:
        modfile = os.path.basename(jp)
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                m = pat.match(n)
                if not m:
                    continue
                ns, path = m.groups()
                try:
                    d = jload(z.read(n))
                except Exception:
                    continue
                recipes.extend(norm_recipe(f"{ns}:{path}", d, modfile))
    return recipes


# ------------------------------------------------- receitas do pack (KubeJS)
#
# Os scripts do pack geram receitas dentro de loops e funcoes auxiliares
# parametrizadas, entao ler o codigo com regex perde parte delas. Em vez disso
# executamos os scripts com um KubeJS falso (tools/dump_kubejs.mjs) e lemos as
# chamadas ja resolvidas.

COUNT_PREFIX = re.compile(r"^\s*(\d+)\s*x\s+(.+?)\s*$")

SCRIPTS = os.path.join(INST, "kubejs", "server_scripts")
DUMP = os.path.join(OUT, "kubejs_calls.json")


def run_node_dump():
    import subprocess
    mjs = os.path.join(HERE, "dump_kubejs.mjs")
    r = subprocess.run(["node", mjs, SCRIPTS], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"node falhou: {r.stderr[:400]}")
    with io.open(DUMP, "w", encoding="utf-8") as f:
        f.write(r.stdout)
    return json.loads(r.stdout)


def parse_stack(v):
    """'4x mod:item' | 'mod:item' | '#tag' | {item:..} -> (kind, id, count)"""
    if isinstance(v, dict):
        if isinstance(v.get("item"), str):
            return ("item", v["item"], v.get("count", 1))
        if isinstance(v.get("tag"), str):
            return ("tag", v["tag"], v.get("count", 1))
        # Item.of('id', '{nbt}') vindo do stub do Node
        raw = v.get("__item")
        if isinstance(raw, list) and raw and isinstance(raw[0], str):
            first = raw[0]
            n = 1
            if len(raw) > 1 and isinstance(raw[1], int):
                n = raw[1]
            m = COUNT_PREFIX.match(first)
            if m:
                n, first = int(m.group(1)), m.group(2)
            if ":" in first:
                return ("item", first, n)
        return None
    if not isinstance(v, str):
        return None
    n = 1
    m = COUNT_PREFIX.match(v)
    if m:
        n, v = int(m.group(1)), m.group(2)
    v = v.strip()
    if v.startswith("#"):
        return ("tag", v[1:], n)
    if ":" in v:
        return ("item", v, n)
    return None


def extract_pack_recipes():
    """Devolve (receitas_adicionadas, remocoes, falhas) a partir do dump do Node."""
    data = run_node_dump()
    if data.get("errors"):
        log(f"   ATENCAO: {len(data['errors'])} script(s) com erro de execucao")
        for e in data["errors"]:
            log(f"     {e['file']}: {e['error'][:120]}")

    added, removals, fails = [], [], []
    for idx, c in enumerate(data["calls"]):
        if not c["event"].startswith("recipes"):
            continue
        op, args = c["op"], c.get("args") or []
        where = c["file"]
        rid = c.get("rid")

        if op == "remove":
            removals.append({"where": where, "filter": args[0] if args else None})
            continue
        if op in ("replaceInput", "replaceOutput"):
            removals.append({"where": where, "op": op,
                             "filter": args[0] if args else None,
                             "from": args[1] if len(args) > 1 else None,
                             "to": args[2] if len(args) > 2 else None})
            continue

        if op == "custom":
            if not args or not isinstance(args[0], dict):
                fails.append({"where": where, "op": op, "err": "argumento nao e objeto"})
                continue
            for x in norm_recipe(rid or f"pack:{where}#{idx}", args[0], "kubejs"):
                x["pack"] = 1
                x["where"] = where
                added.append(x)
            continue

        if op in ("shaped", "shapeless"):
            if not args:
                continue
            res = parse_stack(args[0])
            if not res:
                fails.append({"where": where, "op": op, "err": "resultado ilegivel",
                              "snippet": str(args[0])[:120]})
                continue
            ings = []
            if op == "shaped" and len(args) >= 3 and isinstance(args[2], dict):
                for v in args[2].values():
                    s = parse_stack(v)
                    if s:
                        ings.append(s)
            elif op == "shapeless" and len(args) >= 2 and isinstance(args[1], list):
                for v in args[1]:
                    s = parse_stack(v)
                    if s:
                        ings.append(s)
            seen, ilist = set(), []
            for kind, ident, cnt in ings:
                if (kind, ident) in seen:
                    continue
                seen.add((kind, ident))
                ilist.append({"k": kind[0], "id": ident,
                              "n": cnt if isinstance(cnt, int) else 1})
            added.append({
                "id": rid or f"pack:{where}#{idx}",
                "t": f"minecraft:crafting_{op}",
                "in": ilist,
                "out": [{"k": "i", "id": res[1], "n": res[2]}],
                "src": "kubejs", "pack": 1, "where": where,
                "pattern": args[1] if op == "shaped" and len(args) > 1 else None,
            })
    return added, removals, fails


def apply_removals(recipes, removals):
    """Marca como removidas as receitas que o pack apaga."""
    by_id = {}
    by_out = collections.defaultdict(list)
    for i, r in enumerate(recipes):
        by_id.setdefault(r["id"], []).append(i)
        for o in r["out"]:
            if o["k"] == "i":
                by_out[o["id"]].append(i)

    by_type = collections.defaultdict(list)
    by_in = collections.defaultdict(list)
    for i, r in enumerate(recipes):
        by_type[r["t"]].append(i)
        for e in r["in"]:
            by_in[e["id"]].append(i)

    removed = set()
    unmatched = []
    for rm in removals:
        if rm.get("op"):           # replaceInput/Output nao remove
            continue
        f = rm.get("filter")
        if isinstance(f, str):     # string solta = id da receita ou item de saida
            f = {"id": f} if "/" in f else {"output": f}
        if not isinstance(f, dict):
            unmatched.append(rm)
            continue
        hit = False
        if isinstance(f.get("id"), str):
            for i in by_id.get(f["id"], []):
                removed.add(i)
                hit = True
        if isinstance(f.get("output"), str):
            for i in by_out.get(f["output"].lstrip("#"), []):
                removed.add(i)
                hit = True
        if isinstance(f.get("type"), str):
            for i in by_type.get(f["type"], []):
                removed.add(i)
                hit = True
        if isinstance(f.get("input"), str):
            for i in by_in.get(f["input"].lstrip("#"), []):
                removed.add(i)
                hit = True
        if not hit:
            unmatched.append(rm)

    for i in removed:
        recipes[i]["removed"] = 1
    return len(removed), unmatched


# ---------------------------------------------------------------- icones

def extract_icons():
    """Atlas resolvido pelos modelos (ver tools/icons.py)."""
    import icons as icons_mod
    names = jload_out("names.json")
    recipes = jload_out("recipes.json")
    tags = jload_out("tags.json")

    # tudo que pode aparecer na tela: nomes conhecidos + ids citados em
    # receitas + membros de tag (o chip de tag mostra o icone do 1o membro)
    ids = set(names)
    for r in recipes:
        for side in ("in", "out"):
            for x in r.get(side, []):
                if x["k"] == "i":
                    ids.add(x["id"])
                else:
                    ids.update(tags.get(x["id"], [])[:3])
        if r.get("outv"):
            ids.add(r["outv"])

    pos, st = icons_mod.build(JARS, sorted(ids), os.path.join(OUT, "icons"))
    return st


def jload_out(name):
    return json.load(io.open(os.path.join(OUT, name), encoding="utf-8"))


# ---------------------------------------------------------------- agricraft

def read_pack_json(subpath):
    """Le arquivos do datapack do pack, retornando {ns: {nome: dados}}."""
    base = os.path.join(INST, "kubejs", "data")
    out = {}
    for root, _, files in os.walk(base):
        rel = os.path.relpath(root, base).replace("\\", "/")
        if subpath not in rel:
            continue
        ns = rel.split("/")[0]
        for f in files:
            if not f.endswith(".json"):
                continue
            try:
                out[f"{ns}:{f[:-5]}"] = jload(io.open(os.path.join(root, f), "rb").read())
            except Exception:
                pass
    return out


def extract_agricraft():
    plants = read_pack_json("agricraft/plants")
    mutations = read_pack_json("agricraft/mutations")
    soils = read_pack_json("agricraft/soils")
    # tambem dentro dos jars (agricraft base)
    pat = re.compile(r"^data/([a-z0-9_.-]+)/agricraft/(plants|mutations|soils)/(.+)\.json$")
    jar_p, jar_m, jar_s = {}, {}, {}
    for jp in JARS:
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                m = pat.match(n)
                if not m:
                    continue
                ns, kind, path = m.groups()
                try:
                    d = jload(z.read(n))
                except Exception:
                    continue
                {"plants": jar_p, "mutations": jar_m, "soils": jar_s}[kind][f"{ns}:{path}"] = d
    jar_p.update(plants)
    jar_m.update(mutations)
    jar_s.update(soils)
    return {"plants": jar_p, "mutations": jar_m, "soils": jar_s}


# ---------------------------------------------------------------- abelhas

def extract_bees():
    out = {"species": {}, "mutations": {}, "combs": {}, "flowers": {}}
    keymap = {"species": "species", "mutation": "mutations",
              "comb": "combs", "flower": "flowers"}
    base = os.path.join(INST, "kubejs", "data")
    for root, _, files in os.walk(base):
        rel = os.path.relpath(root, base).replace("\\", "/")
        if "complicated_bees/" not in rel:
            continue
        seg = rel.split("complicated_bees/")[-1].split("/")[0]
        bucket = keymap.get(seg)
        if not bucket:
            continue
        for f in files:
            if not f.endswith(".json"):
                continue
            try:
                out[bucket][f[:-5]] = jload(io.open(os.path.join(root, f), "rb").read())
            except Exception:
                pass
    pat = re.compile(r"^data/([a-z0-9_.-]+)/complicated_bees/([a-z_]+)(?:/[a-z_]+)?/(.+)\.json$")
    for jp in JARS:
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                m = pat.match(n)
                if not m:
                    continue
                _, seg, path = m.groups()
                bucket = keymap.get(seg)
                if not bucket or path in out[bucket]:
                    continue
                try:
                    out[bucket][path] = jload(z.read(n))
                except Exception:
                    pass
    return out


# ---------------------------------------------------------------- rituais

def extract_rituals():
    out = {"pack_book": {}, "circle_magic": {}, "tree_ritual": {}}
    # livro proprio do pack
    pb = os.path.join(INST, "patchouli_books")
    for root, _, files in os.walk(pb):
        for f in files:
            if not f.endswith(".json"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, pb).replace("\\", "/")
            try:
                out["pack_book"][rel] = jload(io.open(full, "rb").read())
            except Exception:
                pass
    # circle magic do datapack
    base = os.path.join(INST, "kubejs", "data")
    for root, _, files in os.walk(base):
        rel = os.path.relpath(root, base).replace("\\", "/")
        if "circle_magic" not in rel:
            continue
        for f in files:
            if not f.endswith(".json"):
                continue
            try:
                out["circle_magic"][f"{rel}/{f[:-5]}"] = jload(
                    io.open(os.path.join(root, f), "rb").read())
            except Exception:
                pass
    return out


# ---------------------------------------------------------------- livros

def extract_books():
    books = {}
    pat = re.compile(r"^(?:data|assets)/([a-z0-9_.-]+)/(patchouli_books|modonomicon)/([^/]+)/(.+)\.json$")
    for jp in JARS:
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                m = pat.match(n)
                if not m:
                    continue
                ns, system, book, path = m.groups()
                if "/en_us/" not in n and "/en_us." not in n and system == "patchouli_books":
                    if "/entries/" in n or "/categories/" in n:
                        continue
                try:
                    d = jload(z.read(n))
                except Exception:
                    continue
                books.setdefault(f"{ns}:{book}", {})[path] = d
    return books


# ---------------------------------------------------------------- overlay

OVERLAY_RE = re.compile(
    r"event\.(remove|shaped|shapeless|custom|replaceInput|replaceOutput)\s*\(", re.S)


def extract_overlay():
    d = os.path.join(INST, "kubejs", "server_scripts")
    ops = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".js"):
            continue
        src = io.open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        lines = src.split("\n")
        for i, line in enumerate(lines):
            m = OVERLAY_RE.search(line)
            if not m:
                continue
            # captura o bloco ate fechar parenteses
            depth, buf, j = 0, [], i
            while j < len(lines) and j < i + 60:
                buf.append(lines[j])
                depth += lines[j].count("(") - lines[j].count(")")
                if j > i and depth <= 0:
                    break
                j += 1
            ops.append({"file": f, "line": i + 1, "op": m.group(1),
                        "code": "\n".join(buf).strip()[:1400]})
    return ops


# ---------------------------------------------------------------- mods

def extract_mods():
    out = []
    for jp in JARS:
        info = {"jar": os.path.basename(jp)}
        try:
            with zipfile.ZipFile(jp) as z:
                if "META-INF/mods.toml" in z.namelist():
                    toml = z.read("META-INF/mods.toml").decode("utf-8", "replace")
                    mid = re.search(r'modId\s*=\s*"([^"]+)"', toml)
                    nm = re.search(r'displayName\s*=\s*"([^"]+)"', toml)
                    ver = re.search(r'version\s*=\s*"([^"]+)"', toml)
                    desc = re.search(r"description\s*=\s*'''(.*?)'''", toml, re.S)
                    info["id"] = mid.group(1) if mid else None
                    info["name"] = nm.group(1) if nm else None
                    info["version"] = ver.group(1) if ver else None
                    if desc:
                        info["desc"] = " ".join(desc.group(1).split())[:400]
        except Exception:
            pass
        out.append(info)
    return out


# ---------------------------------------------------------------- main

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else "all"

    if only in ("all", "names"):
        log("nomes...")
        names, entity, misc, aux = extract_names()
        write("names.json", names)
        write("entities.json", entity)
        write("aux_names.json", aux)
        log(f"   {len(names):,} itens/blocos, {len(entity):,} entidades, "
            f"{len(aux):,} fluidos/gases/especies/rituais")

    if only in ("all", "tags"):
        log("tags...")
        tags = extract_tags()
        write("tags.json", tags)
        log(f"   {len(tags):,} tags")

    if only in ("all", "recipes"):
        log("receitas...")
        try:
            KNOWN_ITEMS = set(json.load(io.open(
                os.path.join(OUT, "names.json"), encoding="utf-8")))
            globals()["KNOWN_ITEMS"] = KNOWN_ITEMS
        except Exception:
            log("   (names.json ausente: rode 'names' antes para filtrar melhor)")
        log(f"   mods instalados: {len(installed_modids())}")
        rec = extract_recipes()
        log(f"   {len(rec):,} dos jars")
        added, removals, fails = extract_pack_recipes()
        log(f"   {len(added):,} adicionadas pelo pack, {len(removals)} remocoes/replaces, "
            f"{len(fails)} nao parseadas")
        rec.extend(added)
        nrem, unmatched = apply_removals(rec, removals)
        log(f"   {nrem:,} marcadas como removidas pelo pack "
            f"({len(unmatched)} filtros sem correspondencia)")
        write("recipes.json", rec)
        write("pack_changes.json", {"removals": removals, "fails": fails,
                                    "unmatched": unmatched})
        types = collections.Counter(r["t"] for r in rec)
        log(f"   TOTAL {len(rec):,} receitas, {len(types)} tipos")

    if only in ("all", "icons"):
        log("icones...")
        st = extract_icons()
        log(f"   {st['resolvidos']:,}/{st['pedidos']:,} ids com icone "
            f"({100*st['resolvidos']/max(1,st['pedidos']):.0f}%), "
            f"{st['sprites_unicos']:,} sprites unicos, "
            f"atlas {st['tamanho'][0]}x{st['tamanho'][1]}")
        if st["exemplos_sem"]:
            log(f"   sem icone (exemplos): {', '.join(st['exemplos_sem'][:5])}")

    if only in ("all", "agricraft"):
        log("agricraft...")
        ag = extract_agricraft()
        write("agricraft.json", ag)
        log(f"   {len(ag['plants'])} plantas, {len(ag['mutations'])} mutacoes, {len(ag['soils'])} solos")

    if only in ("all", "bees"):
        log("abelhas...")
        b = extract_bees()
        write("bees.json", b)
        log(f"   {len(b['species'])} especies, {len(b['mutations'])} mutacoes, "
            f"{len(b['combs'])} combs, {len(b['flowers'])} flores")

    if only in ("all", "rituals"):
        log("rituais...")
        r = extract_rituals()
        write("rituals.json", r)
        log(f"   {len(r['pack_book'])} arquivos do livro do pack, {len(r['circle_magic'])} rites")

    if only in ("all", "books"):
        log("guidebooks...")
        bk = extract_books()
        write("books.json", bk)
        log(f"   {len(bk)} livros, {sum(len(v) for v in bk.values()):,} paginas")

    if only in ("all", "overlay"):
        log("overlay kubejs...")
        ov = extract_overlay()
        write("overlay.json", ov)
        log(f"   {len(ov)} operacoes")

    if only in ("all", "mods"):
        log("mods...")
        m = extract_mods()
        write("mods.json", m)
        log(f"   {len(m)} mods")

    log("ok")
