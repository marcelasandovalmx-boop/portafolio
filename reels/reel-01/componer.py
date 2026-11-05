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
CORTE = f'{P}/1-corte/corte.mp4'
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
ZOOM = [(t_pel, LISTA_INI, 'seco'), (a_alto[0], a_det[1] + .25, 'seco'), (t_nopas, t_simil_fin + .2, 'lento')]
CITA = (t_lam - .15, t_tien_fin + .5, '“Lamento mucho, pero no tenemos una solución con el presupuesto que tienes.”')
json.dump({'escenas': [(a, b, k) for a, b, k, _ in ESC], 'zooms': ZOOM, 'cita': CITA[:2], 'dur': DUR + COLA}, open('escenas.json', 'w'), indent=1)
print('escenas:', [(round(a, 2), round(b, 2), k) for a, b, k, _ in ESC]); print('zooms:', [(round(a, 2), round(b, 2), k) for a, b, k in ZOOM])

def escena(t):
    for a, b, k, d in ESC:
        if a <= t < b: return a, b, k, d
    return None
def zoom(t):
    for a, b, k in ZOOM:
        if a <= t < b: return 1.04 if k == 'seco' else 1 + .04 * suave((t - a) / (b - a))
    return 1.0

CENTRO = (540, 720)
BAJA = 300                                   # en escenas papel March baja 300 px para liberar arriba                          # zoom hacia la cara
def escala(img, z):
    if z == 1: return img
    w, h = round(W_ / z), round(H_ / z); x = round(CENTRO[0] - CENTRO[0] / z); y = round(CENTRO[1] - CENTRO[1] / z)
    return img.crop((x, y, x + w, y + h)).resize((W_, H_), Image.LANCZOS)

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
    if e and e[2] == 'titulo':
        img = Image.new('RGBA', (W_, H_), PAPEL + (255,)); texto, nar = e[3]
        lineas, size = ajusta(texto, 132); alto = len(lineas) * round(size * 1.02)
        titulo(lineas, size, 880 - alto // 2, e[0], t, img, nar); return img
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
    img = escala(real, zoom(t)).convert('RGBA'); img.alpha_composite(sub_r)
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
TRAMOS = [(0.0, f'{R}/dr0.4-frente.mp4', f'{R}/dr0.4-alfa.mkv'), (56.5, f'{R}/seg-lista-frente.mp4', f'{R}/seg-lista-alfa.mkv')]
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
    e = escena(t); fr, al = mate.get(t) if e and e[2] in ('gancho', 'lista') else (None, None)
    real, sub_r, sub_p = ultimo
    ff.stdin.write(cuadro(t, real, fr, al, sub_r, sub_p).convert('RGB').tobytes())
    if n % 300 == 0: print(f'{t:6.1f} s', flush=True)
ff.stdin.close(); ff.wait(); print('listo', SALIDA)
