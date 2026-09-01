# -*- coding: utf-8 -*-
"""
Resolve o icone de cada item/bloco do jeito que o jogo faz: pelo MODELO.

Indexar apenas `textures/item/<id>.png` cobria so 19% dos ids, porque:
  - blocos nao tem textura de item (o icone e o modelo 3D renderizado)
  - muitos itens apontam para uma textura com nome diferente do id

Aqui seguimos a cadeia de `parent` do modelo, juntamos o dicionario de
`textures`, resolvemos as indirecoes `#chave` e escolhemos a face mais
representativa.
"""
import io, os, re, json, zipfile, collections

TEX = re.compile(r"^assets/([a-z0-9_.-]+)/textures/(.+)\.png$")
MDL = re.compile(r"^assets/([a-z0-9_.-]+)/models/(.+)\.json$")

# ordem de preferencia da face: o que melhor representa o item numa lista
FACE_ORDER = ("layer0", "layer1", "all", "texture", "side", "front",
              "north", "top", "end", "cross", "fan", "particle",
              "0", "1", "bottom", "up", "down")

MAX_PARENT_DEPTH = 12


def index_jars(jars):
    """tex[ns:path] -> (jar, entry) ; mdl[ns:path] -> json"""
    tex, mdl = {}, {}
    for jp in jars:
        with zipfile.ZipFile(jp) as z:
            for n in z.namelist():
                m = TEX.match(n)
                if m:
                    key = f"{m.group(1)}:{m.group(2)}"
                    tex.setdefault(key, (jp, n))
                    continue
                m = MDL.match(n)
                if m:
                    key = f"{m.group(1)}:{m.group(2)}"
                    if key in mdl:
                        continue
                    try:
                        mdl[key] = json.loads(z.read(n).decode("utf-8-sig"))
                    except Exception:
                        pass
    return tex, mdl


def _norm(ref, default_ns="minecraft"):
    ref = str(ref)
    return ref if ":" in ref else f"{default_ns}:{ref}"


def collect_textures(model_key, mdl, depth=0, seen=None):
    """Junta o dict `textures` subindo a cadeia de parent (filho tem prioridade)."""
    seen = seen or set()
    if depth > MAX_PARENT_DEPTH or model_key in seen or model_key not in mdl:
        return {}
    seen.add(model_key)
    d = mdl[model_key]
    out = {}
    parent = d.get("parent")
    if isinstance(parent, str):
        out.update(collect_textures(_norm(parent), mdl, depth + 1, seen))
    t = d.get("textures")
    if isinstance(t, dict):
        out.update({k: v for k, v in t.items() if isinstance(v, str)})
    return out


def pick_texture(textures):
    """Escolhe a face mais representativa e resolve indirecao #chave."""
    if not textures:
        return None

    def deref(val, hops=0):
        while isinstance(val, str) and val.startswith("#") and hops < 8:
            val = textures.get(val[1:])
            hops += 1
        return val if isinstance(val, str) and not val.startswith("#") else None

    for k in FACE_ORDER:
        if k in textures:
            v = deref(textures[k])
            if v:
                return v
    for v in textures.values():
        v = deref(v)
        if v:
            return v
    return None


# alguns itens usam `parent: minecraft:builtin/entity`, ou seja, o icone e
# composto em runtime e nao existe como PNG. Para os grupos grandes damos uma
# textura generica: melhor um icone aproximado do que uma caixa vazia.
FALLBACK_PREFIX = (
    ("theurgy:alchemical_sulfur_", "theurgy:item/empty_jar_labeled"),
    ("theurgy:alchemical_salt_", "theurgy:item/alchemical_salt"),
    ("theurgy:alchemical_niter_", "theurgy:item/empty_ceramic_jar_labeled"),
)


def resolve(ident, tex, mdl):
    """id de item/bloco -> chave de textura, ou None."""
    ns, _, path = ident.partition(":")
    if not path:
        return None

    # 1) modelo de item (cobre itens planos e itens-de-bloco via parent)
    for mk in (f"{ns}:item/{path}", f"{ns}:block/{path}"):
        t = pick_texture(collect_textures(mk, mdl))
        if t:
            key = _norm(t, ns)
            nsp, _, p = key.partition(":")
            if f"{nsp}:{p}" in tex:
                return f"{nsp}:{p}"

    # 2) caminho direto, item e depois bloco
    for cand in (f"{ns}:item/{path}", f"{ns}:block/{path}"):
        if cand in tex:
            return cand

    # 3) generico por prefixo (icones compostos em runtime)
    for pref, fb in FALLBACK_PREFIX:
        if ident.startswith(pref) and fb in tex:
            return fb
    return None


def build(jars, ids, out_dir, cell=16, cols=96):
    """Monta o atlas para `ids`. Retorna (mapa de posicoes, stats).

    cell=16 porque as texturas do Minecraft sao 16x16: renderizar maior so
    inflaria o PNG. O CSS reescala com image-rendering:pixelated.
    """
    from PIL import Image

    tex, mdl = index_jars(jars)
    resolved, unresolved = {}, []
    for ident in ids:
        k = resolve(ident, tex, mdl)
        if k:
            resolved[ident] = k
        else:
            unresolved.append(ident)

    # varias ids compartilham a mesma textura: desenha uma vez so
    uniq = sorted(set(resolved.values()))
    slot = {k: i for i, k in enumerate(uniq)}
    rows = (len(uniq) + cols - 1) // cols
    atlas = Image.new("RGBA", (cols * cell, rows * cell), (0, 0, 0, 0))

    zips, drawn = {}, 0
    for k, i in slot.items():
        jp, entry = tex[k]
        if jp not in zips:
            zips[jp] = zipfile.ZipFile(jp)
        try:
            im = Image.open(io.BytesIO(zips[jp].read(entry))).convert("RGBA")
        except Exception:
            continue
        # texturas animadas empilham frames verticalmente: usa o primeiro
        if im.height > im.width and im.height % im.width == 0:
            im = im.crop((0, 0, im.width, im.width))
        if im.size != (cell, cell):
            im = im.resize((cell, cell), Image.NEAREST)
        atlas.paste(im, ((i % cols) * cell, (i // cols) * cell))
        drawn += 1
    for z in zips.values():
        z.close()

    pos = {ident: [slot[k] % cols, slot[k] // cols] for ident, k in resolved.items()}

    os.makedirs(out_dir, exist_ok=True)
    atlas.save(os.path.join(out_dir, "atlas.png"), optimize=True)
    with io.open(os.path.join(out_dir, "atlas.json"), "w", encoding="utf-8") as f:
        json.dump({"cell": cell, "cols": cols, "rows": rows, "pos": pos},
                  f, ensure_ascii=False, separators=(",", ":"))

    return pos, {
        "pedidos": len(ids),
        "resolvidos": len(resolved),
        "sprites_unicos": len(uniq),
        "desenhados": drawn,
        "sem_icone": len(unresolved),
        "tamanho": (cols * cell, rows * cell),
        "exemplos_sem": unresolved[:10],
    }
