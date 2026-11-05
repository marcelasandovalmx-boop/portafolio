import json, subprocess
W = json.load(open('../1-transcripcion/words.json'))
# --- correcciones de March (texto de subtítulos) ---
def fix(i, new): W[i]['word'] = new
idx = {i: w['word'] for i, w in enumerate(W)}
def find(word, near):
    c = [i for i, w in idx.items() if w == word]; return min(c, key=lambda i: abs(W[i]['start'] - near))
fix(find('Marcelo,', 29), 'Marcela,')
i = find('ofrezcas.', 58.7); fix(i, 'ofreces.'); W[i-1]['drop'] = True          # "te ofrezcas" -> "ofreces"
i = find('aterregató', 97.5); fix(i, 'regateó'); fix(i-1, 'te')                 # "se aterregató" -> "te regateó"
i = find('horas,', 101.3); fix(i, 'deshoras,'); fix(i-1, 'a'); W[i-2]['drop'] = True if W[i-2]['word']=='de' else W[i-2].get('drop')
i = find('que', 115.6); assert W[i-1]['word'] in ('bueno',), W[i-1]; fix(i-1, 'bueno,'); W[i]['drop'] = True
fix(find('Piensan', 181.4), 'Piensa')
W = [w for w in W if not w.get('drop')]
# --- cortes: silencio inicial/final, pausas >0.8 s (quedan ~0.4 s), tropiezo A ---
FIN = 209.0
cuts = [(0, 1.09), (80.82, 81.54), (83.06, 83.78), (170.16, 171.69), (202.87, 203.28), (206.25, FIN)]
keep, t = [], 0
for a, b in cuts:
    if a > t: keep.append((t, a))
    t = b
json.dump({'cuts': cuts, 'keep': keep}, open('cortes.json', 'w'), indent=1)
def remap(x):
    off = 0
    for a, b in cuts:
        if x >= b: off += b - a
        elif x > a: return None
    return round(x - off, 3)
out = []
for w in W:
    s, e = remap(w['start']), remap(w['end'])
    if s is None or e is None:
        if 170.16 <= w['start'] < 171.69: continue    # palabras del tropiezo A
        s = s if s is not None else remap(min(b for a, b in cuts if a < w['start'] <= b))
        e = e if e is not None else remap(max(a for a, b in cuts if a < w['end'] <= b))
    out.append({'word': w['word'], 'start': s, 'end': e})
json.dump(out, open('words.json', 'w'), ensure_ascii=False, indent=1)
dur = sum(b - a for a, b in keep)
print(f"{len(out)} palabras · antes {FIN:.2f}s · después {dur:.2f}s")
# --- render: segmentos + fundido de 8 ms en cada unión ---
fc, n = [], len(keep)
for k, (a, b) in enumerate(keep):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{k}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={b-a-0.008:.3f}:d=0.008[a{k}]")
fc.append(''.join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/root/reels/tomas/video.mp4', '-filter_complex', ';'.join(fc),
    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30',
    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', 'corte.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'corte.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '26',
    '-preset', 'fast', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'vista-previa-1B.mp4'], check=True)
