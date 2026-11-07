# Plantilla de referencia (sistema B "se escribe solo" + chips + polaroids). Ajusta rutas, KEEP y overlays por proyecto.
"""Reel March v6 · calidad (sin ampliar, denoise) + sistema de textos tipo referencia 3 con branding March:
captions typewriter serif/sans, chips, polaroids con trabajo real, momento dim, lockups rojos, firma."""
import json, subprocess, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
T = json.load(open("transcript.json")); words = [w for s in T for w in s["words"]]
IMG = "/home/user/portafolio/img"

KEEP = [(2.4, 29.80), (34.98, 43.44), (47.16, 61.14), (72.62, 82.50), (92.30, 98.22),
        (116.74, 125.20), (132.90, 137.98), (98.22, 108.36)]
def snap(t, kind):
    if kind == "start":
        c = [w["s"] for w in words if w["s"] >= t - 0.25]; return (min(c) if c else t) - 0.12
    c = [w["e"] for w in words if w["e"] <= t + 0.25]
    if not c: return t
    e = max(c); nxt = [w["s"] for w in words if w["s"] >= e]
    return e + min(0.18, max(0.0, (min(nxt) if nxt else e + 1) - e))
KEEP = [(max(0, snap(a, "start")), snap(b, "end")) for a, b in KEEP]
total = sum(b - a for a, b in KEEP)
def remap(t):
    acc = 0.0
    for a, b in KEEP:
        if a <= t <= b: return acc + (t - a)
        acc += b - a
    return None
seg_bounds = []; acc = 0.0
for a, b in KEEP: seg_bounds.append(round(acc, 3)); acc += b - a
def at(t): return remap(t)
def seg_end(t):  # fin (línea nueva) del segmento que contiene t
    for i, (a, b) in enumerate(KEEP):
        if a <= t <= b: return seg_bounds[i] + (b - a)
TITLE_END = 3.6; LAST = KEEP[-1][1] - KEEP[-1][0]

# ---------- overlays ----------
NF = HERE + "/npmfonts"
css = f"""
@font-face{{font-family:'Mont';src:url(/root/.fonts/montserrat/Montserrat-ExtraBold.ttf);font-weight:800}}
@font-face{{font-family:'Mont';src:url(/root/.fonts/montserrat/Montserrat-Bold.ttf);font-weight:700}}
@font-face{{font-family:'Mont';src:url(/root/.fonts/montserrat/Montserrat-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:'Mont';src:url(/root/.fonts/montserrat/Montserrat-Medium.ttf);font-weight:500}}
@font-face{{font-family:'Playfair';src:url({HERE}/fonts/PlayfairDisplay.ttf);font-weight:400 900}}
@font-face{{font-family:'Playfair';src:url({HERE}/fonts/PlayfairDisplay-Italic.ttf);font-weight:400 900;font-style:italic}}
@font-face{{font-family:'Marker';src:url({NF}/covered-by-your-grace/files/covered-by-your-grace-latin-400-normal.woff2)}}
@font-face{{font-family:'Firma';src:url({NF}/dawning-of-a-new-day/files/dawning-of-a-new-day-latin-400-normal.woff2)}}
body{{margin:0;background:transparent;width:1080px;height:1920px;position:relative;font-family:'Mont';color:#fff}}
.lock{{position:absolute;left:110px;right:170px;top:1040px;display:flex;flex-direction:column;align-items:center;text-align:center;text-shadow:0 6px 30px rgba(0,0,0,.55),0 1px 5px rgba(0,0,0,.35)}}
.lock.mid{{top:760px;left:90px;right:90px}}
.caps{{font-family:'Mont';font-weight:800;font-size:84px;line-height:1;letter-spacing:.01em;text-transform:uppercase}}
.marker{{font-family:'Marker';font-size:150px;line-height:.9;margin:6px 0 2px}}
.script{{font-family:'Firma';font-size:150px;line-height:.9;margin:4px 0 0}}
.label{{display:inline-block;background:#fff;color:#c92520;font-family:'Mont';font-weight:700;font-size:34px;letter-spacing:.18em;text-transform:uppercase;padding:10px 22px 8px;text-shadow:none;margin-bottom:22px}}
.bar{{display:inline-block;background:#c92520;color:#fff;font-family:'Mont';font-weight:800;font-size:96px;line-height:1;letter-spacing:-.01em;text-transform:uppercase;padding:18px 34px 14px;margin-top:16px;text-shadow:none;box-shadow:0 10px 30px rgba(0,0,0,.3)}}
.row{{display:flex;gap:18px;align-items:center;justify-content:center;margin-top:22px;font-family:'Mont';font-weight:600;font-size:40px;flex-wrap:wrap}}
.row i{{font-style:normal;color:#7bb8c2;font-weight:800;font-size:52px}}
.sub{{font-family:'Mont';font-weight:500;font-size:30px;letter-spacing:.16em;text-transform:uppercase;margin-top:24px;opacity:.95}}
.firma{{position:absolute;left:0;right:0;top:272px;display:flex;flex-direction:column;align-items:center;text-shadow:0 3px 16px rgba(0,0,0,.6);opacity:.92}}
.firma .nm{{font-family:'Playfair';font-weight:400;font-size:42px;letter-spacing:.02em;line-height:1}}
.firma .tg{{font-family:'Mont';font-weight:500;font-size:14px;letter-spacing:.32em;text-transform:uppercase;margin-top:8px}}
/* chips (columna bajo los captions) */
.chip{{position:absolute;left:0;right:170px;display:flex;justify-content:center}}
.chip span{{display:inline-flex;align-items:center;gap:14px;background:rgba(255,255,255,.96);color:#343434;font-family:'Mont';font-weight:600;font-size:36px;line-height:1;padding:16px 28px 15px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.28)}}
.chip b{{font-weight:800;color:#c92520;font-size:38px}} .chip i{{font-style:normal;font-weight:800;color:#7bb8c2;font-size:38px}}
/* polaroid con trabajo real */
.pol{{position:absolute;left:50%;top:940px;width:560px;margin-left:-330px;background:#fff;padding:22px 22px 18px;box-shadow:0 18px 50px rgba(0,0,0,.4);transform:rotate(-3deg)}}
.pol.r{{transform:rotate(2.5deg);margin-left:-230px}}
.pol img{{width:560px;height:560px;object-fit:cover;display:block}}
.pol .cap{{font-family:'Marker';font-size:40px;color:#343434;text-align:center;margin-top:10px;line-height:1}}
"""
def chip(k, txt, icon="♡", icon_cls="b"): return f'<div class="chip" style="top:{1190 + k*74}px"><span><{icon_cls}>{icon}</{icon_cls}>{txt}</span></div>'
def pol(img, cap, cls=""): return f'<div class="pol {cls}"><img src="{IMG}/{img}"><div class="cap">{cap}</div></div>'

