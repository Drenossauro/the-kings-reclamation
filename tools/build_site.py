# -*- coding: utf-8 -*-
"""Gera o site estatico da wiki a partir de data/."""
import os, io, re, json, shutil, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")

import theme

FONTS = ("https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600"
         "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400"
         "&family=JetBrains+Mono:wght@400;600&display=swap")

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'"
           "%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%B1%3C/text%3E%3C/svg%3E")

NAV = [
    ("index.html", "Início"),
    ("guia.html", "Guia"),
    ("itens.html", "Itens"),
    ("plantas.html", "Plantas"),
    ("abelhas.html", "Abelhas"),
    ("rituais.html", "Rituais"),
    ("alteracoes.html", "Alterações"),
    ("mods.html", "Mods"),
    ("livros.html", "Livros"),
]


def jload(p):
    return json.load(io.open(os.path.join(DATA, p), encoding="utf-8"))


def e(s):
    return html.escape(str(s), quote=True)


def nav_html(active):
    links = "".join(
        f'<a href="{href}"{" class=\"on\"" if href == active else ""}>{e(label)}</a>'
        for href, label in NAV)
    return (
        '<header class="gnav"><div class="gnav-in">'
        '<a class="brand" href="index.html">The Kings <span>Reclamation</span></a>'
        f'<nav>{links}</nav></div></header>')


FOOT = (
    '<p class="foot">Wiki gerada a partir da instalação local — Reclamation 2.3.2 · '
    'Minecraft 1.20.1 · Forge 47.4.0.<br>'
    'Dados extraídos dos 169 jars, do datapack do pack e dos scripts KubeJS executados.<br>'
    'Se o modpack for atualizado, receitas podem mudar: o EMI in-game é a fonte definitiva.</p>')


def page(fname, title, active, body, page_js="", atlas=None, narrow=False):
    atlas_vars = ""
    if atlas:
        # caminho absoluto de proposito: url() dentro de custom property resolve
        # relativo a folha onde a var e USADA (wiki.css), nao a este documento
        atlas_vars = (f":root{{--atlas:url(/icons/atlas.png);"
                      f"--acols:{atlas['cols']};--arows:{atlas['rows']}}}")
    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/wiki.css">
<style>{atlas_vars}</style>
</head>
<body>
{nav_html(active)}
<main class="page{' narrow' if narrow else ''}">
{body}
{FOOT}
</main>
<script src="assets/wiki.js"></script>
<script>{page_js}</script>
</body>
</html>
"""
    with io.open(os.path.join(SITE, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print(f"  {fname:<20} {len(doc)/1024:>7.0f} KB")


# ======================================================================= dados

def prepare_db(atlas):
    """Copia para site/db apenas o que o cliente precisa."""
    db = os.path.join(SITE, "db")
    os.makedirs(db, exist_ok=True)

    recipes = jload("recipes.json")
    names = jload("names.json")
    aux = jload("aux_names.json")
    tags = jload("tags.json")

    # so as tags realmente referenciadas por alguma receita
    used_tags = set()
    for r in recipes:
        for side in ("in", "out"):
            for x in r.get(side, []):
                if x["k"] == "t":
                    used_tags.add(x["id"])
    tags_small = {k: v for k, v in tags.items() if k in used_tags}

    # so os nomes de ids que aparecem em receitas, tags ou tem icone
    keep = set(atlas["pos"])
    for r in recipes:
        for side in ("in", "out"):
            for x in r.get(side, []):
                keep.add(x["id"])
        if r.get("outv"):
            keep.add(r["outv"])
    for v in tags_small.values():
        keep.update(v)
    names_small = {k: v for k, v in names.items() if k in keep}
    # nomes sem receita nenhuma continuam uteis na busca de itens
    names_small.update({k: v for k, v in names.items() if k in atlas["pos"]})

    def w(n, o):
        p = os.path.join(db, n)
        with io.open(p, "w", encoding="utf-8") as f:
            json.dump(o, f, ensure_ascii=False, separators=(",", ":"))
        print(f"  db/{n:<20} {os.path.getsize(p)/1024:>7.0f} KB")

    w("recipes.json", recipes)
    w("names.json", names_small)
    w("aux_names.json", aux)
    w("tags.json", tags_small)
    return recipes, names_small, tags_small


# ======================================================================= paginas

def build_index(stats):
    cards = [
        ("guia.html", "Guia de progressão",
         "Os 9 atos do pack na ordem do questbook — de raspar cobre oxidado até abrir o End.",
         "9 atos"),
        ("itens.html", "Itens e receitas",
         "Busca em todos os itens do pack, com o que produz cada um e onde ele é usado.",
         f"{stats['recipes']:,} receitas".replace(",", ".")),
        ("plantas.html", "Plantas e cruzamento",
         "A árvore de mutação do AgriCraft com as condições exatas de solo, luz e estação.",
         f"{stats['plants']} plantas · {stats['mutations']} mutações"),
        ("abelhas.html", "Abelhas",
         "Espécies, genética e a cadeia de mutação do Complicated Bees.",
         f"{stats['species']} espécies"),
        ("rituais.html", "Rituais",
         "O livro exclusivo do pack e os rites de circle magic, com reagentes e círculos.",
         f"{stats['rituals']} rituais"),
        ("alteracoes.html", "Alterado pelo pack",
         "As receitas que o Reclamation adiciona e remove — onde a wiki genérica dos mods engana.",
         f"{stats['added']} adicionadas · {stats['removed']} removidas"),
        ("mods.html", "Mods",
         "Os 169 mods da instalação, com versão e função dentro do pack.",
         "169 mods"),
        ("livros.html", "Livros in-game",
         "Índice das páginas de guidebook de cada mod, com o que cada livro cobre.",
         f"{stats['book_pages']:,} páginas".replace(",", ".")),
    ]
    hub = "".join(
        f'<a href="{h}"><p class="t">{e(t)}</p><p class="d">{e(d)}</p><p class="c">{e(c)}</p></a>'
        for h, t, d, c in cards)
    body = f"""
