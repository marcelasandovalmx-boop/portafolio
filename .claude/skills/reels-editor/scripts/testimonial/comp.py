# Compositor del reel de Mario: fundidos de corte suave, contorno blanco en preguntas,
# placa de nombre y captions tipo karaoke (caja blanca, texto que se va pintando).
# uso: /usr/bin/python3 comp.py [t_ini t_fin salida]   (sin argumentos = video completo)
import json, subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import onnxruntime as ort

W, H, FPS = 1080, 1920, 30
F = '/root/.fonts/montserrat/Montserrat-%s.ttf'
ROJO = (229, 80, 28)          # naranja Orangy #E5501C
ROJO_SUAVE = (245, 176, 150)  # palabra aún no dicha
TINTA = (40, 22, 14)

edl = json.load(open('edl.json'))
caps = json.load(open('captions.json'))
segs = edl['segs']; DUR = edl['dur']; PREG = edl['preg']
NF = round(DUR * FPS)
seg_start = {round(s['t'] * FPS): s for s in segs}

t0, t1, salida = 0.0, DUR, 'out.mp4'
if len(sys.argv) >= 4:
    t0, t1, salida = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
f0, f1 = round(t0 * FPS), min(NF, round(t1 * FPS))

# ── Captions ──
CAP_Y = 1398
f_cap = ImageFont.truetype(F % 'ExtraBold', 52)
cache = {}
def cap_img(ci, nsp):
    k = (ci, nsp)
    if k in cache: return cache[k]
    words = [w['w'] for w in caps[ci]['words']]
    sp = f_cap.getlength(' ')
    ws = [f_cap.getlength(w) for w in words]
    tw = sum(ws) + sp * (len(words) - 1)
    padx, bh = 30, 104
    bw = int(tw + 2 * padx)
    S = 2  # supermuestreo
    im = Image.new('RGBA', (bw * S, bh * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, bw * S - 1, bh * S - 1], radius=16 * S, fill=(255, 255, 255, 255))
    fb = ImageFont.truetype(F % 'ExtraBold', 52 * S)
    x = padx * S
    for i, w in enumerate(words):
        d.text((x, bh * S / 2 + 1 * S), w, font=fb, fill=(ROJO if i < nsp else ROJO_SUAVE) + (255,), anchor='lm')
        x += (ws[i] + sp) * S
    im = im.resize((bw, bh), Image.LANCZOS)
    cache[k] = im
    return im

def cap_at(t):
    for ci, c in enumerate(caps):
        if c['s'] <= t < c['e']:
            nsp = sum(1 for w in c['words'] if t >= w['s'] - 0.03)
            return ci, max(1, nsp), t - c['s']
    return None

