# The Kings Reclamation

Manual de progressão em português do modpack **Reclamation — Reclaim the World**
(v2.3.2 · Minecraft 1.20.1 · Forge 47.4.0).

🌱 **Site:** https://the-kings-reclamation.vercel.app

## O que é

Guia completo dos 9 atos de progressão do pack, escrito a partir do questbook FTB
da instalação real (10 capítulos, 558 quests) e dos scripts KubeJS que reescrevem
receitas — não de wikis genéricas dos mods. Inclui mecânicas do pack que não
aparecem em nenhuma quest, como a bateia de cobre com tigela em gravel.

## Estrutura

| Arquivo | O que é |
|---|---|
| `manual-reclamation.html` | fonte da página (fragmento HTML, sem `<head>`/`<body>`) |
| `build.py` | empacota a fonte em `site/index.html` como documento standalone |
| `site/index.html` | build servido pela Vercel |
| `MANUAL-RECLAMATION-PTBR.md` | mesmo conteúdo em Markdown |
| `vercel.json` | config do deploy estático (`outputDirectory: site`) |

## Publicar

```bash
python build.py && vercel deploy --prod --yes
```

## Aviso

Se o modpack for atualizado, receitas podem mudar. O EMI dentro do jogo é sempre
a fonte definitiva.