<p class="eyebrow">Wiki do modpack · Reclamation 2.3.2</p>
<h1>The Kings Reclamation</h1>
<p class="lede">Wiki construída a partir da instalação real do modpack: os jars, o datapack e os
scripts do pack executados de verdade. Por isso ela acerta onde a documentação genérica dos mods
erra — as receitas que o Reclamation reescreveu.</p>
<div class="stats">
  <span>{stats['recipes']:,} receitas</span>
  <span>{stats['names']:,} itens</span>
  <span>{stats['icons']:,} ícones</span>
  <span>{stats['plants']} plantas</span>
  <span>{stats['species']} abelhas</span>
  <span>{stats['added'] + stats['removed']} receitas alteradas</span>
</div>
<div class="hub">{hub}</div>

<h2>Como esta wiki foi feita</h2>
<div class="note tip"><span class="lbl">Por que confiar nela</span>
<p>Os dados não vêm de wiki de mod. Vêm de <code>C:\\Users\\PC\\curseforge\\...\\Reclamation</code>:
169 jars lidos direto, o datapack <code>kubejs/data</code> do pack, e os
<code>server_scripts</code> <strong>executados num KubeJS falso</strong> para capturar as receitas
que só existem em tempo de execução — inclusive as geradas dentro de loops e funções.</p></div>
<p>Isso importa porque o pack faz <strong>689 operações</strong> sobre receitas. Ler o código com
expressão regular encontraria só 436 delas; executá-lo encontra todas. É a diferença entre uma
wiki que às vezes mente e uma que confere com o seu EMI.</p>
""".replace("{:,}", "")
    body = body.replace(f"{stats['recipes']:,}", f"{stats['recipes']:,}".replace(",", "."))
    body = body.replace(f"{stats['names']:,}", f"{stats['names']:,}".replace(",", "."))
    body = body.replace(f"{stats['icons']:,}", f"{stats['icons']:,}".replace(",", "."))
    page("index.html", "The Kings Reclamation", "index.html", body, narrow=True)


def build_itens(atlas):
    body = """
<p class="eyebrow">Itens e receitas</p>
<h1>Itens</h1>
<p class="lede">Busque por nome ou por id. Clique num item para ver tudo que o produz e tudo que
o consome — incluindo o que o pack alterou.</p>
<div class="searchbar">
  <input type="search" id="q" placeholder="buscar item... (ex: sulfur, aura, copper)" autocomplete="off">
  <select id="mod"><option value="">todos os mods</option></select>
  <select id="filtro">
    <option value="">tudo</option>
    <option value="pack">só alterados pelo pack</option>
    <option value="craft">só com receita</option>
  </select>
</div>
<p class="count" id="count">carregando...</p>
<div id="out"></div>
"""
    js = r"""