# ── Placa de nombre ──
P_IN, P_OUT = 0.95, 6.35
NOMBRE = ['MARIO', 'BARRERA']
ROL = ['Aliado', 'estratégico']
f_nom = ImageFont.truetype(F % 'Black', 50)
f_rol = ImageFont.truetype(F % 'Medium', 40)
def placa(t):
    """Devuelve RGBA 1080x(alto) y su posición, según el tiempo desde P_IN."""
    u = t - P_IN
    S = 2
    fn = ImageFont.truetype(F % 'Black', 50 * S); fr = ImageFont.truetype(F % 'Medium', 40 * S)
    spn = f_nom.getlength(' '); spr = f_rol.getlength(' ')
    wn = [f_nom.getlength(w) for w in NOMBRE]; wr = [f_rol.getlength(w) for w in ROL]
    tn = sum(wn) + spn * (len(NOMBRE) - 1); tr = sum(wr) + spr * (len(ROL) - 1)
    bw, bh = int(tn + 64), 92
    rw, rh = max(int(tr + 80), bw + 64), 100
    off = 36
    cw, chh = rw + 8, bh + rh - 10 + 8
    im = Image.new('RGBA', (cw * S, chh * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # caja roja (entra a los 0.55 s, con barrido vertical)
    if u >= 0.55:
        p = min(1, (u - 0.55) / 0.22); p = 1 - (1 - p) ** 3
        y_a = (bh - 10) * S; hh = int(rh * S * p)
        d.rectangle([0, y_a, rw * S, y_a + hh], fill=ROJO + (255,))
        x = 40 * S
        for i, w in enumerate(ROL):
            ti = u - 0.72 - 0.16 * i
            if ti >= 0:
                q = min(1, ti / 0.2); q = 1 - (1 - q) ** 3
                yy = y_a + rh * S / 2 + (1 - q) * 26 * S
                tmp = Image.new('RGBA', im.size, (0, 0, 0, 0))
                ImageDraw.Draw(tmp).text((x, yy), w, font=fr, fill=TINTA + (int(255 * q),), anchor='lm')
                # recorte al interior de la caja roja
                msk = Image.new('L', im.size, 0); ImageDraw.Draw(msk).rectangle([0, y_a, rw * S, y_a + rh * S], fill=255)
                im.paste(tmp, (0, 0), Image.composite(tmp.getchannel('A'), Image.new('L', im.size, 0), msk))
            x += (wr[i] + spr) * S
        d = ImageDraw.Draw(im)
    # caja blanca con nombre (palabra por palabra)
    d.rounded_rectangle([off * S, 0, (off + bw) * S, bh * S], radius=14 * S, fill=(255, 255, 255, 255))
    x = (off + 32) * S
    for i, w in enumerate(NOMBRE):
        if u >= 0.10 + 0.22 * i:
            d.text((x, bh * S / 2 + 1 * S), w, font=fn, fill=ROJO + (255,), anchor='lm')
        x += (wn[i] + spn) * S
    im = im.resize((cw, chh), Image.LANCZOS)
    # entrada con rebote y salida con fundido
    a = 1.0; sc = 1.0
    if u < 0.14: sc = 0.86 + 0.18 * (u / 0.14) if u < 0.1 else 1.04 - 0.04 * ((u - 0.1) / 0.04); a = min(1, u / 0.08)
    if t > P_OUT - 0.25: a = max(0, (P_OUT - t) / 0.25)
    if sc != 1.0:
        im = im.resize((max(2, int(cw * sc)), max(2, int(chh * sc))), Image.LANCZOS)
    if a < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    return im
PLACA_X, PLACA_Y = 150, 905   # esquina superior izquierda de la caja roja (referencia)

# ── Segmentación para el contorno ──
sess = ort.InferenceSession('models/modnet.onnx', providers=['CPUExecutionProvider'])
def matte(rgb):
    x = np.asarray(Image.fromarray(rgb).resize((512, 896), Image.BILINEAR), np.float32) / 127.5 - 1
    return sess.run(None, {'input': x.transpose(2, 0, 1)[None]})[0][0, 0]
def ring_alpha(m):
    """m: matte 896x512 (0..1) → alfa del anillo a 1080x1920."""
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
        if a - 0.02 <= t <= b:
            return min(1, (t - a + 0.02) / 0.16, max(0, (b - t) / 0.16))
    return 0.0

# ── Lectura y escritura ──
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{max(0, f0 - 1) / FPS:.4f}', '-i', __import__('os').environ.get('BASE', 'base_v.mp4'),
    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
audio = ['-ss', f'{f0 / FPS:.4f}', '-t', f'{(f1 - f0) / FPS:.4f}', '-i', 'base_a.wav']
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-'] + audio +
    ['-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
     '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart',
     '-c:a', 'aac', '-b:a', '192k', '-shortest', salida], stdin=subprocess.PIPE)

prev = None; m_prev = None; ra = None; blend_from = None; blend_k = 0
n = max(0, f0 - 1)
while n < f1:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    if n < f0:
        prev = fr; n += 1; continue
    t = n / FPS
    s = seg_start.get(n)
    if s is not None and s['corte'] == 'soft' and prev is not None:
        blend_from = prev.astype(np.float32); blend_k = 1
    raw = fr
    out = fr.astype(np.float32)
    if blend_k:
        a = blend_k / 4.0
        out = blend_from * (1 - a) + out * a
        blend_k = blend_k + 1 if blend_k < 3 else 0
    # contorno
    pw = preg_w(t)
    if pw > 0:
        if ra is None or n % 2 == 0:
            m = matte(raw)
            if m_prev is not None and not (s is not None and s['corte'] != 'soft'): m = 0.65 * m + 0.35 * m_prev
            m_prev = m; ra = ring_alpha(m)
        al = (ra * pw)[..., None]
        out = out * (1 - al) + 255.0 * al
    else:
        ra = None; m_prev = None
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    # placa
    if P_IN <= t < P_OUT:
        pl = placa(t)
        img.paste(pl, (PLACA_X, PLACA_Y), pl)
    # caption
    c = cap_at(t)
    if c:
        ci, nsp, u = c
        ci_img = cap_img(ci, nsp)
        if u < 0.1:
            sc = 0.9 + 0.1 * (u / 0.1)
            ci_img = ci_img.resize((int(ci_img.width * sc), int(ci_img.height * sc)), Image.LANCZOS)
        img.paste(ci_img, (W // 2 - ci_img.width // 2, CAP_Y - ci_img.height // 2), ci_img)
    arr = np.asarray(img)
    # fundido de salida
    rest = (NF - n) / FPS
    if rest < 0.4: arr = (arr.astype(np.float32) * max(0, rest / 0.4)).astype(np.uint8)
    enc.stdin.write(arr.tobytes())
    prev = raw
    n += 1
    if n % 300 == 0: print('cuadro', n, '/', f1, flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
print('listo', salida)
