# EDL del reel de Mario Barrera: cortes de contenido + recorte de silencios + encuadres
# uso: /usr/bin/python3 edl.py   → edl.json, run_base.sh
import json, re, subprocess, os, sys
import numpy as np
from PIL import Image

SRC = '../src/mario.mov'
FPS = 30
TM = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"

# Bloques de contenido (segundos del original)
KEEP = [
 (0.85, 19.39),    # saludo + P1 + "llegaste a resolver muchos problemas... gestión y organización"
 (27.02, 44.03),   # "hubo un seguimiento, una planificación, una estrategia... muy feliz"
 (44.90, 63.55),   # P2 + "el cambio más visible es la gente que capacitaste para ventas"
 (66.24, 85.70),   # "sí fue un cambio muy radical... ágil y hábil"
 (101.05, 134.26), # "toda la empatía... un proyecto que pensábamos que ya estaba perdido"
 (135.30, 157.60), # P3 + "de tener cero alcance llegamos a cifras inimaginables"
 (160.72, 167.17), # "el cliente está muy contento... te referiría en todos los proyectos"
 (167.92, 176.07), # "Súper" + P4
 (178.28, 205.00), # "muchas veces como dueños de negocio... que te contraten, definitivamente"
 (223.75, 236.35), # cierre: dónde encontrarlo
]
# Cambios de encuadre (tiempo original → escala). W abierto, M medio, C cerrado
W, M, C = 1.0, 1.14, 1.28
SHOTS = [
 (0.85, W), (11.30, M), (27.02, C), (44.90, W), (55.80, M), (66.24, C), (101.05, M),
 (135.30, W), (141.90, C), (160.72, M), (167.92, W), (178.28, M), (196.34, C), (223.75, W),
]
# Tramos donde pregunta March (original): llevan contorno blanco
PREG = [(0.85, 10.45), (44.90, 55.00), (135.30, 141.05), (167.92, 175.95), (223.75, 226.45), (234.40, 235.30)]

MIN_SIL, LEAVE_A, LEAVE_B = 0.62, 0.17, 0.15
sil = []
for l in open('sil.txt'):
    m = re.match(r'([\d.]+)-([\d.]+)', l)
    a, b = float(m[1]), float(m[2])
    if sil and a - sil[-1][1] < 0.06: sil[-1] = (sil[-1][0], b)
    else: sil.append((a, b))

def grid(t): return round(t * FPS) / FPS

shot_times = [s[0] for s in SHOTS]
segs = []   # (a, b, corte)  corte: 'hard' | 'soft' | 'shot'
for ka, kb in KEEP:
    cuts = [ka]
    tipos = ['hard']
    for a, b in sil:
        en_preg = any(pa <= a and b <= pb for pa, pb in PREG)   # la voz de March llega baja: no recortar dentro de sus preguntas
        if a > ka + 0.2 and b < kb - 0.2 and (b - a) >= MIN_SIL and not en_preg:
            ra, rb = a + LEAVE_A, b - LEAVE_B
            # si hay cambio de encuadre dentro del silencio, es corte de plano
            es_shot = any(a <= st <= b for st in shot_times)
            cuts += [ra, rb]; tipos.append('shot' if es_shot else 'soft')
    # cambios de encuadre que no caen en silencio recortado
    for st in shot_times:
        if ka < st < kb and not any(a <= st <= b and (b - a) >= MIN_SIL and not any(pa <= a and b <= pb for pa, pb in PREG) for a, b in sil):
            cuts += [st, st]; tipos.append('shot')
    cuts.append(kb)
    # ordenar pares
    pares = sorted(zip(cuts[1:-1:2], cuts[2:-1:2], tipos[1:]), key=lambda x: x[0])
    ini = ka; tipo = 'hard'
    for ra, rb, tp in pares:
        segs.append((grid(ini), grid(ra), tipo)); ini = rb; tipo = tp
    segs.append((grid(ini), grid(kb), tipo))
segs = [s for s in segs if s[1] - s[0] > 1 / FPS]

def scale_at(t):
    sc = SHOTS[0][1]
    for st, s in SHOTS:
        if t >= st - 0.02: sc = s
    return sc
def shot_idx(t):
    i = 0
    for k, (st, s) in enumerate(SHOTS):
        if t >= st - 0.02: i = k
    return i

