# Portada tipográfica del reel 01 — Orangy: papel, Montserrat, barra, contraste de escala, un acento naranja
from PIL import Image, ImageDraw, ImageFont
W_, H_, X0, ANCHO = 1080, 1920, 96, 888
PAPEL, GRIS, NARANJA = (244, 241, 235), (84, 84, 84), (229, 80, 28)
BARRA = [((229, 80, 28), 48), ((242, 116, 5), 15.5), ((50, 166, 166), 27.4), ((153, 233, 242), 6.8)]
def fuente(s, w): f = ImageFont.truetype('/root/reels/fuentes/Montserrat.ttf', s); f.set_variation_by_axes([w]); return f
def largo(t, f, tr): return f.getlength(t) + tr * (len(t) - 1)
def dibuja(d, x, y, t, f, tr, c):
    for i, ch in enumerate(t): d.text((x + f.getlength(t[:i]) + tr * i, y), ch, font=f, fill=c)
def ajusta(t, peso, maxs=600):
    s = maxs
    while largo(t, fuente(s, peso), -.03 * s) > ANCHO: s -= 2
    return s
img = Image.new('RGB', (W_, H_), PAPEL); d = ImageDraw.Draw(img)
lineas = [('No quieres que', 600, GRIS, 70), ('todo el', 800, GRIS, None), ('mundo te', 800, GRIS, None), ('recomiende.', 800, NARANJA, None)]
bloques = []
for t, w, c, s in lineas:
    s = s or ajusta(t, w); f = fuente(s, w); bb = f.getbbox(t); bloques.append((t, f, s, c, bb))
alto = sum(bb[3] - bb[1] for *_, bb in bloques) + 34 * (len(bloques) - 1)
y = 960 - alto // 2 + 40                       # centrado óptico dentro del recorte 3:4 (y 240–1680)
x = X0
for col, pct in BARRA: w = 600 * pct / 97.7; d.rectangle([x, y - 110, x + w - 1, y - 99], fill=col); x += w
for t, f, s, c, bb in bloques:
    dibuja(d, X0, y - bb[1], t, f, -.03 * s if s > 100 else -.01 * s, c); y += bb[3] - bb[1] + 34
logo = Image.open('/home/user/portafolio/img/logo-orangy.png').convert('RGBA'); logo = logo.resize((300, round(300 * logo.height / logo.width)), Image.LANCZOS)
img.paste(logo, (X0, 1560 - logo.height), logo)
img.save('reel-01-portada-tipografica.png'); print([(t, s) for t, f, s, c, bb in bloques])