(async () => {
  const out = document.getElementById("out"), cnt = document.getElementById("count");
  await Promise.all([loadNames(), loadAtlas(), loadTags(), loadRecipes()]);
  const idx = buildIndex();

  const packItems = new Set();
  W.recipes.forEach((r) => {
    if (!r.pack && !r.removed) return;
    (r.out || []).forEach((x) => { if (x.k === "i") packItems.add(x.id); });
  });

  const ids = Object.keys(W.names).sort((a, b) => nameOf(a).localeCompare(nameOf(b)));
  const mods = [...new Set(ids.map((i) => i.split(":")[0]))].sort();
  const sel = document.getElementById("mod");
  mods.forEach((m) => {
    const o = document.createElement("option");
    o.value = m; o.textContent = m; sel.appendChild(o);
  });

  const searchable = ids.map((id) => ({ id, s: norm(nameOf(id) + " " + id) }));

  function render() {
    const q = norm(document.getElementById("q").value.trim());
    const m = sel.value, f = document.getElementById("filtro").value;
    let list = searchable;
    if (q) list = list.filter((x) => x.s.includes(q));
    if (m) list = list.filter((x) => x.id.startsWith(m + ":"));
    if (f === "pack") list = list.filter((x) => packItems.has(x.id));
    if (f === "craft") list = list.filter((x) => idx.made.has(x.id));
    cnt.textContent = `${list.length.toLocaleString("pt-BR")} itens` +
      (list.length > 600 ? " — mostrando os 600 primeiros, refine a busca" : "");
    const g = document.createElement("div");
    g.className = "grid";
    list.slice(0, 600).forEach((x) => {
      const b = document.createElement("button");
      b.className = "cell"; b.type = "button";
      b.appendChild(icon(x.id));
      const t = document.createElement("div");
      t.className = "nm";
      t.textContent = nameOf(x.id);
      const s = document.createElement("span");
      s.className = "id"; s.textContent = x.id;
      t.appendChild(s);
      b.appendChild(t);
      b.addEventListener("click", () => openItem(x.id));
      g.appendChild(b);
    });
    out.replaceChildren(list.length ? g : Object.assign(document.createElement("p"),
      { className: "empty", textContent: "Nada encontrado." }));
  }

  function openItem(id) {
    const d = drawer();
    const head = document.createElement("div");
    head.style.cssText = "display:flex;gap:11px;align-items:center;min-width:0";
    head.appendChild(icon(id));
    const ht = document.createElement("div");
    ht.innerHTML = `<div style="font-family:Oswald,sans-serif;text-transform:uppercase;font-size:17px;line-height:1.15">${nameOf(id)}</div><div class="mono dim">${id}</div>`;
    head.appendChild(ht);

    const body = document.createElement("div");
    const made = (idx.made.get(id) || []).map((i) => W.recipes[i]);
    const used = (idx.used.get(id) || []).map((i) => W.recipes[i]);

    const sec = (title, arr, emptyMsg) => {
      const h = document.createElement("h3");
      h.textContent = `${title} (${arr.length})`;
      body.appendChild(h);
      if (!arr.length) {
        const p = document.createElement("p");
        p.className = "empty"; p.textContent = emptyMsg;
        body.appendChild(p);
        return;
      }
      arr.slice(0, 60).forEach((r) => body.appendChild(recipeCard(r, (en) => {
        if (en.k === "i") openItem(en.id);
      })));
      if (arr.length > 60) {
        const p = document.createElement("p");
        p.className = "dim mono";
        p.textContent = `... e mais ${arr.length - 60}`;
        body.appendChild(p);
      }
    };
    sec("Como obter", made, "Nenhuma receita produz este item. Ele vem de drop, geração ou ritual.");
    sec("Onde é usado", used, "Nenhuma receita usa este item.");
    d.open(head, body);
  }

  ["q", "mod", "filtro"].forEach((i) =>
    document.getElementById(i).addEventListener("input", render));
  render();

  const h = new URLSearchParams(location.search).get("id");
  if (h && W.names[h]) openItem(h);
})();
"""
    page("itens.html", "Itens do Reclamation", "itens.html", body, js, atlas)


def build_plantas(atlas, ag):
    body = """
<p class="eyebrow">AgriCraft</p>
<h1>Plantas e cruzamento</h1>
<p class="lede">Cada planta do pack com as condições exatas de solo, luz e estação, e a árvore
completa de cruzamento. Isso normalmente só se descobre por tentativa e erro — aqui está lido
direto do datapack.</p>
<div class="note tip"><span class="lbl">Como ler</span>
<p>Uma mutação só acontece se as <strong>duas plantas-mãe</strong> estiverem adjacentes a um crop
stick vazio. A chance listada é a base — <strong>Mutativity</strong> alta melhora o resultado, e
plantar em cruz (+) dá 4 chances de escolher pais em vez de 2.</p></div>
<div class="searchbar">
  <input type="search" id="q" placeholder="buscar planta..." autocomplete="off">
  <select id="modo">
    <option value="plantas">Plantas e requisitos</option>
    <option value="mut">Árvore de cruzamento</option>
  </select>
</div>
<p class="count" id="count"></p>
<div id="out"></div>
"""
    js = """
const AG = %s;
""" % json.dumps({"plants": ag["plants"], "mutations": ag["mutations"], "soils": ag["soils"]},
                 ensure_ascii=False, separators=(",", ":")) + r"""