# Ancla de cabeza por plano (segmentación en el primer cuadro del plano)
import onnxruntime as ort
sess = ort.InferenceSession('models/modnet.onnx', providers=['CPUExecutionProvider'])
def head(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', SRC, '-frames:v', '1',
        '-vf', f'scale=512:896,{TM}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(896, 512, 3).astype(np.float32) / 127.5 - 1
    m = sess.run(None, {'input': im.transpose(2, 0, 1)[None]})[0][0, 0]
    rows = np.where((m > 0.5).sum(1) > 12)[0]
    top = rows[0]
    band = m[top:top + 110]
    xs = np.where(band > 0.5)[1]
    return float(xs.mean()) / 512 * 2160, float(top) / 896 * 3840
anchors = {}
for k, (st, sc) in enumerate(SHOTS):
    cx, top = head(st + 0.3)
    anchors[k] = (cx, top)
    print('plano', k, st, sc, 'cabeza x', round(cx), 'tope', round(top))

out = []
t_new = 0.0
for a, b, tp in segs:
    k = shot_idx(a); sc = SHOTS[k][1]; cx, top = anchors[k]
    cw = int(round(2160 / sc / 2)) * 2; ch = int(round(3840 / sc / 2)) * 2
    x0 = int(min(max(cx - cw / 2, 0), 2160 - cw) / 2) * 2
    # tope de la cabeza a ~9.5 % de la altura de salida cuando hay zoom; abierto conserva el cuadro
    y0 = 0 if sc == 1.0 else int(min(max(top - 0.095 * ch, 0), 3840 - ch) / 2) * 2
    d = round((b - a) * FPS) / FPS
    out.append(dict(a=a, b=b, d=d, t=round(t_new, 4), corte=tp, plano=k, esc=sc, crop=[cw, ch, x0, y0]))
    t_new += d
print('segmentos', len(out), 'duración', round(t_new, 2))

def remap(t):
    for s in out:
        if s['a'] <= t <= s['b']: return s['t'] + (t - s['a'])
    # si cae en un hueco, al inicio del siguiente segmento
    for s in out:
        if s['a'] > t: return s['t']
    return t_new
preg = [(round(remap(a), 3), round(remap(b), 3)) for a, b in PREG]
json.dump(dict(segs=out, dur=t_new, preg=preg), open('edl.json', 'w'), indent=1)

# Comando ffmpeg: video
ins, fc = [], []
for i, s in enumerate(out):
    ins += ['-ss', f"{s['a']:.4f}", '-t', f"{s['d'] + 0.2:.4f}", '-i', SRC]
    cw, ch, x0, y0 = s['crop']
    n = round(s['d'] * FPS)
    fc.append(f"[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,crop={cw}:{ch}:{x0}:{y0},scale=1080:1920:flags=lanczos,setsar=1[v{i}]")
fc.append(''.join(f'[v{i}]' for i in range(len(out))) + f"concat=n={len(out)}:v=1:a=0,{TM},eq=saturation=0.96[v]")
open('fc_video.txt', 'w').write(';\n'.join(fc))
# audio: desde el wav, con microfundidos en cada corte
fa = []
for i, s in enumerate(out):
    fa.append(f"[0:a]atrim=start={s['a']:.4f}:end={s['a'] + s['d']:.4f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.012,afade=t=out:st={s['d'] - 0.014:.4f}:d=0.012[a{i}]")
fa.append(''.join(f'[a{i}]' for i in range(len(out))) + f"concat=n={len(out)}:v=0:a=1,highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000[a]")
open('fc_audio.txt', 'w').write(';\n'.join(fa))
cmd = "ffmpeg -v error -stats -y " + ' '.join(ins) + " -filter_complex_script fc_video.txt -map '[v]' -r 30 -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 base_v.mp4\n"
cmd += "ffmpeg -v error -y -i audio.wav -filter_complex_script fc_audio.txt -map '[a]' -c:a pcm_s16le base_a.wav\n"
open('run_base.sh', 'w').write(cmd)
for s in out: print(f"{s['t']:7.2f}  {s['a']:7.2f}-{s['b']:7.2f} d={s['d']:.2f} {s['corte']:5} plano {s['plano']} esc {s['esc']} crop {s['crop']}")
print('preg', preg)
