# Pasada 4B · Motion graphics Orangy — compone corte + recorte + subtítulos + escenas del plan aprobado
# Sigue reels/Reglas-de-estilo.md y reels/reel-01/plan-graficos-4A.md
import json, os, re, subprocess, sys
import av, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FPS, W_, H_ = 30, 1080, 1920
X0, MAXW = 64, 812
PAPEL, GRIS, NARANJA, HAIR = (244, 241, 235), (84, 84, 84), (229, 80, 28), (227, 222, 213)
BARRA = [((229, 80, 28), 48), ((242, 116, 5), 15.5), ((50, 166, 166), 27.4), ((153, 233, 242), 6.8)]
FONT = '/root/reels/fuentes/Montserrat.ttf'
LOGO = '/home/user/portafolio/img/logo-orangy.png'
P = '/root/reels/proyecto'
CORTE = os.environ.get('CORTE', f'{P}/1-corte/corte.mp4')
FRENTE = os.environ.get('FRENTE', f'{P}/2-recorte/completo-frente.mp4'); ALFA = os.environ.get('ALFA', f'{P}/2-recorte/completo-alfa.mkv')
SUB_R, SUB_P = f'{P}/3-subtitulos/subtitulos.mov', f'{P}/3-subtitulos/subtitulos-papel.mov'
DESDE, HASTA = float(os.environ.get('DESDE', 0)), float(os.environ.get('HASTA', 1e9))
SALIDA = os.environ.get('SALIDA', 'graficos.mp4')

W = json.load(open(f'{P}/1-corte/words.json'))
DUR = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', CORTE]))
COLA = 2.0                                   # cierre agregado al final
norm = lambda s: re.sub(r'[^\wáéíóúñü]', '', s.lower())
def palabra(txt, cerca):                     # tiempo (inicio, fin) de una palabra cercana a `cerca`
    c = [w for w in W if norm(w['word']) == norm(txt) and abs(w['start'] - cerca) < 4]
    w = min(c, key=lambda w: abs(w['start'] - cerca)); return w['start'], w['end']

def fuente(size, peso):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([peso]); return f
def largo(t, f, tr): return f.getlength(t) + tr * max(len(t) - 1, 0)
def dibuja(d, x, y, t, f, tr, col):
    for i, ch in enumerate(t): d.text((x + f.getlength(t[:i]) + tr * i, y), ch, font=f, fill=col)
def bezier(t, p1=(.16, 1), p2=(.3, 1)):
    t = min(max(t, 0), 1); lo, hi = 0.0, 1.0
    for _ in range(25):
        u = (lo + hi) / 2; x = 3*(1-u)**2*u*p1[0] + 3*(1-u)*u**2*p2[0] + u**3
        lo, hi = (u, hi) if x < t else (lo, u)
    return 3*(1-u)**2*u*p1[1] + 3*(1-u)*u**2*p2[1] + u**3
def back(x, c1=1.70158):
    x = min(max(x, 0), 1); c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
SOMBRA_C = (61, 61, 61)
def suave(t): t = min(max(t, 0), 1); return t * t * (3 - 2 * t)

# ---------- piezas gráficas ----------
def barra(img, x, y, ancho, alto, t0, t):    # cada segmento 1.0 s, desfase 0.12 s
    d = ImageDraw.Draw(img); x_ = x
    for k, (col, pct) in enumerate(BARRA):
        seg = ancho * pct / 97.7; p = bezier((t - t0 - .12 * k) / 1.0)
        if seg * p >= 1: d.rectangle([x_, y, x_ + seg * p - 1, y + alto - 1], fill=col)
        x_ += seg

def titulo(lineas, size, y, t0, t, img, palabra_naranja=None):
    """Líneas Montserrat 800; entran escalonadas (24 px, 0.3 s). palabra_naranja: texto exacto a pintar en naranja."""
    f = fuente(size, 800); tr = -0.02 * size; lh = round(size * 1.02)
    for k, ln in enumerate(lineas):
        p = bezier((t - t0 - .06 * k) / .3)
        if p <= 0: continue
        capa = Image.new('RGBA', (W_, H_)); d = ImageDraw.Draw(capa)
        yy = y + k * lh + round(24 * (1 - p)); x = X0
        for w in ln.split(' '):
            col = NARANJA if palabra_naranja and norm(w) in palabra_naranja else GRIS
            dibuja(d, x, yy, w, f, tr, col); x += largo(w + ' ', f, tr)
        if p < 1: capa.putalpha(capa.getchannel('A').point(lambda v: int(v * p)))
        img.alpha_composite(capa)

