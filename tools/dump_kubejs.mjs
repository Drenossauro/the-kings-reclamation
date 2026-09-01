/**
 * Executa os server_scripts do pack com um KubeJS falso e grava toda chamada
 * de receita com os argumentos JA RESOLVIDOS (loops e funcoes auxiliares
 * inclusos). Substitui o parser por regex, que nao alcanca codigo dinamico.
 *
 * uso: node tools/dump_kubejs.mjs <dir_server_scripts> > data/kubejs_calls.json
 */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const dir = process.argv[2];
if (!dir) {
  console.error("uso: node dump_kubejs.mjs <dir>");
  process.exit(1);
}

const calls = [];
let currentFile = "";

/** objeto encadeavel: .id(...).stage(...) etc nao quebram */
function chainable(record) {
  const handler = {
    get(_t, prop) {
      if (prop === "then") return undefined; // nao e promise
      if (prop === Symbol.toPrimitive) return () => "[recipe]";
      return (...args) => {
        if (prop === "id" && typeof args[0] === "string") record.rid = args[0];
        else record.chain = (record.chain || []).concat([{ m: String(prop), a: safe(args) }]);
        return new Proxy({}, handler);
      };
    },
  };
  return new Proxy({}, handler);
}

function safe(v, depth = 0) {
  if (depth > 12) return "[deep]";
  if (v === null || v === undefined) return null;
  const t = typeof v;
  if (t === "string" || t === "number" || t === "boolean") return v;
  if (t === "function") return "[fn]";
  if (Array.isArray(v)) return v.map((x) => safe(x, depth + 1));
  if (t === "object") {
    const o = {};
    for (const k of Object.keys(v)) {
      try { o[k] = safe(v[k], depth + 1); } catch { o[k] = "[err]"; }
    }
    return o;
  }
  return String(v);
}

function recorder(kind) {
  return new Proxy({}, {
    get(_t, prop) {
      const name = String(prop);
      return (...args) => {
        const rec = { file: currentFile, event: kind, op: name, args: safe(args) };
        calls.push(rec);
        return chainable(rec);
      };
    },
  });
}

// ---- stubs dos globais que os scripts usam
const Item = {
  of: (...a) => ({ __item: safe(a) }),
  getList: () => [],
};
const Ingredient = { of: (...a) => ({ __ingredient: safe(a) }) };
const Fluid = { of: (...a) => ({ __fluid: safe(a) }) };
const Component = new Proxy({}, {
  get: () => (...a) => new Proxy({}, { get: () => () => ({ __text: safe(a) }) }),
});
const Platform = { mods: new Proxy({}, { get: () => ({}) }) };

const sandbox = {
  console,
  Math,
  JSON,
  String, Number, Boolean, Array, Object,
  Item, Ingredient, Fluid, Component, Platform,
  ServerEvents: {
    recipes: (fn) => fn(recorder("recipes")),
    tags: (type, fn) => fn(recorder("tags:" + type)),
    loaded: () => {},
    highPriorityData: () => {},
  },
  LootJS: { modifiers: (fn) => { try { fn(recorder("loot")); } catch {} } },
  EntityEvents: new Proxy({}, { get: () => () => {} }),
  BlockEvents: new Proxy({}, { get: () => () => {} }),
  ItemEvents: new Proxy({}, { get: () => () => {} }),
  StartupEvents: new Proxy({}, { get: () => () => {} }),
  onEvent: (_n, fn) => { try { fn(recorder("legacy")); } catch {} },
};
sandbox.global = sandbox;
vm.createContext(sandbox);

const errors = [];
for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".js")).sort()) {
  currentFile = f;
  const code = fs.readFileSync(path.join(dir, f), "utf8");
  try {
    vm.runInContext(code, sandbox, { filename: f, timeout: 20000 });
  } catch (e) {
    errors.push({ file: f, error: String(e).slice(0, 200) });
  }
}

process.stdout.write(JSON.stringify({ calls, errors }, null, 0));
console.error(`arquivos: ok | chamadas: ${calls.length} | erros: ${errors.length}`);
for (const e of errors) console.error("  ERRO", e.file, e.error);
