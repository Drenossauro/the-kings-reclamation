# -*- coding: utf-8 -*-
"""Empacota o artifact (fragmento HTML) num documento standalone para deploy estatico."""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "manual-reclamation.html")
OUT_DIR = os.path.join(HERE, "site")
OUT = os.path.join(OUT_DIR, "index.html")

frag = io.open(SRC, encoding="utf-8").read()

# o fragmento e: <title> ... <link> ... <style>...</style> ... conteudo do body
cut = frag.index("</style>") + len("</style>")
head_part = frag[:cut].strip()
body_part = frag[cut:].strip()

title_m = re.search(r"<title>(.*?)</title>", head_part, re.S)
title = title_m.group(1).strip() if title_m else "Manual do Reclamation"
head_part = re.sub(r"<title>.*?</title>\s*", "", head_part, flags=re.S).strip()

DESC = ("Guia de progressao completo do modpack Reclamation 2.3.2 (Minecraft 1.20.1) "
        "em portugues, escrito a partir do questbook e dos scripts do pack.")

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%B1%3C/text%3E%3C/svg%3E"
)

doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{FAVICON}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC}">
<meta name="twitter:card" content="summary">
{head_part}
</head>
<body>
{body_part}
</body>
</html>
"""

os.makedirs(OUT_DIR, exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
print("escrito:", OUT, len(doc), "bytes")
