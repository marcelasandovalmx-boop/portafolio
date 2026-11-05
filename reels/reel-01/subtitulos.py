# Pasada 3 · Subtítulos Orangy (capa RGBA aparte) — sigue reels/Reglas-de-estilo.md
import json, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS, W_, H_ = 30, 1080, 1920
X0, MAXW = 64, 812                 # margen izquierdo y ancho útil (zona segura)
Y_APOYO, Y_CLAVE = 1250, 1330      # tops de la línea de apoyo y de la palabra clave
PAPEL, SOMBRA, NARANJA = (244, 241, 235), (61, 61, 61), (229, 80, 28)
FONT = '/root/reels/fuentes/Montserrat.ttf'
MIN_DUR, ENTRADA, DESPL = 0.4, 0.2, 12

W = json.load(open('../1-corte/words.json'))
claves = {k['i'] for k in json.load(open('claves.json'))}
DUR = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                     '../1-corte/corte.mp4']))

def fuente(size, peso):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([peso]); return f

def limpia(t):                      # sin comas ni puntos finales; se conservan ¿? y acentos
    return re.sub(r'[.,;:…]+$', '', t)

def largo(texto, f, track):
    return f.getlength(texto) + track * max(len(texto) - 1, 0)

def dibuja(d, xy, texto, f, track, color):   # tracking manteniendo el kerning
    x, y = xy
    for i, ch in enumerate(texto):
        d.text((x + f.getlength(texto[:i]) + track * i, y), ch, font=f, fill=color)

# ---------- bloques de 1–3 palabras; la clave cierra su bloque ----------
bloques, cur = [], []
def cierra():
    global cur
    if cur: bloques.append({'w': cur, 'clave': None}); cur = []
for i, w in enumerate(W):
    if i in claves:
        prev = cur[-2:]; cur = cur[:-2]; cierra()
        bloques.append({'w': prev + [i], 'clave': i}); continue
    cur.append(i)
    if len(cur) == 3 or re.search(r'[.,?!]$', w['word']): cierra()
cierra()

# ---------- bloques demasiado rápidos (<0.4 s naturales) se juntan si caben en 3 palabras ----------
def natural(n):
    sig = W[bloques[n + 1]['w'][0]]['start'] if n + 1 < len(bloques) else DUR
    return sig - W[bloques[n]['w'][0]]['start']
cambio = True
while cambio:
    cambio = False
    for n in range(len(bloques) - 1):
        a, b = bloques[n], bloques[n + 1]
        if natural(n) < MIN_DUR and len(a['w']) + len(b['w']) <= 3 and not (a['clave'] is not None and b['clave'] is not None) \
           and (a['clave'] is None or a['clave'] == a['w'][-1] and False or a['clave'] is None):
            bloques[n:n + 2] = [{'w': a['w'] + b['w'], 'clave': b['clave']}]; cambio = True; break
        if n and natural(n) < MIN_DUR and len(bloques[n - 1]['w']) + len(a['w']) <= 3 and bloques[n - 1]['clave'] is None:
            p_ = bloques[n - 1]; bloques[n - 1:n + 1] = [{'w': p_['w'] + a['w'], 'clave': a['clave']}]; cambio = True; break

# ---------- tiempos: entra con su primera palabra, mínimo 0.4 s ----------
retraso = 0
for n, b in enumerate(bloques):
    ini = W[b['w'][0]]['start']
    if n and ini < bloques[n - 1]['fin']: retraso = max(retraso, bloques[n - 1]['fin'] - ini); ini = bloques[n - 1]['fin']
    b['ini'] = ini
    sig = W[bloques[n + 1]['w'][0]]['start'] if n + 1 < len(bloques) else DUR
    fin_voz = W[b['w'][-1]]['end']
    b['fin'] = max(ini + MIN_DUR, sig if sig - fin_voz <= 0.6 else fin_voz + 0.3)
    b['fin'] = min(b['fin'], DUR)
print(f'{len(bloques)} bloques · retraso máx. por mínimo de 0.4 s: {retraso:.2f} s')

