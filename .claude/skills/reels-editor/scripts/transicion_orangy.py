"""Transición de marca Orangy: «la barra que se abre».
La barra segmentada de Orangy (firma visual de March) se dibuja de izquierda a derecha, se abre como telón hasta
cubrir la pantalla, y se cierra hacia abajo dejando ver el plano siguiente; termina un instante como barra al pie.

Uso:  python3 transicion_orangy.py <carpeta_salida> [ancho alto]
Genera t_00.png … t_17.png (RGBA) e imprime el cuadro de corte. El corte entre planos va en el cuadro CORTE (pantalla
llena): en ffmpeg, la secuencia entra con `-framerate 30 -i carpeta/t_%02d.png`, se retrasa con
`setpts=PTS+(t_corte - CORTE/30)/TB` y se superpone con `overlay=eof_action=pass`.
"""
import sys, os
from PIL import Image, ImageDraw

SEG = [("#E5501C", 0.48), ("#F27405", 0.155), ("#32A6A6", 0.274), ("#99E9F2", 0.091)]   # proporciones reales del brochure
N, CORTE = 18, 8
GROSOR = 0.0115   # alto de la barra en reposo, como fracción del alto

def ease_out(x): return 1 - (1 - x) ** 3
def ease_in_out(x): return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

def frame(f, W, H):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    g = max(6, round(H * GROSOR)); cy = H // 2
    alpha, x_max = 255, W
    if f <= 2:                                   # 1) la barra se dibuja de izquierda a derecha
        y0, y1 = cy - g // 2, cy + g // 2; x_max = round(W * ease_out((f + 1) / 3))
    elif f <= 7:                                 # 2) se abre como telón
        h = g + (H - g) * ease_out((f - 2) / 5); y0, y1 = round(cy - h / 2), round(cy + h / 2)
    elif f <= 9:                                 # 3) pantalla llena: aquí va el corte
        y0, y1 = 0, H
    elif f <= 15:                                # 4) se cierra hacia abajo y queda como barra al pie
        y0, y1 = round((H - g) * ease_in_out((f - 9) / 6)), H
    else:                                        # 5) la barra del pie se desvanece
        y0, y1 = H - g, H; alpha = 150 if f == 16 else 60
    x = 0.0
    for col, p in SEG:
        x1 = x + p * W
        a, b = round(x), min(round(x1), x_max)
        if b > a:
            r, gg, bb = (int(col[i:i + 2], 16) for i in (1, 3, 5))
            d.rectangle((a, max(0, y0), b, min(H, y1)), fill=(r, gg, bb, alpha))
        x = x1
    return im

if __name__ == "__main__":
    out = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 1080; H = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
    os.makedirs(out, exist_ok=True)
    for f in range(N): frame(f, W, H).save(os.path.join(out, f"t_{f:02d}.png"))
    print("cuadros", N, "corte en el cuadro", CORTE, "duración", round(N / 30, 2), "s")