def ajusta(texto, size_max, maxw=MAXW, max_lineas=4):
    for size in range(size_max, 60, -2):
        f = fuente(size, 800); tr = -0.02 * size; lineas, cur = [], ''
        for w in texto.split(' '):
            prueba = (cur + ' ' + w).strip()
            if largo(prueba, f, tr) <= maxw: cur = prueba
            else: lineas.append(cur); cur = w
        lineas.append(cur)
        if len(lineas) <= max_lineas and all(largo(l, f, tr) <= maxw for l in lineas): return lineas, size
    raise ValueError(texto)

# ---------- línea de tiempo del plan aprobado ----------
a_alto = palabra('Alto', 80); a_det = palabra('detente', 81)
t_rep = palabra('No', 21.1); t_rep_fin = palabra('recomiende', 23)[1]
t_gust = palabra('Te', 100.3); t_gust_fin = palabra('recomiende', 101.3)[1]
t_pien = palabra('Piensa', 177.3); t_pien_fin = palabra('ellos', 179.2)[1]
t_pel = palabra('peligroso', 50.2)[0]; t_prec = palabra('precio', 58.5)
t_nopas = palabra('No', 117.2)[0]; t_simil_fin = palabra('ellos', 130.6)[1]
t_lam = palabra('lamento', 147.0)[0]; t_tien_fin = palabra('tienes', 151.0)[1]
LISTA_INI = palabra('Te', 58.5)[0]
LISTA = [('Bajarte el precio', palabra('precio', 60.4)[0]), ('Concesiones especiales', palabra('concesiones', 62.1)[0]),
         ('Urgencia', palabra('urgencia', 66.1)[0]), ('Un poquito más', palabra('poquito', 67.3)[0])]
LISTA_FIN = palabra('Y', 70.0)[0]

ESC = [  # (inicio, fin, tipo, datos)
    (0.0, 3.0, 'gancho', None),
    (t_rep[0], t_rep_fin + .35, 'titulo', ('No quieres que todo el mundo te recomiende.', {'recomiende'})),
    (LISTA_INI, LISTA_FIN, 'lista', None),
    (t_gust[0], t_gust_fin + .35, 'titulo', ('¿Te gustaría que te recomiende?', {'recomiende'})),
    (t_pien[0], t_pien_fin + .45, 'titulo', ('No quieres más clientes como ellos.', {'como', 'ellos'})),
    (DUR, DUR + COLA, 'cierre', None),
]
FRASES = [('pero', 27.3, '¿Pero cómo, Marcela?', {'marcela'}), ('mira', 49.9, 'Mira qué peligroso es esto.', {'peligroso'}),
    ('Alto', 80.1, 'Alto ahí.', {'alto'}), ('Tú', 102.0, '¿Qué va a decir de ti?', {'decir'}), ('No', 117.2, '¿No pasará entonces…?', {'pasará'}),
    ('primer', 140, 'El primer paso.', {'primer', 'paso'}), ('algo', 160.3, 'Algo bien peligroso.', {'peligroso'}),
    ('no', 183, 'No hay una sola manera correcta.', {'correcta'})]
if os.environ.get('CORTES'):
    for w, cerca, txt, nar in FRASES:
        t0 = palabra(w, cerca)[0]
        prev_fin = max([b for a, b, k, d in ESC if a <= t0 < b] or [t0])
        ESC.append((prev_fin, prev_fin + 1.4, 'frase', (txt, nar)))
    ESC.sort(key=lambda e: e[0])