(async () => {
  await Promise.all([loadNames(), loadAtlas()]);
  const out = document.getElementById("out"), cnt = document.getElementById("count");

  const SEASON = { spring: "primavera", summer: "verão", autumn: "outono", winter: "inverno" };
  const LEVEL = {
    dry: "seco", wet: "úmido", damp: "úmido leve", humid: "úmido", normal: "normal",
    low: "baixo", medium: "médio", high: "alto",
    very_low: "muito baixo", very_high: "muito alto",
    acidic: "ácido", slightly_acidic: "levemente ácido", neutral: "neutro",
    slightly_alkaline: "levemente alcalino", alkaline: "alcalino",
    highly_acidic: "muito ácido", highly_alkaline: "muito alcalino",
    arid: "árido", dank: "encharcado",
  };
  const tr = (v) => LEVEL[v] || v;
  const cmp = (t) => (t === "equal" ? "=" : t === "equal_or_higher" ? "≥" : t === "equal_or_lower" ? "≤" : t || "");

  /* de qual planta sai qual semente/produto, pra mostrar icone */
  function plantIcon(id) {
    const p = AG.plants[id];
    const cand = (p && p.products && p.products[0] && p.products[0].item)
      || (p && p.seeds && p.seeds[0] && p.seeds[0].item) || id;
    return icon(cand, true);
  }
  function plantName(id) {
    const p = AG.plants[id];
    const cand = p && p.products && p.products[0] && p.products[0].item;
    if (cand && W.names[cand]) return W.names[cand];
    if (W.aux && W.aux[id]) return W.aux[id].n;
    return nameOf(id);
  }

  const plantIds = Object.keys(AG.plants).sort((a, b) => plantName(a).localeCompare(plantName(b)));
  const mutIds = Object.keys(AG.mutations);

  function renderPlantas(q) {
    const list = plantIds.filter((id) => !q || norm(plantName(id) + " " + id).includes(q));
    cnt.textContent = `${list.length} plantas`;
    const wrap = document.createElement("div");
    wrap.className = "tbl";
    const t = document.createElement("table");
    t.innerHTML = "<thead><tr><th>Planta</th><th>Solo</th><th>Luz</th><th>Estações</th>" +
      "<th>Produto</th><th>Clonável</th></tr></thead>";
    const tb = document.createElement("tbody");
    list.forEach((id) => {
      const p = AG.plants[id], rq = p.requirement || {};
      const tr_ = document.createElement("tr");

      const c1 = document.createElement("td");
      const box = document.createElement("span");
      box.style.cssText = "display:inline-flex;gap:7px;align-items:center";
      box.appendChild(plantIcon(id));
      const nm = document.createElement("span");
      nm.innerHTML = `${plantName(id)}<br><span class="mono dim">${id}</span>`;
      box.appendChild(nm);
      c1.appendChild(box);

      const soil = [];
      if (rq.soil_humidity) soil.push(`umidade ${cmp(rq.soil_humidity.type)} ${tr(rq.soil_humidity.value)}`);
      if (rq.soil_acidity) soil.push(`acidez ${cmp(rq.soil_acidity.type)} ${tr(rq.soil_acidity.value)}`);
      if (rq.soil_nutrients) soil.push(`nutrientes ${cmp(rq.soil_nutrients.type)} ${tr(rq.soil_nutrients.value)}`);
      const c2 = document.createElement("td");
      c2.innerHTML = soil.length ? soil.join("<br>") : '<span class="dim">qualquer</span>';

      const c3 = document.createElement("td");
      c3.className = "num";
      c3.textContent = (rq.min_light != null) ? `${rq.min_light}–${rq.max_light}` : "—";

      const c4 = document.createElement("td");
      c4.textContent = (rq.seasons || []).map((s) => SEASON[s] || s).join(", ") || "todas";

      const c5 = document.createElement("td");
      c5.innerHTML = (p.products || []).map((x) =>
        `${nameOf(x.item)} <span class="mono dim">${x.min ?? 1}–${x.max ?? 1}</span>`
      ).join("<br>") || "—";

      const c6 = document.createElement("td");
      c6.innerHTML = p.cloneable
        ? '<span class="badge ok">sim</span>'
        : '<span class="badge">não</span>';

      [c1, c2, c3, c4, c5, c6].forEach((c) => tr_.appendChild(c));
      tb.appendChild(tr_);
    });
    t.appendChild(tb);
    wrap.appendChild(t);
    out.replaceChildren(wrap);
  }

  function renderMut(q) {
    const list = mutIds.filter((id) => {
      const m = AG.mutations[id];
      if (!q) return true;
      return norm([m.child, m.parent1, m.parent2].map(plantName).join(" ") + " " + id).includes(q);
    }).sort((a, b) => plantName(AG.mutations[a].child).localeCompare(plantName(AG.mutations[b].child)));
    cnt.textContent = `${list.length} mutações`;
    const wrap = document.createElement("div");
    wrap.className = "tbl";
    const t = document.createElement("table");
    t.innerHTML = "<thead><tr><th>Resultado</th><th>Mãe A</th><th>Mãe B</th><th>Chance</th></tr></thead>";
    const tb = document.createElement("tbody");
    const cellFor = (pid) => {
      const td = document.createElement("td");
      const b = document.createElement("span");
      b.style.cssText = "display:inline-flex;gap:7px;align-items:center";
      b.appendChild(plantIcon(pid));
      const s = document.createElement("span");
      s.textContent = plantName(pid);
      b.appendChild(s);
      td.appendChild(b);
      return td;
    };
    list.forEach((id) => {
      const m = AG.mutations[id];
      const tr_ = document.createElement("tr");
      tr_.appendChild(cellFor(m.child));
      tr_.appendChild(cellFor(m.parent1));
      tr_.appendChild(cellFor(m.parent2));
      const c = document.createElement("td");
      c.className = "num";
      c.textContent = Math.round((m.chance ?? 0) * 100) + "%";
      tr_.appendChild(c);
      tb.appendChild(tr_);
    });
    t.appendChild(tb);
    wrap.appendChild(t);
    out.replaceChildren(wrap);
  }

  function render() {
    const q = norm(document.getElementById("q").value.trim());
    if (document.getElementById("modo").value === "mut") renderMut(q);
    else renderPlantas(q);
  }
  document.getElementById("q").addEventListener("input", render);
  document.getElementById("modo").addEventListener("change", render);
  render();
})();
"""
    page("plantas.html", "Plantas e cruzamento", "plantas.html", body, js, atlas)


def build_abelhas(atlas, bees):
    body = """
<p class="eyebrow">Complicated Bees</p>
<h1>Abelhas</h1>
<p class="lede">Espécies, genética e a cadeia completa de mutação. A regra que trava todo mundo:
especialidades só saem com a abelha <strong>ecstatic</strong> — o clima da casa tem que bater
exatamente com o preferido dela.</p>
<div class="searchbar">
  <input type="search" id="q" placeholder="buscar abelha..." autocomplete="off">
  <select id="modo">
    <option value="esp">Espécies e genes</option>
    <option value="mut">Cadeia de mutação</option>
  </select>
</div>
<p class="count" id="count"></p>
<div id="out"></div>
"""
    js = """
