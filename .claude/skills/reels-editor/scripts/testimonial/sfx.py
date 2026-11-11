# Efectos de sonido sintetizados (sin librerías con licencia): pop, tick, whoosh, swipe, impacto.
# uso: /usr/bin/python3 sfx.py  → sfx.wav (48 kHz mono) alineado al video
import json, wave, numpy as np
SR = 48000
rng = np.random.default_rng(7)
ev = json.load(open('eventos.json'))['ev']
edl = json.load(open('edl.json')); N = int(edl['dur'] * SR) + SR
out = np.zeros(N, np.float32)

def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def bandpass_var(x, f_ini, f_fin, q=1.4):
    """Filtro pasa banda de estado variable con frecuencia que barre."""
    y = np.zeros_like(x); lp = bp = 0.0
    fs = np.geomspace(f_ini, f_fin, len(x))
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * fs[i] / SR)
        hp = x[i] - lp - bp / q
        bp += f * hp; lp += f * bp
        y[i] = bp
    return y
def pop(f0=560, f1=190, amp=0.30):
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / t[-1]); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 0.022)
    s[:int(0.002 * SR)] += rng.standard_normal(int(0.002 * SR)) * 0.25
    return s * amp
def tick(amp=0.085):
    n = int(0.018 * SR); x = rng.standard_normal(n)
    x = np.diff(x, prepend=0)  # realce de agudos
    f = rng.uniform(2300, 3400); t = np.arange(n) / SR
    return (x * 0.5 + np.sin(2 * np.pi * f * t)) * env_exp(n, 0.0035) * amp
def whoosh(dur=0.34, f_ini=500, f_fin=3200, amp=0.16):
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float64)
    y = bandpass_var(x, f_ini, f_fin)
    p = np.arange(n) / n; e = np.sin(np.pi * p ** 0.7) ** 2
    y = y / (np.abs(y).max() + 1e-9)
    return (y * e * amp).astype(np.float32)
def impacto(amp=0.42):
    n = int(0.32 * SR); t = np.arange(n) / SR
    f = 120 * (52 / 120) ** (t / t[-1]); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.075)
    m = int(0.03 * SR); golpe = rng.standard_normal(m); golpe = np.convolve(golpe, np.ones(24) / 24, 'same') * env_exp(m, 0.008)
    s[:m] += golpe * 1.6
    return np.tanh(s * 1.4) * amp
def pon(t, s):
    i = int(t * SR)
    if i < 0 or i >= N: return
    j = min(N, i + len(s)); out[i:j] += s[:j - i]

for e in ev:
    k, t = e['k'], e['t']
    if k == 'pop': pon(t, pop())
    elif k == 'pop2': pon(t, pop(680, 240, 0.26))
    elif k == 'tick': pon(t, tick())
    elif k == 'ticks':
        for q in range(e['n']): pon(t + q * e['paso'], tick(0.07 + 0.02 * rng.random()))
    elif k == 'whoosh': pon(t - 0.05, whoosh())
    elif k == 'whoosh_c': pon(t - 0.04, whoosh(0.26, 700, 3600, 0.11))
    elif k == 'swipe': pon(t - 0.06, whoosh(0.3, 2600, 600, 0.10))
    elif k == 'impacto': pon(t, impacto())
pico = float(np.abs(out).max()); print('eventos', len(ev), 'pico', round(20 * np.log10(pico), 1), 'dBFS')
w = wave.open('sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