ZOOM = [(t_pel, LISTA_INI, 'seco'), (a_alto[0], a_det[1] + .25, 'seco'), (t_nopas, t_simil_fin + .2, 'lento')]
CITA = (t_lam - .15, t_tien_fin + .5, '“Lamento mucho, pero no tenemos una solución con el presupuesto que tienes.”')
json.dump({'escenas': [(a, b, k) for a, b, k, _ in ESC], 'zooms': ZOOM, 'cita': CITA[:2], 'dur': DUR + COLA}, open(os.environ.get('ESC_JSON', 'escenas.json'), 'w'), indent=1)
print('escenas:', [(round(a, 2), round(b, 2), k) for a, b, k, _ in ESC]); print('zooms:', [(round(a, 2), round(b, 2), k) for a, b, k in ZOOM])

def escena(t):
    for a, b, k, d in ESC:
        if a <= t < b: return a, b, k, d
    return None
DINAMICO = bool(os.environ.get('DINAMICO'))
CLAVES_T = [k['start'] for k in json.load(open(f'{P}/3-subtitulos/claves.json'))]
def zoom(t):
    for a, b, k in ZOOM:
        if a <= t < b: return (1.06 if DINAMICO else 1.04) if k == 'seco' else 1 + (.06 if DINAMICO else .04) * suave((t - a) / (b - a))
    if not DINAMICO: return 1.0
    if en_efecto(t): return 1.0
    # ritmo de editor: en cada palabra clave alterna plano abierto / cerrado (corte seco) + empuje lento de 1.5 %
    prev = [i for i, c in enumerate(CLAVES_T) if c <= t]
    if not prev: return 1.0 + .015 * min(1, t / 4)
    i = prev[-1]; nivel = 1.045 if i % 2 == 0 else 1.0
    return nivel + .015 * min(1, (t - CLAVES_T[i]) / 4)

CENTRO = (540, 720)
BAJA = 300                                   # en escenas papel March baja 300 px para liberar arriba                          # zoom hacia la cara
def escala(img, z):
    if z == 1: return img
    w, h = round(W_ / z), round(H_ / z); x = round(CENTRO[0] - CENTRO[0] / z); y = round(CENTRO[1] - CENTRO[1] / z)
    return img.crop((x, y, x + w, y + h)).resize((W_, H_), Image.LANCZOS)

# ---------- elementos: ícono de línea (Lucide, ISC) en tarjeta papel, disparado en su palabra ----------
ICO_DIR = '/root/reels/proyecto/7-mejoras/iconos'
ICONOS_PLAN = [('acuerdo', 9.2, 'handshake'), ('conclusión', 14.7, 'lightbulb'), ('conocen', 29.8, 'users'), ('feliz', 39.5, 'smile'),
    ('términos', 42.5, 'file-text'), ('recomendar', 47.8, 'thumbs-up'), ('peligroso', 50.2, 'triangle-alert'), ('detente', 81.0, 'hand'),
    ('cliente', 85.7, 'user-round'), ('barato', 90.6, 'tag'), ('regateó', 94.9, 'badge-percent'), ('deshoras', 98.7, 'moon'),
    ('decir', 103.3, 'message-square-quote'), ('superbarato', 107.5, 'piggy-bank'), ('ordenado', 110.7, 'folder-open'), ('gratis', 114.4, 'gift'),
    ('trabajo', 124.3, 'briefcase'), ('negocio', 138.4, 'store'), ('cotización', 143.8, 'receipt'), ('personalidad', 156.3, 'fingerprint'),
    ('costaba', 169.2, 'wallet'), ('comentarios', 181.6, 'message-circle'), ('correcta', 184.1, 'signpost')]
ICONOS = []
for w, cerca, ico in ICONOS_PLAN if os.environ.get('ICONOS') else []:
    t0 = palabra(w, cerca)[0]
    card = Image.new('RGBA', (176, 176), PAPEL + (255,)); dc = ImageDraw.Draw(card)
    dc.rectangle([0, 0, 175, 175], outline=HAIR + (255,), width=2)
    card.alpha_composite(Image.open(f'{ICO_DIR}/{ico}.png').convert('RGBA').resize((176, 176), Image.LANCZOS))
    dc.rectangle([0, 172, 175, 175], fill=NARANJA + (255,))
    ICONOS.append([t0, t0 + 1.6, card])