const BEES = %s;
""" % json.dumps(bees, ensure_ascii=False, separators=(",", ":")) + r"""
(async () => {
  await Promise.all([loadNames(), loadAtlas()]);
  const out = document.getElementById("out"), cnt = document.getElementById("count");

  const PT = {
    slowest: "lentíssima", slower: "muito lenta", slow: "lenta",
    average: "média", normal: "normal",
    fast: "rápida", faster: "muito rápida", fastest: "rapidíssima",
    shortest: "curtíssima", shorter: "muito curta", short: "curta",
    long: "longa", longer: "muito longa", longest: "longuíssima",
    diurnal: "diurna", nocturnal: "noturna", metaturnal: "dia e noite",
    crepuscular: "crepuscular",
    hot: "quente", cold: "frio", warm: "morno", cool: "fresco",
    icy: "gélido", hellish: "infernal",
    arid: "árido", dry: "seco", damp: "úmido", humid: "muito úmido",
    INVALID: "—",
  };
  const TOL = { both_1: "±1", both_2: "±2", both_3: "±3",
                up_1: "+1", up_2: "+2", down_1: "−1", down_2: "−2", none: null };
  const tr = (v) => PT[v] ?? v;
  const gene = (sp, key) => {
    const c = sp.default_chromosome || {};
    const g = c["complicated_bees:" + key];
    return g ? g : null;
  };
  const beeName = (id) => {
    const short = String(id).split(":").pop();
    return nameOf("complicated_bees:" + short) !== ("Complicated Bees " + short)
      ? (W.aux && W.aux["complicated_bees:" + short] ? W.aux["complicated_bees:" + short].n : null) || cap(short)
      : cap(short);
  };
  const cap = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  const spIds = Object.keys(BEES.species).sort();
  const mutIds = Object.keys(BEES.mutations);

  function renderEsp(q) {
    const list = spIds.filter((id) => !q || norm(id).includes(q));
    cnt.textContent = `${list.length} espécies`;
    const wrap = document.createElement("div");
    wrap.className = "tbl";
    const t = document.createElement("table");
    t.innerHTML = "<thead><tr><th>Espécie</th><th>Produtividade</th><th>Vida</th>" +
      "<th>Fertilidade</th><th>Clima</th><th>Flor</th><th>Efeito</th></tr></thead>";
    const tb = document.createElement("tbody");
    list.forEach((id) => {
      const sp = BEES.species[id];
      const g = (k) => { const x = gene(sp, k); return x ? tr(x.data) : "—"; };
      const hum = gene(sp, "humidity"), tmp = gene(sp, "temperature");
      const clim = [tmp ? tr(tmp.data) : null, hum ? tr(hum.data) : null].filter(Boolean).join(" / ") || "—";
      const tolOf = (g, lbl) => {
        if (!g || !g.tolerance) return null;
        const t = TOL[g.tolerance];
        return t ? `${lbl} ${t}` : null;
      };
      const tolp = [tolOf(tmp, "temp"), tolOf(hum, "umid")].filter(Boolean).join(" · ");
      const tr_ = document.createElement("tr");
      const sw = sp.color
        ? `<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#${sp.color};margin-right:7px;vertical-align:middle"></span>`
        : "";
      tr_.innerHTML =
        `<td>${sw}${cap(id)}</td>` +
        `<td>${g("productivity")}</td>` +
        `<td>${g("lifespan")}</td>` +
        `<td class="num">${g("fertility")}</td>` +
        `<td>${clim}${tolp ? ` <span class="mono dim">${tolp}</span>` : ""}</td>` +
        `<td>${(() => { const f = gene(sp, "flower"); return f ? (W.names[f.data] || cap(String(f.data).split(":").pop())) : "—"; })()}</td>` +
        `<td>${(() => { const x = gene(sp, "effect"); return x && x.data !== "INVALID" ? cap(String(x.data).split(":").pop()) : "—"; })()}</td>`;
      tb.appendChild(tr_);
    });
    t.appendChild(tb);
    wrap.appendChild(t);
    out.replaceChildren(wrap);
  }

  function renderMut(q) {
    const list = mutIds.filter((id) => {
      const m = BEES.mutations[id];
      return !q || norm([m.result, m.first, m.second].join(" ")).includes(q);
    }).sort((a, b) => String(BEES.mutations[a].result).localeCompare(String(BEES.mutations[b].result)));
    cnt.textContent = `${list.length} mutações`;
    const wrap = document.createElement("div");
    wrap.className = "tbl";
    const t = document.createElement("table");
    t.innerHTML = "<thead><tr><th>Resultado</th><th>Par A</th><th>Par B</th><th>Chance</th></tr></thead>";
    const tb = document.createElement("tbody");
    list.forEach((id) => {
      const m = BEES.mutations[id];
      const tr_ = document.createElement("tr");
      tr_.innerHTML =
        `<td><strong>${cap(String(m.result).split(":").pop())}</strong></td>` +
        `<td>${cap(String(m.first).split(":").pop())}</td>` +
        `<td>${cap(String(m.second).split(":").pop())}</td>` +
        `<td class="num">${Math.round((m.chance ?? 0) * 100)}%</td>`;
      tb.appendChild(tr_);
    });
    t.appendChild(tb);
    wrap.appendChild(t);
    out.replaceChildren(wrap);
  }

  function render() {
    const q = norm(document.getElementById("q").value.trim());
    if (document.getElementById("modo").value === "mut") renderMut(q);
    else renderEsp(q);
  }
  document.getElementById("q").addEventListener("input", render);
  document.getElementById("modo").addEventListener("change", render);
  render();
})();
"""
    page("abelhas.html", "Abelhas do Reclamation", "abelhas.html", body, js, atlas)


def build_rituais(atlas, rituals):
    """Livro proprio do pack + rites de circle magic."""
    entries = []
    for path, d in rituals["pack_book"].items():
        if "/entries/" not in path or not isinstance(d, dict):
            continue
        cat = path.split("/entries/")[1].split("/")[0]
        texts = []
        for pg in d.get("pages", []):
            if isinstance(pg, dict):
                for k in ("text", "description"):
                    if isinstance(pg.get(k), str):
                        texts.append(pg[k])
        rite = None
        for pg in d.get("pages", []):
            if isinstance(pg, dict) and pg.get("type", "").endswith("rite_requirements"):
                rite = pg.get("rite")
        entries.append({
            "name": d.get("name", path),
            "icon": d.get("icon"),
            "cat": cat,
            "text": " ".join(texts),
            "rite": rite,
        })
    entries.sort(key=lambda x: (x["cat"], x["name"]))

    rites = {}
    for key, d in rituals["circle_magic"].items():
        if not isinstance(d, dict) or "items" not in d:
            continue
        name = key.split("/")[-1]
        rites[name] = {
            "items": [{"id": i.get("id"), "n": i.get("Count", 1)}
                      for i in d.get("items", []) if isinstance(i, dict)],
            "shapes": d.get("shapes", {}),
            "factory": (d.get("factory") or {}).get("type"),
            "path": key,
        }

    body = """
