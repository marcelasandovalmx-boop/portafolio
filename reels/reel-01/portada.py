# Portada del reel 01: papel, March recortada, barra y palabra clave grande (legible en miniatura)
import sys; sys.argv = ['x']
import av, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W_, H_, X0, MAXW = 1080, 1920, 64, 812
PAPEL, GRIS, NARANJA = (244, 241, 235), (84, 84, 84), (229, 80, 28)
BARRA = [((229, 80, 28), 48), ((242, 116, 5), 15.5), ((50, 166, 166), 27.4), ((153, 233, 242), 6.8)]
R = '/root/reels/proyecto/2-recorte'
def frame(path, n, fmt):
    for i, f in enumerate(av.open(path).decode(video=0)):
        if i == n: return Image.fromarray(f.to_ndarray(format=fmt))
fr, al = frame(f'{R}/dr0.4-frente.mp4', 60, 'rgb24'), frame(f'{R}/dr0.4-alfa.mkv', 60, 'gray')
chico = al.resize((W_ // 4, H_ // 4)).point(lambda v: 255 if v > 140 else 0)
al = ImageChops.multiply(al, chico.filter(ImageFilter.MaxFilter(11)).resize((W_, H_)).filter(ImageFilter.GaussianBlur(10)))
def fuente(s, w): f = ImageFont.truetype('/root/reels/fuentes/Montserrat.ttf', s); f.set_variation_by_axes([w]); return f
def largo(t, f, tr): return f.getlength(t) + tr * (len(t) - 1)
def dibuja(d, x, y, t, f, tr, c):
    for i, ch in enumerate(t): d.text((x + f.getlength(t[:i]) + tr * i, y), ch, font=f, fill=c)
img = Image.new('RGBA', (W_, H_), PAPEL + (255,))
p = fr.convert('RGBA'); p.putalpha(al); img.alpha_composite(p, (0, 520))
d = ImageDraw.Draw(img); x = X0
for col, pct in BARRA: w = 600 * pct / 97.7; d.rectangle([x, 300, x + w - 1, 309], fill=col); x += w
f1 = fuente(64, 700); dibuja(d, X0, 344, 'No quieres que todo el mundo te', f1, -0.64, GRIS) if largo('No quieres que todo el mundo te', f1, -.64) <= MAXW else None
if largo('No quieres que todo el mundo te', f1, -.64) > MAXW:
    dibuja(d, X0, 344, 'No quieres que', f1, -.64, GRIS); dibuja(d, X0, 414, 'todo el mundo te', f1, -.64, GRIS); yk = 490
else: yk = 420
t = 'recomiende.'; s = 220
while largo(t, fuente(s, 800), -.02 * s) > MAXW: s -= 2
dibuja(d, X0, yk, t, fuente(s, 800), -.02 * s, NARANJA)
img.convert('RGB').save('reel-01-portada.png'); print('palabra clave a', s, 'px')