for a, b in zip(ICONOS, ICONOS[1:]): a[1] = min(a[1], b[0] - .05)
json.dump([a for a, b, _ in ICONOS], open(os.environ.get('ICO_JSON', 'iconos.json'), 'w'))
print('elementos:', [(round(a, 2), round(b, 2)) for a, b, _ in ICONOS])
def elemento(img, t):
    for a, b, card in ICONOS:
        if a <= t < b:
            k = (t - a) / .3; sal = 1 - suave((t - (b - .2)) / .2)
            sc = .7 + .3 * back(k) if DINAMICO else 1
            c = card.resize((max(1, round(176 * sc)), max(1, round(176 * sc))), Image.LANCZOS) if sc != 1 else card.copy()
            al_ = min(1, k * 2.5) * sal; c.putalpha(c.getchannel('A').point(lambda v: int(v * al_)))
            x = X0 + (176 - c.width) // 2; y = 250 + (176 - c.height) // 2 + (0 if DINAMICO else round(16 * (1 - bezier(k))))
            sh = Image.new('RGBA', c.size, SOMBRA_C + (0,)); sh.putalpha(c.getchannel('A').point(lambda v: int(v * .35)))
            pad = Image.new('RGBA', (c.width + 80, c.height + 80)); pad.alpha_composite(sh, (40, 40)); pad = pad.filter(ImageFilter.GaussianBlur(16))
            img.alpha_composite(pad, (x - 40, y - 40 + 8)); img.alpha_composite(c, (x, y))

# ---------- efectos con recorte: órbita de portafolio y palabra gigante detrás de March ----------
EFECTOS = bool(os.environ.get('EFECTOS'))
IMG = '/home/user/portafolio/img'
ORBITA = DETRAS = None; CARTAS = []
if EFECTOS:
    ORBITA = (palabra('todos', 29.05)[0] - .1, palabra('recomienden', 33.2)[1] + .35)
    DETRAS = []
    for w, cerca in (('contraproducente', 25.39), ('similares', 129.6), ('advertí', 201.1)):
        a, b = palabra(w, cerca); DETRAS.append((a - .1, min(b + .9, DUR - .02), limpia_txt := re.sub(r'[^\wáéíóúñü]', '', w)))
    for caso, sl in ((1, 2), (2, 2), (3, 3), (4, 2), (5, 3), (3, 1)):     # piezas reales del portafolio
        im = Image.open(f'{IMG}/caso-{caso}/slide-{sl}-sm.jpg').convert('RGB').resize((240, 300), Image.LANCZOS)
        c = Image.new('RGBA', (256, 316), PAPEL + (255,)); c.paste(im, (8, 8))
        pad = Image.new('RGBA', (336, 396)); sh = Image.new('RGBA', (256, 316), SOMBRA_C + (90,))
        pad.alpha_composite(sh, (40, 52)); pad = pad.filter(ImageFilter.GaussianBlur(14)); pad.alpha_composite(c, (40, 40))
        CARTAS.append(pad)
    print('órbita', ORBITA, '· detrás', DETRAS)

def en_efecto(t):
    if not EFECTOS: return None
    if ORBITA[0] <= t < ORBITA[1]: return 'orbita'
    for a, b, w in DETRAS:
        if a <= t < b: return ('detras', a, b, w)
    return None