# ---------- layout de cada bloque ----------
f_apoyo = fuente(64, 600)
def layout(b):
    apoyo = [i for i in b['w'] if i != b['clave']]
    piezas = []                       # (i_palabra, x, y, texto, fuente, track, color)
    x = X0; sp = f_apoyo.getlength(' ')
    for i in apoyo:
        t = limpia(W[i]['word']); piezas.append((i, x, Y_APOYO, t, f_apoyo, -0.64, PAPEL)); x += largo(t, f_apoyo, -0.64) + sp
    if b['clave'] is not None:
        t = limpia(W[b['clave']]['word']); y = Y_CLAVE if apoyo else Y_APOYO
        size = 150; f = fuente(size, 800)
        while largo(t, f, -0.02 * size) > MAXW and size > 115: size -= 1; f = fuente(size, 800)
        if largo(t, f, -0.02 * size) > MAXW:          # se parte con guion a 150 px
            f = fuente(150, 800)
            SILABAS = {'contraproducente': 6}      # contra- / producente
            corte = SILABAS.get(t.lower(), len(t) // 2)
            for k, (parte, yy) in enumerate([(t[:corte] + '-', y), (t[corte:], y + 150)]):
                piezas.append((b['clave'], X0, yy, parte, f, -3, NARANJA))
        else:
            piezas.append((b['clave'], X0, y, t, f, -0.02 * size, NARANJA))
    b['piezas'] = piezas
for b in bloques: layout(b)

# ---------- curva cubic-bezier(.16,1,.3,1) ----------
def bezier(t, p1=(.16, 1), p2=(.3, 1)):
    lo, hi = 0.0, 1.0
    for _ in range(30):
        u = (lo + hi) / 2
        x = 3 * (1 - u) ** 2 * u * p1[0] + 3 * (1 - u) * u ** 2 * p2[0] + u ** 3
        lo, hi = (u, hi) if x < t else (lo, u)
    return 3 * (1 - u) ** 2 * u * p1[1] + 3 * (1 - u) * u ** 2 * p2[1] + u ** 3

# ---------- render ----------
cache = {}
def cuadro(b, visibles, prog):
    key = (id(b), visibles, round(prog, 2))
    if key in cache: return cache[key]
    txt = Image.new('RGBA', (W_, H_)); d = ImageDraw.Draw(txt)
    dy = round(DESPL * (1 - prog))
    for (i, x, y, t, f, tr, col) in b['piezas']:
        if i in visibles: dibuja(d, (x, y + dy), t, f, tr, col + (255,))
    a = txt.getchannel('A')
    sombra = Image.new('RGBA', (W_, H_), SOMBRA + (0,))
    sombra.putalpha(a.point(lambda v: int(v * .45)).filter(ImageFilter.GaussianBlur(12)))
    capa = Image.new('RGBA', (W_, H_)); capa.alpha_composite(sombra, (0, 4)); capa.alpha_composite(txt)
    if prog < 1: capa.putalpha(capa.getchannel('A').point(lambda v: int(v * prog)))
    cache.clear() if len(cache) > 64 else None
    cache[key] = capa.tobytes(); return cache[key]

vacio = bytes(W_ * H_ * 4)
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W_}x{H_}', '-r', str(FPS),
                       '-i', '-', '-c:v', 'qtrle', 'subtitulos.mov'], stdin=subprocess.PIPE)
n_fr = round(DUR * FPS); k = 0
for fr in range(n_fr):
    t = fr / FPS
    while k < len(bloques) and t >= bloques[k]['fin']: k += 1
    b = bloques[k] if k < len(bloques) and t >= bloques[k]['ini'] else None
    if not b: ff.stdin.write(vacio); continue
    vis = tuple(i for i in b['w'] if W[i]['start'] <= t or i == b['w'][0])
    prog = bezier(min(1, (t - b['ini']) / ENTRADA))
    ff.stdin.write(cuadro(b, vis, prog))
ff.stdin.close(); ff.wait()
json.dump([{'ini': round(b['ini'], 3), 'fin': round(b['fin'], 3), 'texto': ' '.join(W[i]['word'] for i in b['w']),
            'clave': W[b['clave']]['word'] if b['clave'] is not None else None} for b in bloques],
          open('bloques.json', 'w'), ensure_ascii=False, indent=1)
print('cortos (<0.4 s):', sum(1 for b in bloques if b['fin'] - b['ini'] < MIN_DUR - 1e-6))
