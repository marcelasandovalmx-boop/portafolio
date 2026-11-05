# Pasada 5 · Sonido: voz limpia, lo-fi con ducking, efectos mínimos y máster −14 LUFS / −1 dBTP
import json, re, subprocess, sys
VIDEO = sys.argv[1]; SALIDA = sys.argv[2]
E = json.load(open('/root/reels/proyecto/4-graficos/escenas.json')); DUR = E['dur']
def lufs(args):
    o = subprocess.run(['ffmpeg', '-hide_banner', *args, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', o)[-1])
voz_db, _ = lufs(['-i', VIDEO, '-map', '0:a'])
import os
MUSICA = os.environ.get('MUSICA', 'musica-lofi.wav')
mus_db, _ = lufs(['-i', MUSICA])
who_db = -20.0  # pico aprox. del whoosh normalizado (efecto corto; se nivela por pico)
# efectos: whoosh en cada cambio de escena (entrada y salida), toque al cierre
cambios = sorted({round(t, 2) for a, b, k in E['escenas'] for t in (a, b) if 0.5 < t < DUR - 0.5 and k != 'cierre'} | {round(E['escenas'][-1][0], 2)})
toque = E['escenas'][-1][0] + 0.2
g_mus = (voz_db - float(os.environ.get('MUS_DB', 18))) - mus_db                               # música 18 dB debajo de la voz
import os
ICO = json.load(open('/root/reels/proyecto/4-graficos/iconos.json')) if os.environ.get('CLICS') else []
inputs = ['-i', VIDEO, '-i', MUSICA] + sum([['-i', 'SFX_WHOOSH_pitch1.0x.wav'] for _ in cambios], []) + sum([['-i', 'SFX_UICLICK_pitch1.0x.wav'] for _ in ICO], []) + ['-i', 'SFX_UICLICK_pitch1.0x.wav']
fc = [f"[0:a]highpass=f=80,deesser=i=0.3,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,asplit[voz][sc]",
      f"[1:a]atrim=0:{DUR},volume={g_mus:.2f}dB,afade=t=in:d=0.6,afade=t=out:st={DUR-1.5}:d=1.5[m0]",
      "[m0][sc]sidechaincompress=threshold=0.02:ratio=4:attack=40:release=450:makeup=1[mus]"]
mix = ['[voz]', '[mus]']
for n, t in enumerate(cambios):   # whoosh centrado en el corte (pico a ~0.4 s del inicio)
    fc.append(f"[{2+n}:a]volume=-22dB,adelay={max(0,int((t-0.4)*1000))}|{max(0,int((t-0.4)*1000))}[w{n}]"); mix.append(f'[w{n}]')
for j, t in enumerate(ICO):     # clic suave en cada elemento (−28 dB): acompaña sin estorbar
    n = 2 + len(cambios) + j
    fc.append(f"[{n}:a]volume=-28dB,adelay={int(t*1000)}|{int(t*1000)}[c{j}]"); mix.append(f'[c{j}]')
k = 2 + len(cambios) + len(ICO)
fc.append(f"[{k}:a]volume=-16dB,adelay={int(toque*1000)}|{int(toque*1000)}[tq]"); mix.append('[tq]')
fc.append(''.join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[pre]")
pre = 'premezcla.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[pre]', '-ar', '48000', pre], check=True)
# loudnorm en dos pasadas
o = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(o[o.rindex('{'):o.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO, '-i', pre, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', af,
                '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', SALIDA], check=True)
I, TP = lufs(['-i', SALIDA])
print(f'voz {voz_db:.1f} LUFS · música {g_mus:+.1f} dB · {len(cambios)} whooshes en {cambios} · toque {toque:.2f}')
print(f'FINAL: {I:.1f} LUFS integrados · pico real {TP:.1f} dBTP')