OV = []  # (id, start, dur, html, hide_captions)
OV.append(("titulo", 0.0, TITLE_END, '<div class="lock"><div class="caps">Tu producto</div><div class="marker">es excelente.</div><div class="bar" style="font-size:66px;line-height:1.08">y tu marca<br>no lo dice.</div></div>', True))
OV.append(("pol1", at(9.88), at(11.88) - at(9.88), pol("caso-2/slide-3-sm.jpg", "lo que diseñas · Kaleia"), True))
OV.append(("pol2", at(11.88), at(13.70) - at(11.88), pol("caso-1/slide-2-sm.jpg", "lo que cocinas · Xcaanda'", "r"), True))
OV.append(("pol3", at(13.70), at(15.9) - at(13.70), pol("caso-5/slide-3-sm.jpg", "el servicio que prestas · GAMA IP"), True))
e1 = seg_end(24.4)
OV.append(("c1", at(24.40), e1 - at(24.40), chip(0, "nuevos clientes"), False))
OV.append(("c2", at(26.22), e1 - at(26.22), chip(1, "cómo los atiendes"), False))
OV.append(("c3", at(27.62), e1 - at(27.62), chip(2, "que repitan"), False))
OV.append(("c4", at(28.72), e1 - at(28.72), chip(3, "que te recomienden"), False))
DIM = (at(36.96), 3.0)
OV.append(("culpa", DIM[0], DIM[1], '<div class="lock mid"><div class="caps" style="font-size:76px">No te sientas</div><div class="marker" style="font-size:170px">culpable.</div></div>', True))
e2 = at(53.5)
OV.append(("c5", at(48.26), e2 - at(48.26), chip(0, "logo hecho con IA", "✦", "i"), False))
OV.append(("c6", at(50.56), e2 - at(50.56), chip(1, "no me representa", "✕"), False))
e3 = seg_end(78.76)
OV.append(("c7", at(78.76), e3 - at(78.76), chip(0, "wow, está increíble", "✓", "i"), False))
OV.append(("c8", at(80.34), e3 - at(80.34), chip(1, "me ayudaste un montón", "✓", "i"), False))
OV.append(("nivel", at(92.30) + 0.2, at(98.22) - at(92.30) - 0.2, '<div class="lock"><div class="label">Tu comunicación</div><div class="script" style="font-size:132px">no está al nivel</div><div class="bar" style="font-size:72px">de tu producto.</div></div>', True))
OV.append(("c9", at(119.5), at(121.4) - at(119.5), chip(0, "funciona como Google Maps", "⌖", "i"), False))
OV.append(("maps", at(121.56), at(125.20) - at(121.56), '<div class="lock"><div class="row" style="margin:0;font-size:50px"><span>dónde estás</span><i>→</i><span>a dónde vas</span></div><div class="bar" style="font-size:110px;margin-top:26px">la ruta.</div></div>', True))
OV.append(("c10", at(135.66), seg_end(135.66) - at(135.66), chip(0, "hacemos match", "✓", "i"), False))
OV.append(("cta", total - LAST + 0.3, LAST - 0.4, '<div class="lock"><div class="label">Escribe</div><div class="bar" style="font-size:104px;margin-top:0">diagnóstico</div><div class="marker" style="font-size:104px;margin-top:18px">aquí abajo</div><div class="sub">o mándame DM</div></div>', True))
OV.append(("firma", TITLE_END, total - TITLE_END, '<div class="firma"><div class="nm">March Sandoval</div><div class="tg">Growth &amp; Brand Strategy</div></div>', False))
os.makedirs("placas6", exist_ok=True)
for pid, st, du, html, _ in OV:
    open(f"placas6/{pid}.html", "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{html}</body></html>")
