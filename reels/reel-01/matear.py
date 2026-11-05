# Recorte con RobustVideoMatting: guarda el mate (alfa) y el primer plano por separado
import sys, time, av, torch, numpy as np
sys.path.insert(0, '/root/rvm'); from model import MattingNetwork
torch.set_num_threads(4)
src, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
m = MattingNetwork('mobilenetv3').eval(); m.load_state_dict(torch.load('/root/rvm/rvm_mobilenetv3.pth', map_location='cpu'))
inp = av.open(src); vs = inp.streams.video[0]
def mk(path, pix, crf):
    c = av.open(path, 'w'); s = c.add_stream('ffv1' if pix == 'gray' else 'libx264', rate=30)
    s.width, s.height, s.pix_fmt = 1080, 1920, pix
    if crf: s.options = {'crf': str(crf), 'preset': 'medium'}
    return c, s
ca, sa = mk(out + '-alfa.mkv', 'gray', None); cf, sf = mk(out + '-frente.mp4', 'yuv444p', 10)
rec = [None]*4; n = 0; t0 = time.time()
with torch.no_grad():
    for fr in inp.decode(vs):
        if fr.time is not None and fr.time >= dur: break
        if fr.time is not None and fr.time < float(__import__('os').environ.get('INICIO', 0)) - 1e-3: continue
        x = torch.from_numpy(fr.to_ndarray(format='rgb24')).permute(2,0,1)[None].float()/255
        fgr, pha, *rec = m(x, *rec, downsample_ratio=float(__import__("os").environ.get("DR","0.25")))
        a = (pha[0,0].clamp(0,1).numpy()*255+.5).astype(np.uint8)
        f = (fgr[0].permute(1,2,0).clamp(0,1).numpy()*255+.5).astype(np.uint8)
        for p in sa.encode(av.VideoFrame.from_ndarray(a, format='gray')): ca.mux(p)
        for p in sf.encode(av.VideoFrame.from_ndarray(f, format='rgb24')): cf.mux(p)
        n += 1
        if n % 300 == 0: print(f'{n} fotogramas · {(time.time()-t0)/n:.2f} s/fotograma', flush=True)
for c, s in ((ca, sa), (cf, sf)):
    for p in s.encode(): c.mux(p)
    c.close()
print(f'listo: {n} fotogramas en {time.time()-t0:.0f} s ({(time.time()-t0)/max(n,1):.2f} s/fotograma)')