<p class="eyebrow">Rituais</p>
<h1>Rituais</h1>
<p class="lede">O <strong>Reclamation Rituals</strong> é o livro exclusivo do pack — não existe
documentação dele em lugar nenhum. Abaixo, as entradas do livro e os rites de circle magic com
reagentes e círculos de giz.</p>
<div class="note warn"><span class="lbl">Atenção</span>
<p>O <strong>Ritual of Reclamation</strong> pode apagar blocos. Execute longe de qualquer coisa
que você preze.</p></div>
<div class="searchbar">
  <input type="search" id="q" placeholder="buscar ritual..." autocomplete="off">
  <select id="modo">
    <option value="book">Livro do pack</option>
    <option value="circle">Circle magic (reagentes)</option>
  </select>
</div>
<p class="count" id="count"></p>
<div id="out"></div>
"""
    js = ("const ENTRIES = %s;\nconst RITES = %s;\n" % (
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
        json.dumps(rites, ensure_ascii=False, separators=(",", ":")))) + r"""
(async () => {
  await Promise.all([loadNames(), loadAtlas()]);
  const out = document.getElementById("out"), cnt = document.getElementById("count");
  const CAT = { basic_rituals: "Rituais básicos", terraforming: "Terraformação" };
  const cap = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  function renderBook(q) {
    const list = ENTRIES.filter((x) => !q || norm(x.name + " " + x.text).includes(q));
    cnt.textContent = `${list.length} entradas do livro`;
    const frag = document.createDocumentFragment();
    let cur = null;
    list.forEach((x) => {
      if (x.cat !== cur) {
        cur = x.cat;
        const h = document.createElement("h2");
        h.textContent = CAT[cur] || cap(cur);
        frag.appendChild(h);
      }
      const c = document.createElement("div");
      c.className = "card";
      const head = document.createElement("div");
      head.style.cssText = "display:flex;gap:10px;align-items:center;margin-bottom:8px";
      if (x.icon) head.appendChild(icon(x.icon));
      const t = document.createElement("div");
      t.style.cssText = "font-family:Oswald,sans-serif;text-transform:uppercase;font-size:16px";
      t.textContent = x.name;
      head.appendChild(t);
      if (x.rite) {
        const b = document.createElement("span");
        b.className = "badge aura";
        b.textContent = x.rite;
        head.appendChild(b);
      }
      c.appendChild(head);
      const p = document.createElement("p");
      p.style.margin = "0";
      p.textContent = x.text.replace(/\$\(.*?\)/g, "").replace(/\s+/g, " ").trim() || "—";
      c.appendChild(p);
      frag.appendChild(c);
    });
    out.replaceChildren(frag);
  }

  function renderCircle(q) {
    const keys = Object.keys(RITES).filter((k) => !q || norm(k).includes(q)).sort();
    cnt.textContent = `${keys.length} rites de circle magic`;
    const frag = document.createDocumentFragment();
    keys.forEach((k) => {
      const r = RITES[k];
      const c = document.createElement("div");
      c.className = "card";
      const t = document.createElement("div");
      t.style.cssText = "font-family:Oswald,sans-serif;text-transform:uppercase;font-size:16px;margin-bottom:9px";
      t.textContent = cap(k);
      c.appendChild(t);

      const circles = Object.entries(r.shapes || {});
      if (circles.length) {
        const s = document.createElement("p");
        s.style.cssText = "margin:0 0 9px";
        s.innerHTML = circles.map(([shape, chalk]) =>
          `<span class="badge">${cap(String(shape).split(":").pop())} · ${cap(String(chalk).split(":").pop())}</span>`
        ).join(" ");
        c.appendChild(s);
      }
      const side = document.createElement("div");
      side.className = "side";
      (r.items || []).forEach((i) => side.appendChild(chip({ k: "i", id: i.id, n: i.n })));
      if (!r.items.length) {
        const d = document.createElement("span");
        d.className = "dim"; d.textContent = "sem reagente listado";
        side.appendChild(d);
      }
      c.appendChild(side);
      frag.appendChild(c);
    });
    out.replaceChildren(frag);
  }

  function render() {
    const q = norm(document.getElementById("q").value.trim());
    if (document.getElementById("modo").value === "circle") renderCircle(q);
    else renderBook(q);
  }
  document.getElementById("q").addEventListener("input", render);
  document.getElementById("modo").addEventListener("change", render);
  render();
})();
"""
    page("rituais.html", "Rituais do Reclamation", "rituais.html", body, js, atlas)
    return len(entries) + len(rites)


def build_alteracoes(atlas):
    body = """
