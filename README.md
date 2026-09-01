# The Kings Reclamation

Wiki completa do modpack **Reclamation — Reclaim the World**
(v2.3.2 · Minecraft 1.20.1 · Forge 47.4.0), em português.

🌱 **https://drenossauro.github.io/the-kings-reclamation/**

## O que a torna diferente

Os dados não vêm de wiki de mod. Vêm da instalação real:

- **169 jars** lidos direto (incluindo o jar vanilla do 1.20.1)
- o **datapack do pack** (`kubejs/data`)
- os **`server_scripts` executados** num KubeJS falso, para capturar as receitas
  que só existem em tempo de execução — inclusive as geradas dentro de loops e
  funções auxiliares

Esse último ponto importa: o pack faz **689 operações** sobre receitas. Ler o
código com expressão regular encontra 436; executá-lo encontra todas. É a
diferença entre uma wiki que às vezes mente e uma que confere com o EMI.

## Conteúdo

| Página | O que tem |
|---|---|
| Guia | Os 9 atos de progressão, na ordem do questbook |
| Itens | 25.055 receitas, busca, "como obter" e "onde é usado" |
| Plantas | 171 plantas AgriCraft com solo/luz/estação + 124 mutações |
| Abelhas | 77 espécies com genética + 85 mutações |
| Rituais | Livro exclusivo do pack + 27 rites de circle magic com reagentes |
| Embers | Guia do Embers Rekindled + as 32 combinacoes de alquimia (aspectus) |
| Alterações | As 427 receitas adicionadas e 311 removidas pelo pack |
| Mods | Os 169 mods com versão e função no pack |
| Livros | Índice dos guidebooks in-game |

## Pipeline

```bash
python tools/extract.py all     # jars + datapack + node dump -> data/
python tools/build_site.py      # data/ -> site/
git add -A && git commit -m "..." && git push   # o Pages publica sozinho
```

O `site/` fica versionado de proposito: gerar exige os jars do modpack, que so
existem na maquina local, entao o CI nao tem como reconstruir.

`tools/extract.py` aceita um estágio por vez (`names`, `recipes`, `icons`,
`agricraft`, `bees`, `rituals`, `embers`, `books`, `overlay`, `mods`) para iterar rápido.

`tools/dump_kubejs.mjs` é o harness Node que executa os scripts do pack com
stubs de `ServerEvents`/`Item`/`LootJS` e grava cada chamada de receita já
resolvida.

## Estrutura

| Caminho | O que é |
|---|---|
| `tools/extract.py` | jars/datapack/scripts → `data/*.json` |
| `tools/dump_kubejs.mjs` | executa os scripts do pack, captura as receitas |
| `tools/theme.py` | CSS e JS compartilhados pelas páginas |
| `tools/build_site.py` | `data/` → `site/` |
| `manual-reclamation.html` | fonte do guia de progressão (vira `site/guia.html`) |
| `data/` | derivado, não versionado — recriar com o extrator |
| `site/` | o que o GitHub Pages serve |

## Aviso

Se o modpack for atualizado, receitas mudam. Rode o pipeline de novo.
O EMI dentro do jogo é sempre a fonte definitiva.
