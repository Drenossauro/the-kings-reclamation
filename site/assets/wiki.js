
/* ---------------- nucleo compartilhado da wiki ---------------- */
const W = {
  names: null, aux: null, atlas: null, recipes: null, tags: null,
  _p: {},
};

function once(key, fn) {
  if (!W._p[key]) W._p[key] = fn();
  return W._p[key];
}

async function getJSON(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error(path + ": " + r.status);
  return r.json();
}

const loadNames  = () => once("names", async () => {
  const [n, a] = await Promise.all([getJSON("db/names.json"), getJSON("db/aux_names.json")]);
  W.names = n; W.aux = a; return n;
});
const loadAtlas   = () => once("atlas", async () => (W.atlas = await getJSON("icons/atlas.json")));
const loadRecipes = () => once("recipes", async () => (W.recipes = await getJSON("db/recipes.json")));
const loadTags    = () => once("tags", async () => (W.tags = await getJSON("db/tags.json")));

/* nome legivel de um id, com fallback derivado do proprio id */
function nameOf(id) {
  if (W.names && W.names[id]) return W.names[id];
  if (W.aux && W.aux[id]) return W.aux[id].n;
  const p = String(id).split(":").pop() || String(id);
  return p.replace(/[_/]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
function kindOf(id) {
  if (W.names && W.names[id]) return null;
  if (W.aux && W.aux[id]) return W.aux[id].k;
  return null;
}

/* elemento de icone posicionado no atlas */
function icon(id, small) {
  const s = document.createElement("span");
  s.className = "ico" + (small ? " sm" : "");
  const pos = W.atlas && W.atlas.pos[id];
  if (!pos) { s.classList.add("none"); return s; }
  const u = small ? 20 : 32;
  s.style.backgroundPosition = `-${pos[0] * u}px -${pos[1] * u}px`;
  return s;
}

/* chip clicavel de item/tag */
function chip(entry, onClick) {
  const b = document.createElement("button");
  b.className = "chip" + (entry.k === "t" ? " tag" : "");
  b.type = "button";
  const id = entry.id;
  if (entry.k === "t") {
    const members = (W.tags && W.tags[id]) || [];
    b.appendChild(icon(members[0], true));
    const t = document.createElement("span");
    t.textContent = "qualquer " + nameOf(id).toLowerCase();
    b.appendChild(t);
    const c = document.createElement("span");
    c.className = "x";
    c.textContent = members.length ? `${members.length} itens` : "tag";
    b.appendChild(c);
    b.title = "#" + id;
  } else {
    b.appendChild(icon(id, true));
    const t = document.createElement("span");
    t.textContent = nameOf(id);
    b.appendChild(t);
    if (entry.n && entry.n > 1) {
      const c = document.createElement("span");
      c.className = "x";
      c.textContent = "x" + entry.n;
      b.appendChild(c);
    }
    b.title = id;
  }
  if (onClick) b.addEventListener("click", () => onClick(entry));
  return b;
}

/* nome curto e legivel do tipo de receita */
function recipeTypeLabel(t) {
  const map = {
    "minecraft:crafting_shaped": "Bancada (com forma)",
    "minecraft:crafting_shapeless": "Bancada (sem forma)",
    "minecraft:smelting": "Fornalha",
    "minecraft:blasting": "Blast Furnace",
    "minecraft:smoking": "Defumador",
    "minecraft:campfire_cooking": "Fogueira",
    "minecraft:stonecutting": "Serra de pedra",
    "minecraft:smithing_transform": "Bancada de ferraria",
    "farmersdelight:cutting": "Cutting Board",
    "farmersdelight:cooking": "Cooking Pot",
  };
  if (map[t]) return map[t];
  const [ns, rest] = String(t).split(":");
  const pretty = (rest || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  return `${pretty} (${ns})`;
}

/* card de uma receita */
function recipeCard(r, onItem) {
  const d = document.createElement("div");
  d.className = "rec" + (r.removed ? " gone" : "");

  const h = document.createElement("div");
  h.className = "rec-h";
  const t = document.createElement("span");
  t.className = "rec-t";
  t.textContent = recipeTypeLabel(r.t);
  h.appendChild(t);
  if (r.pack) {
    const b = document.createElement("span");
    b.className = "badge pack";
    b.textContent = "adicionada pelo pack";
    b.title = r.where || "";
    h.appendChild(b);
  }
  if (r.removed) {
    const b = document.createElement("span");
    b.className = "badge gone";
    b.textContent = "removida pelo pack";
    h.appendChild(b);
  }
  d.appendChild(h);

  const flow = document.createElement("div");
  flow.className = "flow";
  const left = document.createElement("div");
  left.className = "side";
  (r.in || []).forEach((e) => left.appendChild(chip(e, onItem)));
  if (!(r.in || []).length) {
    const s = document.createElement("span");
    s.className = "dim";
    s.textContent = "sem ingrediente listado";
    left.appendChild(s);
  }
  flow.appendChild(left);

  const a = document.createElement("span");
  a.className = "arrow";
  a.textContent = "→";
  flow.appendChild(a);

  const right = document.createElement("div");
  right.className = "side";
  (r.out || []).forEach((e) => right.appendChild(chip(e, onItem)));
  if (!(r.out || []).length) {
    const s = document.createElement("span");
    if (r.outv) {
      s.className = "badge aura";
      s.textContent = `${r.outk || "resultado"}: ${nameOf(r.outv)}`;
    } else {
      s.className = "dim";
      s.textContent = "resultado nao e um item";
    }
    right.appendChild(s);
  }
  flow.appendChild(right);
  d.appendChild(flow);
  return d;
}

/* indices reversos: item -> receitas que o produzem / consomem */
function buildIndex() {
  if (W._idx) return W._idx;
  const made = new Map(), used = new Map();
  const push = (m, k, v) => { if (!m.has(k)) m.set(k, []); m.get(k).push(v); };
  W.recipes.forEach((r, i) => {
    (r.out || []).forEach((e) => { if (e.k === "i") push(made, e.id, i); });
    (r.in || []).forEach((e) => {
      if (e.k === "i") push(used, e.id, i);
      else if (W.tags && W.tags[e.id]) W.tags[e.id].forEach((m) => push(used, m, i));
    });
  });
  W._idx = { made, used };
  return W._idx;
}

/* drawer lateral reutilizavel */
function drawer() {
  if (W._drawer) return W._drawer;
  const scrim = document.createElement("div");
  scrim.className = "scrim";
  const el = document.createElement("aside");
  el.className = "drawer";
  el.innerHTML =
    '<div class="drawer-h"><div class="dh-body"></div>' +
    '<button class="close" type="button">fechar</button></div>' +
    '<div class="drawer-b"></div>';
  document.body.appendChild(scrim);
  document.body.appendChild(el);
  const close = () => { el.classList.remove("open"); scrim.classList.remove("on"); };
  el.querySelector(".close").addEventListener("click", close);
  scrim.addEventListener("click", close);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
  W._drawer = {
    el, scrim, close,
    open(headEl, bodyEl) {
      const h = el.querySelector(".dh-body"), b = el.querySelector(".drawer-b");
      h.replaceChildren(headEl);
      b.replaceChildren(bodyEl);
      b.scrollTop = 0;
      el.classList.add("open");
      scrim.classList.add("on");
    },
  };
  return W._drawer;
}

/* normaliza texto pra busca (sem acento, minusculo) */
function norm(s) {
  return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
}