<p class="eyebrow">Alterado pelo pack</p>
<h1>Alterações</h1>
<p class="lede">Onde a wiki genérica dos mods engana. Estas são as receitas que o Reclamation
<strong>adiciona</strong> e as que ele <strong>remove</strong> — capturadas executando os
scripts do pack, não lendo o código.</p>
<div class="searchbar">
  <input type="search" id="q" placeholder="buscar por item ou tipo..." autocomplete="off">
  <select id="modo">
    <option value="add">Adicionadas pelo pack</option>
    <option value="rem">Removidas pelo pack</option>
  </select>
</div>
<p class="count" id="count">carregando...</p>
<div id="out"></div>
"""
    js = r"""
(async () => {
  await Promise.all([loadNames(), loadAtlas(), loadTags(), loadRecipes()]);
  const out = document.getElementById("out"), cnt = document.getElementById("count");
  const added = W.recipes.filter((r) => r.pack);
  const removed = W.recipes.filter((r) => r.removed);

  function text(r) {
    return norm([...(r.in || []), ...(r.out || [])].map((x) => nameOf(x.id) + " " + x.id).join(" ")
      + " " + r.t + " " + (r.where || ""));
  }
  function render() {
    const q = norm(document.getElementById("q").value.trim());
    const base = document.getElementById("modo").value === "rem" ? removed : added;
    const list = q ? base.filter((r) => text(r).includes(q)) : base;
    cnt.textContent = `${list.length} receitas`;
    const frag = document.createDocumentFragment();
    list.slice(0, 400).forEach((r) => frag.appendChild(recipeCard(r, (en) => {
      if (en.k === "i") location.href = "itens.html?id=" + encodeURIComponent(en.id);
    })));
    if (list.length > 400) {
      const p = document.createElement("p");
      p.className = "dim mono";
      p.textContent = `... e mais ${list.length - 400}. Refine a busca.`;
      frag.appendChild(p);
    }
    out.replaceChildren(frag);
  }
  document.getElementById("q").addEventListener("input", render);
  document.getElementById("modo").addEventListener("change", render);
  render();
})();
"""
    page("alteracoes.html", "Alterações do pack", "alteracoes.html", body, js, atlas)


def build_mods(mods):
    ROLE = {
        "theurgy": "Alquimia base — cria terra e ferro do nada; loop de metais no late game.",
        "enchanted": "Bruxaria — mutandis, altar de plantas, rituais, brilliant fiber.",
        "agricraft": "Genética de plantas — 5 stats, cruzamento, Cuprosia.",
        "naturesaura": "Aura por chunk, Natural Altar, ritual da grama, Altar of Birthing.",
        "botania": "Mana, Pure Daisy (ouro), Fel Pumpkin (blaze), Terrasteel, Alfheim.",
        "embers": "Ember infinito da bedrock, fundição, Dawnstone, alquimia por tentativa e erro.",
        "bloodmagic": "Gemas (diamante, lápis, ametista), Demon Realm, demonic will.",
        "ars_nouveau": "Source, encantamentos, familiares, rituais, storage lectern.",
        "mekanism": "Aço, energia, processamento de minério até 3,3×, reatores, antimatéria.",
        "ae2": "Armazenamento e autocraft digital.",
        "reclamation_util": "Biome bottles, globes, frame remover — o endgame do pack.",
        "complicated_bees": "Geração de recursos por genética de abelhas.",
        "mysticalagriculture": "Essências e sementes de recurso.",
        "create": "Uso leve: haunting, mixing, pressing, brass.",
        "croptopia": "~60 cultivos e árvores frutíferas.",
        "farmersdelight": "Cutting board (essencial no early game), cozinha.",
        "cookingforblockheads": "Cozinha multibloco.",
        "kubejs": "Motor de scripts — é o que reescreve as receitas do pack.",
    }
    rows = []
    for m in sorted(mods, key=lambda x: (x.get("name") or x["jar"]).lower()):
        mid = m.get("id") or ""
        rows.append(
            f'<tr><td><strong>{e(m.get("name") or m["jar"])}</strong>'
            f'<br><span class="mono dim">{e(mid)}</span></td>'
            f'<td class="num">{e(m.get("version") or "—")}</td>'
            f'<td>{e(ROLE.get(mid, "") or (m.get("desc") or "")[:180])}</td></tr>')
    body = f"""
