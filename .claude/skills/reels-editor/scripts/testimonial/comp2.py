# Compositor v2 del reel de Mario: fundidos de corte suave, contorno en preguntas, placa centrada,
# captions karaoke y BLOQUES de palabra clave con letras que entran en fila de derecha a izquierda.
# uso: /usr/bin/python3 comp2.py [t_ini t_fin salida]    → también escribe eventos.json para los efectos de sonido
import json, subprocess, sys, os, re, unicodedata
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import onnxruntime as ort

W, H, FPS = 1080, 1920, 30
MONT = '/root/.fonts/montserrat/Montserrat-%s.ttf'
ANCHA = os.environ.get('FUENTE_NOMBRE', 'fonts/Unbounded.ttf')   # sustituto de Horizon; cambiar por el OTF cuando llegue
def f_ancha(px):
    f = ImageFont.truetype(ANCHA, px)
    try: f.set_variation_by_axes([900])
    except Exception: pass
    return f
NAR = (229, 80, 28); NAR_SUAVE = (245, 176, 150); BLANCO = (255, 255, 255)

edl = json.load(open('edl.json')); caps = json.load(open('captions.json')); words = json.load(open('cut-words.json'))
segs = edl['segs']; DUR = edl['dur']; PREG = edl['preg']
NF = round(DUR * FPS)
seg_start = {round(s['t'] * FPS): s for s in segs}

t0, t1, salida = 0.0, DUR, 'out2_v.mp4'
if len(sys.argv) >= 4: t0, t1, salida = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
f0, f1 = round(t0 * FPS), min(NF, round(t1 * FPS))

ease = lambda p: 1 - (1 - min(1.0, max(0.0, p))) ** 3

# ───────── Letras que navegan ─────────
def letras(d, txt, font, x, yc, u, fill, paso=0.028, dur=0.24, viaje=230, S=1, k0=0):
    """Dibuja txt letra por letra; cada letra entra desde la derecha con retraso creciente. Devuelve cuántas letras ya entraron."""
    n = 0
    for k, ch in enumerate(txt):
        if ch == ' ': continue
        p = (u - paso * (k + k0)) / dur
        if p <= 0: continue
        e = ease(p)
        xx = x + font.getlength(txt[:k]) + (1 - e) * viaje * S
        d.text((xx, yc), ch, font=font, fill=fill + (int(255 * min(1, p * 2.2)),), anchor='ls')
        n += 1
    return n

