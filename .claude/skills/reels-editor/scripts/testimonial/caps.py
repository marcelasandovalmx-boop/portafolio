import json, re
ws = json.load(open('cut-words.json'))
edl = json.load(open('edl.json'))
# 1) limpieza de texto
out = []
low_next = False
for w in ws:
    t = w['w'].strip()
    if t.endswith('...'):
        t = t[:-3]; nxt_low = True
    else: nxt_low = False
    if low_next and t: t = t[0].lower() + t[1:]
    prev_dots = low_next
    low_next = nxt_low
    if out and prev_dots and out[-1]['w'].lower() == t.lower(): continue
    out.append(dict(w=t, s=w['s'], e=w['e']))
FIX = {'le': None}
txt = ' '.join(o['w'] for o in out)
# correcciones puntuales (por contexto)
for i, o in enumerate(out):
    if o['w'] == 'le' and out[i+1]['w'].startswith('diría') and out[i-1]['w'] == 'que': o['w'] = 'les'
# web y usuario: se arman a mano
res = []
i = 0
while i < len(out):
    o = out[i]
    if o['w'].lower().startswith('mario') and i + 2 < len(out) and 'info' in out[i+2]['w']:
        res.append(dict(w='mariobarrera.info', s=o['s'], e=out[i+2]['e'], solo=True)); i += 3; continue
    if 'Frenjer' in o['w'] or 'FrenjerMB' in o['w']:
        i += 1; continue   # usuario de redes: pendiente de confirmar, no se escribe
    res.append(o); i += 1
out = res
# 2) cortes de locutor (tiempos nuevos donde cambia quién habla)
cambios = sorted({round(x, 2) for p in edl['preg'] for x in p})
CONECT = {'y','de','que','a','el','la','en','con','por','los','las','un','una','es','se','te','mi','o','del','al','su','lo','como','muy','más','no','sí','e','tu','le','les','me','nos','ha','he','pero','porque','para','sobre','todo'}
MAXC, MAXW = 23, 5
chunks = []; cur = []
def flush():
    global cur
    if cur: chunks.append(cur); cur = []
for k, o in enumerate(out):
    if o.get('solo'):
        flush(); chunks.append([o]); continue
    # cambio de locutor entre la palabra anterior y esta
    if cur and any(cur[-1]['s'] + 0.3 < c <= o['s'] + 0.05 for c in cambios): flush()
    if cur and o['s'] - cur[-1]['e'] > 1.3: flush()
    cand = ' '.join(x['w'] for x in cur + [o])
    if cur and (len(cand) > MAXC or len(cur) >= MAXW):
        # no dejar conector colgando al final
        mov = []
        comas = [q for q, x in enumerate(cur[:-1]) if x['w'].endswith(',')]
        if comas:
            mov = cur[comas[-1] + 1:]; cur = cur[:comas[-1] + 1]
        while len(cur) > 1 and re.sub(r'[^\wáéíóúñ]', '', cur[-1]['w'].lower()) in CONECT and not re.search(r'[,.?!]$', cur[-1]['w']):
            mov.insert(0, cur.pop())
        flush(); cur = mov
    cur.append(o)
    if re.search(r'[.?!]$', o['w']): flush()
    elif o['w'].endswith(',') and len(cur) >= 2 and len(' '.join(x['w'] for x in cur)) >= 12: flush()
flush()
# 3) tiempos
caps = []
for j, c in enumerate(chunks):
    s = max(0, c[0]['s'] - 0.06)
    e_nat = c[-1]['e'] + 0.45
    if j + 1 < len(chunks):
        ns = chunks[j+1][0]['s'] - 0.06
        e = ns if ns - c[-1]['e'] < 0.9 else e_nat
    else: e = min(e_nat, edl['dur'] - 0.35)
    caps.append(dict(s=round(s, 3), e=round(e, 3), words=[dict(w=x['w'], s=x['s']) for x in c]))
json.dump(caps, open('captions.json', 'w'), ensure_ascii=False, indent=0)
print(len(caps), 'chunks; más ancho:', max(len(' '.join(w['w'] for w in c['words'])) for c in caps))
print(' | '.join(f"{c['s']:.1f} " + ' '.join(w['w'] for w in c['words']) for c in caps))
