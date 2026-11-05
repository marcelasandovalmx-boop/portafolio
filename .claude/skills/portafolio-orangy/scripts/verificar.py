#!/usr/bin/env python3
"""Revisa el portafolio Orangy antes de hacer commit.

Uso: verificar.py [raíz del repo]   (default: directorio actual)

Checa:
  - toda imagen referenciada en index.html y links/index.html existe
  - cada slide (img/caso-*, img/otros) tiene su -sm y ambas son 4:5
  - el <img> de cada slide trae srcset con su -sm
  - no hay más familia tipográfica que Montserrat
"""
import re
import sys
from pathlib import Path

from PIL import Image

raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
errores, avisos = [], []

for html in [raiz / "index.html", raiz / "links/index.html"]:
    if not html.exists():
        continue
    txt = html.read_text(encoding="utf-8")
    base = html.parent
    refs = set(re.findall(r'(?:src|href)="([^"#:]+\.(?:jpg|jpeg|png|svg|webp))"', txt))
    for m in re.findall(r'srcset="([^"]+)"', txt):
        refs.update(p.strip().split()[0] for p in m.split(","))
    for r in sorted(refs):
        if not (base / r).exists():
            errores.append(f"{html.name}: no existe {r}")

    for tag in re.findall(r'<div class="slide"><img[^>]+>', txt):
        src = re.search(r'src="([^"]+)"', tag).group(1)
        sm = src.replace(".jpg", "-sm.jpg")
        if sm not in tag:
            errores.append(f"{html.name}: {src} sin srcset a {sm}")
        if 'alt=""' in tag or "alt=" not in tag:
            avisos.append(f"{html.name}: {src} sin alt descriptivo")

    variables = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", txt))
    familias = re.findall(r"font-family\s*:\s*([^;}\"]+)", txt)
    familias += [v for k, v in variables.items() if "'" in v and "serif" in v]
    for fam in familias:
        fam = re.sub(r"var\((--[\w-]+)\)", lambda m: variables.get(m.group(1), m.group(0)), fam)
        nombres = [f.strip(" '\"").lower() for f in fam.split(",")]
        ajenas = [n for n in nombres if n not in ("montserrat", "sans-serif", "inherit", "system-ui")]
        if ajenas:
            errores.append(f"{html.name}: fuente no permitida -> {fam.strip()}")

for carpeta in list((raiz / "img").glob("caso-*")) + [raiz / "img/otros"]:
    if not carpeta.is_dir():
        continue
    for f in sorted(carpeta.glob("*.jpg")):
        if f.stem.endswith("-sm"):
            continue
        sm = f.with_name(f.stem + "-sm.jpg")
        if not sm.exists():
            errores.append(f"falta {sm}")
        for p in (f, sm):
            if p.exists():
                w, h = Image.open(p).size
                if abs(w / h - 0.8) > 0.01:
                    errores.append(f"{p}: {w}x{h} no es 4:5")

for a in avisos:
    print("aviso:", a)
for e in errores:
    print("ERROR:", e)
print("OK" if not errores else f"{len(errores)} error(es)")
sys.exit(1 if errores else 0)