<p class="eyebrow">Instalação</p>
<h1>Mods</h1>
<p class="lede">Os {len(mods)} mods lidos da sua instância, com a versão exata. A coluna de função
descreve o papel dentro do Reclamation, não o mod em geral.</p>
<div class="tbl"><table>
<thead><tr><th>Mod</th><th>Versão</th><th>Função no pack</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
"""
    page("mods.html", "Mods da instalação", "mods.html", body)


def build_livros(books):
    LIV = {
        "theurgy:books": ("The Hermetica", "Theurgy / Spagyrics — a base de todo o começo do pack."),
        "naturesaura:book": ("Book of Natural Aura", "Multiblocos, geradores de aura e o Ritual of the Forest."),
        "botania:lexicon": ("Lexica Botania", "Mana, flores, runas. Jogue no portal de Alfheim depois."),
        "bloodmagic:guide": ("Sanguine Scientiem", "Runas, rituais, Incense Altar, Demon Realm."),
        "ars_nouveau:worn_notebook": ("Worn Notebook", "Glifos, familiares, rituais, Source."),
        "complicated_bees:field_guide": ("Apiarist Field Guide", "Genética, Mellarium, Gyrofuge."),
        "mysticalagriculture:guide": ("Mystical Agriculture Guide", "Essências, sementes, maquinário."),
        "croptopia:guide": ("Croptopia Guide", "Os ~60 cultivos e receitas de comida."),
        "enchanted:circle_magic": ("Circle Magic", "Rituais de giz do Enchanted."),
        "enchanted:brewing": ("Brewing", "Caldeirão da bruxa e poções."),
        "enchanted:extraction": ("Extraction", "Destilaria, forno da bruxa, fumaças."),
        "buildinggadgets2:buildinggadgets2book": ("Building Gadgets", "Uso das ferramentas de construção."),
    }
    rows = []
    for key, pages in sorted(books.items(), key=lambda kv: -len(kv[1])):
        nice, desc = LIV.get(key, (key.split(":")[-1].replace("_", " ").title(), ""))
        rows.append(
            f'<tr><td><strong>{e(nice)}</strong><br><span class="mono dim">{e(key)}</span></td>'
            f'<td class="num">{len(pages)}</td><td>{e(desc)}</td></tr>')
    body = f"""
<p class="eyebrow">Documentação in-game</p>
<h1>Livros</h1>
<p class="lede">Todo guidebook que existe dentro do jogo, com quantas páginas cada um tem.
Junte todos no <strong>Akashic Tome</strong> logo no começo — ele funde os livros num item só.</p>
<div class="note tip"><span class="lbl">O mais importante</span>
<p>O <strong>Reclamation Rituals</strong> é exclusivo do pack e não aparece nesta lista porque
não vem de mod nenhum: ele é um livro Patchouli do próprio modpack. Faça com
<code>livro + dried earth</code>. O conteúdo dele está em
<a href="rituais.html">Rituais</a>.</p></div>
<div class="tbl"><table>
<thead><tr><th>Livro</th><th>Páginas</th><th>Cobre</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
"""
    page("livros.html", "Livros in-game", "livros.html", body, narrow=True)
    return sum(len(v) for v in books.values())


def build_guia():
    """Reaproveita o manual ja escrito, injetando a navegacao global."""
    src = io.open(os.path.join(ROOT, "manual-reclamation.html"), encoding="utf-8").read()
    cut = src.index("</style>") + len("</style>")
    head, bodypart = src[:cut], src[cut:]
    head = re.sub(r"<title>.*?</title>\s*", "", head, flags=re.S)
    # a barra global e sticky: empurra a sidebar do manual pra baixo dela
    head = head.replace("</style>", """
.side{top:54px!important;height:calc(100vh - 54px)!important}
@media (max-width:900px){ .topbar{top:54px!important} }
</style>""")
    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guia de progressão — Reclamation</title>
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="assets/wiki.css">
{head}
</head>
<body>
{nav_html("guia.html")}
{bodypart}
</body>
</html>
"""
    with io.open(os.path.join(SITE, "guia.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print(f"  guia.html            {len(doc)/1024:>7.0f} KB")


# ======================================================================= main

def main():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "icons"), exist_ok=True)

    with io.open(os.path.join(SITE, "assets", "wiki.css"), "w", encoding="utf-8") as f:
        f.write(theme.CSS)
    with io.open(os.path.join(SITE, "assets", "wiki.js"), "w", encoding="utf-8") as f:
        f.write(theme.JS)

    shutil.copy(os.path.join(DATA, "icons", "atlas.png"), os.path.join(SITE, "icons", "atlas.png"))
    shutil.copy(os.path.join(DATA, "icons", "atlas.json"), os.path.join(SITE, "icons", "atlas.json"))
    atlas = jload("icons/atlas.json")

    print("dados:")
    recipes, names, tags = prepare_db(atlas)

    ag = jload("agricraft.json")
    bees = jload("bees.json")
    rituals = jload("rituals.json")
    books = jload("books.json")
    mods = jload("mods.json")

    print("paginas:")
    build_guia()
    build_itens(atlas)
    build_plantas(atlas, ag)
    build_abelhas(atlas, bees)
    n_rituals = build_rituais(atlas, rituals)
    build_alteracoes(atlas)
    build_mods(mods)
    n_pages = build_livros(books)

    stats = {
        "recipes": len(recipes),
        "names": len(names),
        "icons": len(atlas["pos"]),
        "plants": len(ag["plants"]),
        "mutations": len(ag["mutations"]),
        "species": len(bees["species"]),
        "rituals": n_rituals,
        "added": sum(1 for r in recipes if r.get("pack")),
        "removed": sum(1 for r in recipes if r.get("removed")),
        "book_pages": n_pages,
    }
    build_index(stats)

    total = sum(os.path.getsize(os.path.join(dp, f))
                for dp, _, fs in os.walk(SITE) for f in fs)
    print(f"\ntotal do site: {total/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
