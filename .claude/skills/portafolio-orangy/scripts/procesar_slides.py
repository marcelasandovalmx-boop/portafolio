#!/usr/bin/env python3
"""Procesa imágenes o PDFs a slides 4:5 para el portafolio Orangy.

Salida por imagen:
  <nombre>.jpg     1620x2025, JPG q90 (full-res, la usa el lightbox)
  <nombre>-sm.jpg   800x1000, JPG q82 (srcset móvil)

Uso:
  procesar_slides.py pdf archivo.pdf DESTINO [--desde N] [--paginas 1,3,5]
  procesar_slides.py img a.jpg b.png --salida DESTINO [--desde N]
  procesar_slides.py img logo.png --salida img/otros --nombre kalu

Opciones de recorte:
  --foco x,y   centro del recorte (0-1). Default 0.5,0.5
  --contener   no recorta: encaja la imagen completa sobre --fondo
  --fondo HEX  color de relleno para --contener (default: color de la esquina)

El orden de salida es el orden de entrada (páginas del PDF o argumentos):
el orden que manda March es sagrado.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

FULL = (1620, 2025)
SM = (800, 1000)
RATIO = 4 / 5


def recortar_cover(im, foco):
    w, h = im.size
    fx, fy = foco
    if w / h > RATIO:  # demasiado ancha: recorta lados
        nw = round(h * RATIO)
        x = min(max(round(fx * w - nw / 2), 0), w - nw)
        return im.crop((x, 0, x + nw, h))
    nh = round(w / RATIO)
    y = min(max(round(fy * h - nh / 2), 0), h - nh)
    return im.crop((0, y, w, y + nh))


def contener(im, fondo):
    if fondo is None:
        fondo = im.getpixel((0, 0))
    lienzo = Image.new("RGB", FULL, fondo)
    copia = im.copy()
    copia.thumbnail(FULL, Image.LANCZOS)
    lienzo.paste(copia, ((FULL[0] - copia.width) // 2, (FULL[1] - copia.height) // 2))
    return lienzo


def procesar(origen, destino_dir, nombre, foco, modo_contener, fondo):
    im = ImageOps.exif_transpose(Image.open(origen))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        base = Image.new("RGB", im.size, fondo or "#FFFFFF")
        base.paste(im, mask=im.split()[-1])
        im = base
    else:
        im = im.convert("RGB")
    if modo_contener:
        full = contener(im, fondo)
    else:
        full = recortar_cover(im, foco).resize(FULL, Image.LANCZOS)
    if min(im.size) < 1000:
        print(f"  ! {origen.name}: origen chico ({im.size[0]}x{im.size[1]}), puede verse suave", file=sys.stderr)
    destino_dir.mkdir(parents=True, exist_ok=True)
    f = destino_dir / f"{nombre}.jpg"
    s = destino_dir / f"{nombre}-sm.jpg"
    full.save(f, "JPEG", quality=90, optimize=True, progressive=True)
    full.resize(SM, Image.LANCZOS).save(s, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  {origen.name} -> {f} (+ -sm)")


def paginas_pdf(pdf, tmp, seleccion):
    # 200 dpi: una página de 810x1012 pt da ~2250 px, suficiente para 1620.
    subprocess.run(["pdftoppm", "-r", "200", "-png", str(pdf), str(tmp / "p")], check=True)
    pags = sorted(tmp.glob("p-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    if seleccion:
        pags = [pags[i - 1] for i in seleccion]
    return pags


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modo", choices=["pdf", "img"])
    ap.add_argument("entradas", nargs="+")
    ap.add_argument("--salida")
    ap.add_argument("--desde", type=int, default=1, help="número del primer slide (default 1)")
    ap.add_argument("--nombre", help="nombre fijo (solo con una imagen), ej. kalu")
    ap.add_argument("--paginas", help="páginas del PDF a usar, ej. 1,3,5")
    ap.add_argument("--foco", default="0.5,0.5")
    ap.add_argument("--contener", action="store_true")
    ap.add_argument("--fondo")
    a = ap.parse_args()

    foco = tuple(float(v) for v in a.foco.split(","))
    with tempfile.TemporaryDirectory() as t:
        if a.modo == "pdf":
            if len(a.entradas) != 2 and not a.salida:
                ap.error("pdf: usa  pdf ARCHIVO.pdf DESTINO")
            pdf = Path(a.entradas[0])
            destino = Path(a.salida or a.entradas[1])
            sel = [int(x) for x in a.paginas.split(",")] if a.paginas else None
            fuentes = paginas_pdf(pdf, Path(t), sel)
        else:
            if not a.salida:
                ap.error("img: falta --salida")
            destino = Path(a.salida)
            fuentes = [Path(p) for p in a.entradas]
        if a.nombre and len(fuentes) != 1:
            ap.error("--nombre solo funciona con una imagen")
        for i, src in enumerate(fuentes):
            nombre = a.nombre or f"slide-{a.desde + i}"
            if not a.nombre and (destino / f"{nombre}.jpg").exists():
                print(f"  ~ sobrescribiendo {destino / nombre}.jpg", file=sys.stderr)
            procesar(src, destino, nombre, foco, a.contener, a.fondo)


if __name__ == "__main__":
    main()