def efecto(t, real, al, sub_r):
    ef = en_efecto(t); img = real.convert('RGBA')
    persona_ = real.convert('RGBA'); persona_.putalpha(limpia_mate(al))
    if ef == 'orbita':
        a, b = ORBITA; tt = t - a; ent = bezier(tt / .45); sal = 1 - suave((t - (b - .35)) / .35)
        import math
        cx, cy, rx, ry = 540, 1200, 420 * (.3 + .7 * ent) * (1 + .15 * (1 - sal)), 120
        capas = []
        for i, c in enumerate(CARTAS):
            ang = 2 * math.pi * i / len(CARTAS) + 2 * math.pi * tt / 5.0
            z = math.sin(ang); sc = 1.2 * (.62 + .38 * (z + 1) / 2) * (.6 + .4 * ent)
            cc = c.resize((round(c.width * sc), round(c.height * sc)), Image.BILINEAR).rotate(-8 * math.cos(ang), resample=Image.BICUBIC, expand=True)
            if ent * sal < 1: cc.putalpha(cc.getchannel('A').point(lambda v, k=ent * sal: int(v * k)))
            capas.append((z, cc, (round(cx + rx * math.cos(ang) - cc.width / 2), round(cy + ry * z - cc.height / 2))))
        for z, cc, pos in sorted(capas, key=lambda x: x[0]):
            if z < 0: img.alpha_composite(cc, pos)
        img.alpha_composite(persona_)
        for z, cc, pos in sorted(capas, key=lambda x: x[0]):
            if z >= 0: img.alpha_composite(cc, pos)
        return img                               # una idea: sin subtítulos durante la órbita
    _, a, b, w = ef; tt = t - a
    size = 260; f = fuente(size, 800)
    while largo(w, f, -.02 * size) > 876: size -= 4; f = fuente(size, 800)
    capa = Image.new('RGBA', (W_, H_)); dibuja(ImageDraw.Draw(capa), X0, 236, w, f, -.02 * size, GRIS + (235,))
    p = bezier(tt / .3) * (1 - suave((t - (b - .2)) / .2)); k = 1.08 - .08 * bezier(tt / .5)
    if k != 1:
        capa = capa.resize((round(W_ * k), round(H_ * k)), Image.BILINEAR).crop((round((W_ * k - W_) / 2), round(236 * (k - 1)), round((W_ * k - W_) / 2) + W_, round(236 * (k - 1)) + H_))
    capa.putalpha(capa.getchannel('A').point(lambda v: int(v * p)))
    img.alpha_composite(capa); return img           # encuadre cerrado: la palabra va al frente para que siempre se lea

logo = Image.open(LOGO).convert('RGBA'); logo = logo.resize((560, round(560 * logo.height / logo.width)), Image.LANCZOS)
f_lista, f_cita = fuente(40, 700), fuente(44, 600)