subprocess.run(["node", "placas6.js"], check=True, env=dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules"))
hide = [(st, st + du) for pid, st, du, _, h in OV if h]
print("overlays", len(OV), "dur", round(total, 1))

# ---------- captions typewriter: Playfair + palabras clave en Montserrat Bold ----------
KEYS = {"ocupado","ocupada","producto","servicio","excelencia","clientes","recomienden","repitan","representa","culpables","redes","logo","inteligencia","artificial","nivel","paguen","increíble","montón","comunicación","diagnóstico","DM","Google","Maps","ruta","match","proyecto","dueños","negocio","hoy","funcionado","platicar","colaborar"}
def esc(s): return s.replace("{", "(").replace("}", ")")
def fmt(w):
    t = esc(w.strip()); core = t.strip(".,¿?¡!").lower()
    return "{\\fnMontserrat\\b1}" + t + "{\\r}" if core in {k.lower() for k in KEYS} else t
lines = []; cur = []
def flush():
    global cur
    if cur: lines.append(cur); cur = []
for w in words:
    ns, ne = remap(w["s"]), remap(w["e"])
    if ns is None or ne is None: flush(); continue
    w2 = dict(w, ns=ns, ne=ne)
    if cur:
        prev = cur[-1]; chars = sum(len(x["w"]) for x in cur)
        if (ne - cur[0]["ns"] > 3.0 or len(cur) >= 7 or chars > 34 or (ns - prev["ne"]) > 0.45
                or prev["w"].strip().endswith((".", "?", "!")) or (prev["w"].strip().endswith(",") and len(cur) >= 3)):
            flush()
    cur.append(w2)
flush()
def visible(s, e):
    for a, b in hide:
        if s < b - 0.1 and e > a + 0.1: return False
    return True
def ts(t): return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Playfair Display,64,&H00FFFFFF,&H00FFFFFF,&H82000000,&H96000000,0,0,0,0,100,100,0.2,0,1,1.6,2,2,150,230,760,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
nev = 0
for i, ln in enumerate(lines):
    s0 = ln[0]["ns"]; e0 = ln[-1]["ne"] + 0.35
    if i + 1 < len(lines): e0 = min(e0, lines[i + 1][0]["ns"])
    if not visible(s0, e0): continue
    for k in range(len(ln)):
        st = ln[k]["ns"]; en = ln[k + 1]["ns"] if k + 1 < len(ln) else e0
        if en - st < 0.03: continue
        txt = " ".join(fmt(x["w"]) for x in ln[:k + 1]) + ("{\\r}|" if k + 1 < len(ln) else "")
        ass += f"Dialogue: 0,{ts(st)},{ts(en)},Sub,,0,0,0,,{txt}\n"; nev += 1
open("subs6.ass", "w").write(ass)
print("captions", len(lines), "eventos", nev)

# ---------- planos: sin ampliar (máx 1.12) ----------
cuts = sorted(set([0.0] + seg_bounds[1:] + [round(l[0]["ns"], 3) for l in lines]))
shots = []; last = 0.0
for c in cuts[1:]:
    if (c - last >= 2.8 or c in seg_bounds) and c - last >= 1.0:
        shots.append([last, c]); last = c
shots.append([last, total])
SCALES = [1.0, 1.1, 1.04, 1.12, 1.0, 1.08]
plan = []
for i, (a, b) in enumerate(shots):
    s = 1.0 if i == 0 else SCALES[i % len(SCALES)]
    if plan and abs(plan[-1][2] - s) < 0.03: s = 1.1 if s < 1.05 else 1.0
    plan.append((a, b, s))
print("planos", len(plan))

# ---------- ffmpeg ----------
fc = ""; n = len(plan)
for i, (a, b, s) in enumerate(plan):
    D = max(b - a, 0.5); settle = 0.07 if a in seg_bounds and i > 0 else 0.035
    sexp = f"{s}*(1+0.022*t/{D:.3f})*(1+{settle}*max(0\\,1-t/0.4))"
    fc += (f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,"
           f"scale=w='2*round(1080*{sexp}/2)':h='2*round(1920*{sexp}/2)':eval=frame:flags=lanczos,"
           f"crop=1080:1920:x='(iw-1080)/2':y='min(max(560*iw/1080-560\\,0)\\,ih-1920)'[p{i}];")
fc += "".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[cc];"
cmd = ""
for bnd in seg_bounds[1:]:
    cmd += f"{bnd-0.13:.3f}-{bnd:.3f} [expr] gblur@whip sigma 'lerp(0.01,38,TI)';\n"
    cmd += f"{bnd:.3f}-{bnd+0.17:.3f} [expr] gblur@whip sigma 'lerp(38,0.01,TI)', [leave] gblur@whip sigma 0.01;\n"
open("whip6.cmd", "w").write(cmd)
fc += ("[cc]hqdn3d=2.5:2:4:4,eq=brightness=0.055:gamma=1.17:contrast=1.06:saturation=1.0,"
       "curves=master='0/0.02 0.2/0.21 0.5/0.55 0.8/0.84 1/1',colorbalance=rm=.03:bm=-.03:rh=.02:bh=-.03,"
       "unsharp=5:5:0.5,vignette=PI/6.5:mode=forward,sendcmd=f=whip6.cmd,gblur@whip=sigma=0.01:sigmaV=0.01:steps=2,"
       f"drawbox=x=0:y=0:w=1080:h=1920:color=black@0.55:t=fill:enable='between(t,{DIM[0]:.3f},{DIM[0]+DIM[1]:.3f})',"
       "fade=in:st=0:d=0.5,fade=out:st=%.3f:d=0.8[g];" % (total - 0.8))
cur = "[g]"; inputs = ["-i", "cut.mp4"]
for k, (pid, st, du, _, _) in enumerate(OV):
    inputs += ["-loop", "1", "-framerate", "30", "-t", f"{du:.3f}", "-i", f"placas6/{pid}.png"]
    slide = "" if pid in ("firma",) else f":y='-18*(1-min(1\\,(t-{st:.3f})/0.25))'"
    fc += f"[{k+1}:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,fade=out:st={du-0.25:.3f}:d=0.25:alpha=1,setpts=PTS+{st:.3f}/TB[o{k}];"
    fc += f"{cur}[o{k}]overlay=x=0{slide}:eof_action=pass:enable='between(t,{st:.3f},{st+du:.3f})'[c{k}];"; cur = f"[c{k}]"
fc += f"{cur}ass=subs6.ass:fontsdir=fonts[v]"
amap = ["-map", "0:a", "-c:a", "copy"]
music = sorted(glob.glob("music.*")); MI = len(OV) + 1
if music:
    inputs += ["-stream_loop", "-1", "-i", music[0]]
    fc += (f";[{MI}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume=0.16,afade=in:st=0:d=1.5,afade=out:st={total-3:.3f}:d=3[m];"
           f"[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600:makeup=1[md];"
           f"[v1][md]amix=inputs=2:duration=first:normalize=0[a]")
    amap = ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]; print("música:", music[0])
out = "Reel-March-Diagnostico-v6.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]", *amap,
                "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest", out], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out, "-vf", "fps=1/3.0,scale=270:480,tile=10x3", "-frames:v", "1", "-update", "1", "check6.png"], check=True)
print("ok", out)