# ───────── Placa de nombre (centrada) ─────────
P_IN, P_OUT = 0.95, 6.6
NOMBRE, ROL = 'MARIO BARRERA', 'Aliado estratégico'
PL_CY = 868          # centro vertical de la caja del nombre
def placa(t):
    u = t - P_IN; S = 2
    fn = f_ancha(60 * S); fr = ImageFont.truetype(MONT % 'Bold', 46 * S)
    tn = fn.getlength(NOMBRE); tr = fr.getlength(ROL)
    bw, bh = int(tn / S + 84), 116
    rw, rh = bw + 36, 98
    cw, chh = rw + 40, bh + rh + 20
    im = Image.new('RGBA', (cw * S, chh * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = cw * S / 2
    # pleca del cargo: se abre desde el centro
    if u >= 0.62:
        e = ease((u - 0.62) / 0.26); half = rw * S / 2 * e
        y_a = (bh - 8) * S
        d.rounded_rectangle([cx - half, y_a, cx + half, y_a + rh * S], radius=10 * S, fill=NAR + (255,))
        if u >= 0.80:
            q = ease((u - 0.80) / 0.25)
            tmp = Image.new('RGBA', im.size, (0, 0, 0, 0))
            ImageDraw.Draw(tmp).text((cx, y_a + rh * S / 2 + 3 * S + (1 - q) * 22 * S), ROL, font=fr, fill=BLANCO + (int(255 * q),), anchor='mm')
            msk = Image.new('L', im.size, 0); ImageDraw.Draw(msk).rectangle([cx - half, y_a, cx + half, y_a + rh * S], fill=255)
            im.alpha_composite(Image.composite(tmp, Image.new('RGBA', im.size, (0, 0, 0, 0)), msk))
            d = ImageDraw.Draw(im)
    # caja blanca del nombre
    x_b = cx - bw * S / 2
    d.rounded_rectangle([x_b, 0, x_b + bw * S, bh * S], radius=18 * S, fill=BLANCO + (255,))
    tmp = Image.new('RGBA', im.size, (0, 0, 0, 0))
    asc = fn.getbbox('M')
    base = bh * S / 2 + (asc[3] - asc[1]) / 2
    letras(ImageDraw.Draw(tmp), NOMBRE, fn, cx - tn / 2, base, u - 0.10, NAR, S=S)
    msk = Image.new('L', im.size, 0); ImageDraw.Draw(msk).rounded_rectangle([x_b, 0, x_b + bw * S, bh * S], radius=18 * S, fill=255)
    im.alpha_composite(Image.composite(tmp, Image.new('RGBA', im.size, (0, 0, 0, 0)), msk))
    im = im.resize((cw, chh), Image.LANCZOS)
    a, sc = 1.0, 1.0
    if u < 0.16: sc = 0.8 + 0.25 * (u / 0.11) if u < 0.11 else 1.05 - 0.05 * ((u - 0.11) / 0.05); a = min(1, u / 0.07)
    if t > P_OUT - 0.22: a = max(0, (P_OUT - t) / 0.22); sc = 1 - 0.04 * (1 - a)
    if sc != 1.0: im = im.resize((max(2, int(cw * sc)), max(2, int(chh * sc))), Image.LANCZOS)
    if a < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    return im, (W // 2 - im.width // 2, PL_CY - int(bh * sc / 2) - int((im.height - chh * sc) / 2))

# ───────── Bloques de palabra clave ─────────
def norm(s): return re.sub(r'[^a-z0-9ñ]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode() if 'ñ' not in s.lower() else s.lower())
toks = [norm(w['w']) for w in words]
def busca(frase, desde=0.0):
    q = [norm(x) for x in frase.split()]
    for i in range(len(toks) - len(q) + 1):
        if toks[i:i + len(q)] == q and words[i]['s'] >= desde: return words[i]['s'], words[i + len(q) - 1]['e']
    raise SystemExit('no encontré: ' + frase)
# (frase dicha, líneas del bloque, estilo, encadena con el siguiente)
CLAVES = [
 ('seguimiento', ['SEGUIMIENTO'], 'nar', True), ('planificación', ['PLANIFICACIÓN'], 'nar', True), ('estrategia', ['ESTRATEGIA'], 'nar', False),
 ('cambio muy radical', ['CAMBIO', 'RADICAL'], 'nar', False),
 ('alcances', ['ALCANCES', 'CLAROS'], 'nar', False, 'claros'),
 ('tiempo récord', ['TIEMPO', 'RÉCORD'], 'nar', False),
 ('cero alcance', ['CERO', 'ALCANCE'], 'blanco', True), ('cifras inimaginables', ['CIFRAS', 'INIMAGINABLES'], 'nar', False),
 ('te referiría', ['TE REFERIRÍA'], 'nar', False),
 ('te contraten', ['QUE TE', 'CONTRATEN'], 'nar', False),
]
bloques = []
for frase, lineas, est, cad, *hasta in CLAVES:
    s, e = busca(frase)
    if hasta: e = busca(hasta[0], desde=s)[1]
    bloques.append(dict(s=s - 0.05, e=e + 0.55, lineas=lineas, est=est, cad=cad))
for i, b in enumerate(bloques):
    if b['cad']: b['e'] = bloques[i + 1]['s']
    b['e'] = max(b['e'], b['s'] + 1.15) if not b['cad'] else b['e']
# "que te contraten, definitivamente": sostener hasta que termina de decirlo
s, e = busca('definitivamente', desde=bloques[-1]['s']); bloques[-1]['e'] = e + 0.35
BL_CY, BL_MAXW = 1340, 650
bl_cache = {}
def bloque_img(bi, u, rest):
    b = bloques[bi]
    quieto = u > 1.2 and rest > 0.2
    if quieto and bi in bl_cache: return bl_cache[bi]
    S = 2
    # bloque tipográfico: cada línea se ajusta al ancho común (tope 132 px; una sola línea, tope 100)
    f100 = f_ancha(100)
    wl = [f100.getlength(l) for l in b['lineas']]
    if len(wl) == 1: tams = [min(100, int(100 * BL_MAXW / wl[0]))]
    else:
        Wt = min(BL_MAXW, max(wl)); tams = [min(132, int(100 * Wt / w)) for w in wl]
    fs = [f_ancha(t * S) for t in tams]
    caps_h = [(f.getbbox('M')[3] - f.getbbox('M')[1]) / S for f in fs]
    gap, padx, pady = 24, 46, 40
    tw = max(f.getlength(l) for f, l in zip(fs, b['lineas'])) / S
    bw, bh = int(tw + 2 * padx), int(sum(caps_h) + gap * (len(fs) - 1) + 2 * pady)
    M = 30
    im = Image.new('RGBA', ((bw + 2 * M) * S, (bh + 2 * M) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fondo, tinta = (NAR, BLANCO) if b['est'] == 'nar' else (BLANCO, NAR)
    caja = [M * S, M * S, (M + bw) * S, (M + bh) * S]
    d.rounded_rectangle(caja, radius=22 * S, fill=fondo + (255,))
    tmp = Image.new('RGBA', im.size, (0, 0, 0, 0)); dt = ImageDraw.Draw(tmp)
    k0 = 0; yb = M + pady
    for li, l in enumerate(b['lineas']):
        yb += caps_h[li]
        x = (M + bw / 2) * S - fs[li].getlength(l) / 2
        letras(dt, l, fs[li], x, yb * S, u - 0.06, tinta, S=S, k0=k0)
        k0 += len(l.replace(' ', '')); yb += gap
    msk = Image.new('L', im.size, 0); ImageDraw.Draw(msk).rounded_rectangle(caja, radius=22 * S, fill=255)
    im.alpha_composite(Image.composite(tmp, Image.new('RGBA', im.size, (0, 0, 0, 0)), msk))
    im = im.resize((bw + 2 * M, bh + 2 * M), Image.LANCZOS)
    a, sc, dx = 1.0, 1.0, 0
    if u < 0.2: sc = 0.72 + 0.34 * (u / 0.13) if u < 0.13 else 1.06 - 0.06 * ((u - 0.13) / 0.07); a = min(1, u / 0.06)
    if rest < 0.16 and not b['cad']: a = max(0, rest / 0.16); dx = -int(36 * (1 - a))
    if sc != 1.0: im = im.resize((max(2, int(im.width * sc)), max(2, int(im.height * sc))), Image.LANCZOS)
    if a < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    if quieto: bl_cache[bi] = (im, dx)
    return im, dx
def bloque_at(t):
    for bi, b in enumerate(bloques):
        if b['s'] <= t < b['e']: return bi, t - b['s'], b['e'] - t
    return None

# ───────── Captions karaoke ─────────
CAP_Y = 1398
f_cap = ImageFont.truetype(MONT % 'ExtraBold', 52)
cache = {}
def cap_img(ci, nsp):
    k = (ci, nsp)
    if k in cache: return cache[k]
    ws_ = [w['w'] for w in caps[ci]['words']]
    sp = f_cap.getlength(' '); wl = [f_cap.getlength(w) for w in ws_]
    bw, bh, S = int(sum(wl) + sp * (len(ws_) - 1) + 60), 104, 2
    im = Image.new('RGBA', (bw * S, bh * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, bw * S - 1, bh * S - 1], radius=16 * S, fill=BLANCO + (255,))
    fb = ImageFont.truetype(MONT % 'ExtraBold', 52 * S); x = 30 * S
    for i, w in enumerate(ws_):
        d.text((x, bh * S / 2 + S), w, font=fb, fill=(NAR if i < nsp else NAR_SUAVE) + (255,), anchor='lm'); x += (wl[i] + sp) * S
    im = im.resize((bw, bh), Image.LANCZOS); cache[k] = im
    return im
def cap_at(t):
    for ci, c in enumerate(caps):
        if c['s'] <= t < c['e']:
            return ci, max(1, sum(1 for w in c['words'] if t >= w['s'] - 0.03)), t - c['s']
    return None

# ───────── Eventos para los efectos de sonido ─────────
ev = []
ev += [dict(t=P_IN + 0.02, k='pop'), dict(t=P_IN + 0.12, k='ticks', n=6, paso=0.055), dict(t=P_IN + 0.62, k='whoosh'), dict(t=P_IN + 0.84, k='tick')]
for a, b in PREG:
    if b - a >= 1.0 and a > 0.5: ev.append(dict(t=a, k='swipe'))
for i, b in enumerate(bloques):
    enc = i > 0 and bloques[i - 1]['cad']
    ev.append(dict(t=b['s'], k='pop2' if enc else 'impacto'))
    ev.append(dict(t=b['s'] + 0.02, k='whoosh_c'))
    ev.append(dict(t=b['s'] + 0.09, k='ticks', n=min(7, sum(len(l.replace(' ', '')) for l in b['lineas']) // 2 + 1), paso=0.05))
json.dump(dict(ev=sorted(ev, key=lambda x: x['t']), bloques=bloques), open('eventos.json', 'w'), ensure_ascii=False, indent=1)
if os.environ.get('SOLO_EVENTOS'):
    for b in bloques: print(f"{b['s']:.2f}-{b['e']:.2f}", ' / '.join(b['lineas']))
    sys.exit()

# ───────── Contorno ─────────
sess = ort.InferenceSession('models/modnet.onnx', providers=['CPUExecutionProvider'])
def matte(rgb):
    x = np.asarray(Image.fromarray(rgb).resize((512, 896), Image.BILINEAR), np.float32) / 127.5 - 1
    return sess.run(None, {'input': x.transpose(2, 0, 1)[None]})[0][0, 0]
def ring_alpha(m):
    hard = Image.fromarray(((m > 0.5) * 255).astype(np.uint8)).resize((540, 960), Image.BILINEAR)
    hard = hard.point(lambda v: 255 if v > 127 else 0).filter(ImageFilter.MedianFilter(5))
    dil = hard.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(2.2))
    dil = dil.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
    inner = hard.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.6))
    da = np.clip(np.asarray(dil, np.float32) / 255 * 2.2 - 0.6, 0, 1)
    ia = np.clip(np.asarray(inner, np.float32) / 255 * 2.2 - 0.6, 0, 1)
    return da * (1 - ia)
def preg_w(t):
    for a, b in PREG:
        if b - a < 1.0: continue
        if a - 0.02 <= t <= b: return min(1, (t - a + 0.02) / 0.16, max(0, (b - t) / 0.16))
    return 0.0

# ───────── Lectura y escritura ─────────
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{max(0, f0 - 1) / FPS:.4f}', '-i', 'base_v.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-video_track_timescale', '15360', '-an', salida], stdin=subprocess.PIPE)
prev = None; m_prev = None; ra = None; blend_from = None; blend_k = 0
n = max(0, f0 - 1)
while n < f1:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    if n < f0: prev = fr; n += 1; continue
    t = n / FPS
    s = seg_start.get(n)
    if s is not None and s['corte'] == 'soft' and prev is not None: blend_from = prev.astype(np.float32); blend_k = 1
    raw = fr; out = None
    if blend_k:
        a = blend_k / 4.0; out = blend_from * (1 - a) + fr.astype(np.float32) * a
        blend_k = blend_k + 1 if blend_k < 3 else 0
    pw = preg_w(t)
    if pw > 0:
        if ra is None or n % 2 == 0:
            m = matte(raw)
            if m_prev is not None and not (s is not None and s['corte'] != 'soft'): m = 0.65 * m + 0.35 * m_prev
            m_prev = m; ra = ring_alpha(m)
        al = (ra * pw)[..., None]
        out = (fr.astype(np.float32) if out is None else out) * (1 - al) + 255.0 * al
    else: ra = None; m_prev = None
    img = Image.fromarray(fr if out is None else np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')
    if P_IN <= t < P_OUT:
        pl, pos = placa(t); img.alpha_composite(pl, pos)
    bq = bloque_at(t)
    if bq:
        bi, u, rest = bq
        bim, dx = bloque_img(bi, u, rest)
        img.alpha_composite(bim, (W // 2 - bim.width // 2 + dx, BL_CY - bim.height // 2))
    else:
        c = cap_at(t)
        if c:
            ci, nsp, u = c; cim = cap_img(ci, nsp)
            if u < 0.1:
                sc = 0.9 + 0.1 * (u / 0.1); cim = cim.resize((int(cim.width * sc), int(cim.height * sc)), Image.LANCZOS)
            img.alpha_composite(cim, (W // 2 - cim.width // 2, CAP_Y - cim.height // 2))
    arr = np.asarray(img.convert('RGB'))
    rest_v = (NF - n) / FPS
    if rest_v < 0.4: arr = (arr.astype(np.float32) * max(0, rest_v / 0.4)).astype(np.uint8)
    enc.stdin.write(arr.tobytes())
    prev = raw; n += 1
    if n % 300 == 0: print('cuadro', n, '/', f1, flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
print('listo', salida)