def limpia_mate(al):                     # quita restos lejanos al cuerpo (marco del cuadro): máscara dilatada ~40 px
    chico = al.resize((W_ // 4, H_ // 4)).point(lambda v: 255 if v > 140 else 0)
    zona = chico.filter(ImageFilter.MaxFilter(11)).resize((W_, H_)).filter(ImageFilter.GaussianBlur(10))
    return ImageChops.multiply(al, zona)

def persona(fr, al, s, ancla_x):             # recorte escalado, anclado abajo
    fr = fr.resize((round(W_ * s), round(H_ * s)), Image.LANCZOS); al = al.resize(fr.size, Image.LANCZOS)
    p = fr.convert('RGBA'); p.putalpha(al); return p, (ancla_x - fr.width // 2, H_ - fr.height)

def cuadro(t, real, fr, al, sub_r, sub_p):
    e = escena(t)
    if e and e[2] == 'cierre':
        return empuje(cierre(t, e), real, t - e[0])
    return cuadro_resto(t, e, real, fr, al, sub_r, sub_p)

def empuje(img, real, tt, d=.28):            # transición: la tarjeta papel sube y empuja el plano real
    if not DINAMICO or tt >= d or real is None: return img
    p = bezier(tt / d); base = Image.new('RGBA', (W_, H_)); off = round(H_ * (1 - p))
    base.alpha_composite(real.convert('RGBA'), (0, off - H_)); base.alpha_composite(img, (0, off)); return base

def cierre(t, e):
    if True:
        img = Image.new('RGBA', (W_, H_), PAPEL + (255,)); tt = t - e[0]
        p = bezier(tt / .35); lg = logo.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * p)))
        y = 820 + round(20 * (1 - p)); img.alpha_composite(lg, ((W_ - lg.width) // 2, y))
        barra(img, (W_ - 560) // 2, y + logo.height + 48, 560, 10, e[0] + .2, t)
        f = fuente(40, 600); url = 'orangy.com.mx'; d = ImageDraw.Draw(img)
        pu = bezier((tt - .5) / .35)
        if pu > 0:
            cu = Image.new('RGBA', (W_, H_)); dibuja(ImageDraw.Draw(cu), (W_ - largo(url, f, 0)) / 2, y + logo.height + 96, url, f, 0, GRIS)
            cu.putalpha(cu.getchannel('A').point(lambda v: int(v * pu))); img.alpha_composite(cu)
        return img
def blur_h(img, k):                          # desenfoque de movimiento horizontal (barato)
    if k < 2: return img
    w = max(8, img.width // k); return img.resize((w, img.height), Image.BILINEAR).resize(img.size, Image.BILINEAR)

def barrido(a, b, p):                        # a sale a la izquierda, b entra desde la derecha
    p = bezier(p); off = round(W_ * p); fuerza = round(24 * (1 - abs(2 * p - 1)) + 1)
    base = Image.new('RGBA', (W_, H_)); base.alpha_composite(blur_h(a.convert('RGBA'), fuerza), (-off, 0))
    base.alpha_composite(blur_h(b.convert('RGBA'), fuerza), (W_ - off, 0)); return base

def cuadro_resto(t, e, real, fr, al, sub_r, sub_p):
    if e and e[2] == 'frase':
        img = Image.new('RGBA', (W_, H_), PAPEL + (255,)); texto, nar = e[3]
        lineas, size = ajusta(texto, 128); alto = len(lineas) * round(size * 1.02)
        titulo(lineas, size, 880 - alto // 2, e[0] + .1, t, img, nar)
        r = escala(real, zoom(t)).convert('RGBA'); tt, rest = t - e[0], e[1] - t
        if tt < .22: return barrido(r, img, tt / .22)
        if rest < .2: return barrido(img, r, 1 - rest / .2)
        return img
    if e and e[2] == 'titulo':
        img = Image.new('RGBA', (W_, H_), PAPEL + (255,)); texto, nar = e[3]
        lineas, size = ajusta(texto, 132); alto = len(lineas) * round(size * 1.02)
        titulo(lineas, size, 880 - alto // 2, e[0] + (.12 if DINAMICO else 0), t, img, nar)
        return empuje(img, real, t - e[0])
    if e and e[2] == 'gancho':
        img = Image.new('RGBA', (W_, H_), PAPEL + (255,))
        barra(img, X0, 236, 600, 10, .2, t)
        lineas, size = ajusta('No quieres que todo el mundo te recomiende.', 96, max_lineas=3)
        titulo(lineas, size, 266, .25, t, img, {'recomiende'})
        p = fr.convert('RGBA'); p.putalpha(limpia_mate(al)); img.alpha_composite(p, (0, BAJA))   # sin escalar: sin bordes visibles
        return img                                       # una idea: el título; sin subtítulos
    if e and e[2] == 'lista':
        img = Image.new('RGBA', (W_, H_), PAPEL + (255,))
        p = fr.convert('RGBA'); p.putalpha(limpia_mate(al)); img.alpha_composite(p, (0, BAJA + 60))
        y = 236
        for k, (txt, t0) in enumerate(LISTA):
            pr = bezier((t - t0) / .3)
            if pr <= 0: continue
            capa = Image.new('RGBA', (W_, H_)); dc = ImageDraw.Draw(capa); yy = y + k * 56 + round(24 * (1 - pr))
            dc.rectangle([X0, yy + 21, X0 + 20, yy + 25], fill=NARANJA + (255,))     # guion naranja, acento mínimo
            dibuja(dc, X0 + 44, yy, txt, f_lista, -0.5, GRIS + (255,))
            if pr < 1: capa.putalpha(capa.getchannel('A').point(lambda v: int(v * pr)))
            img.alpha_composite(capa)
        return img                                       # la lista dice lo mismo: sin subtítulos aquí
    # fondo real (con zoom si toca) + subtítulos + cita
    if en_efecto(t) and al is not None: img = efecto(t, real, al, sub_r); elemento(img, t); return img
    img = escala(real, zoom(t)).convert('RGBA'); img.alpha_composite(sub_r); elemento(img, t)
    if CITA[0] <= t < CITA[1]:
        pr = bezier((t - CITA[0]) / .3) * (1 - bezier((t - CITA[1] + .2) / .2))
        capa = Image.new('RGBA', (W_, H_)); dc = ImageDraw.Draw(capa)
        palabras, lineas, cur = CITA[2].split(' '), [], ''
        for w in palabras:
            pr_ = (cur + ' ' + w).strip()
            if largo(pr_, f_cita, 0) <= MAXW - 64: cur = pr_
            else: lineas.append(cur); cur = w
        lineas.append(cur); alto = len(lineas) * 56 + 56; y = 236 + round(16 * (1 - pr))
        dc.rectangle([X0, y, X0 + MAXW, y + alto], fill=PAPEL + (255,), outline=HAIR + (255,), width=2)
        for j, ln in enumerate(lineas): dibuja(dc, X0 + 32, y + 28 + j * 56, ln, f_cita, 0, GRIS + (255,))
        capa.putalpha(capa.getchannel('A').point(lambda v: int(v * pr))); img.alpha_composite(capa)
    return img

# ---------- lectura sincronizada y salida ----------
def lector(path, fmt):
    c = av.open(path)
    for f in c.decode(video=0): yield f.to_image() if fmt == 'rgb' else Image.fromarray(f.to_ndarray(format=fmt))
# el recorte solo existe en los tramos sobre papel (gancho y lista): se lee por tramo, sincronizado por tiempo
R = f'{P}/2-recorte'
SUF = os.environ.get('SUF_FRENTE', '')      # '-grade' = recorte con la corrección de luz
TRAMOS_EF = [(23.9, 'seg-contra'), (27.9, 'seg-orbita'), (128.4, 'seg-simil'), (199.9, 'seg-advert')]
TRAMOS = [(0.0, f'{R}/dr0.4-frente{SUF}.mp4', f'{R}/dr0.4-alfa.mkv'), (56.5, f'{R}/seg-lista-frente{SUF}.mp4', f'{R}/seg-lista-alfa.mkv')]
if EFECTOS: TRAMOS += [(a, f'{R}/{n}-frente.mp4', f'{R}/{n}-alfa.mkv') for a, n in TRAMOS_EF]
class Mate:
    def __init__(s): s.act = None
    def get(s, t):
        ini, fp, ap = max((x for x in TRAMOS if x[0] <= t + 1e-6), key=lambda x: x[0])
        if s.act is None or s.act[0] != ini: s.act = [ini, lector(fp, 'rgb'), lector(ap, 'gray'), -1, None]
        n = round((t - ini) * FPS)
        while s.act[3] < n:
            try: s.act[4] = (next(s.act[1]), next(s.act[2])); s.act[3] += 1
            except StopIteration: break
        return s.act[4]
mate = Mate()
src = [lector(CORTE, 'rgb'), lector(SUB_R, 'rgba'), lector(SUB_P, 'rgba')]
n_tot = round((DUR + COLA) * FPS); n_ini = round(DESDE * FPS); n_fin = min(n_tot, round(HASTA * FPS))
dur_out = (n_fin - n_ini) / FPS
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W_}x{H_}', '-r', str(FPS), '-i', '-',
    '-ss', str(DESDE), '-i', CORTE, '-filter_complex', f'[1:a]apad,atrim=0:{dur_out:.3f}[a]', '-map', '0:v', '-map', '[a]',
    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', SALIDA], stdin=subprocess.PIPE)
ultimo = None
for n in range(n_fin):
    t = n / FPS
    if t < DUR:
        try: ultimo = [next(g) for g in src]
        except StopIteration: pass
    if n < n_ini: continue
    e = escena(t); fr, al = mate.get(t) if (e and e[2] in ('gancho', 'lista')) or (not e and en_efecto(t)) else (None, None)
    real, sub_r, sub_p = ultimo
    ff.stdin.write(cuadro(t, real, fr, al, sub_r, sub_p).convert('RGB').tobytes())
    if n % 300 == 0: print(f'{t:6.1f} s', flush=True)
ff.stdin.close(); ff.wait(); print('listo', SALIDA)
