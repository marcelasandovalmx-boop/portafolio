import json, subprocess, os
edl = json.load(open('edl.json'))
TM = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
lst = []
for i, s in enumerate(edl['segs']):
    cw, ch, x0, y0 = s['crop']; n = round(s['d'] * 30)
    out = f'segs/s{i:02d}.mp4'
    vf = f"trim=end_frame={n},setpts=PTS-STARTPTS,crop={cw}:{ch}:{x0}:{y0},scale=1080:1920:flags=lanczos,setsar=1,{TM},eq=saturation=0.96"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{s['a']:.4f}", '-t', f"{s['d'] + 0.3:.4f}", '-i', '../src/mario.mov', '-an',
        '-vf', vf, '-r', '30', '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-pix_fmt', 'yuv420p',
        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-video_track_timescale', '15360', out], check=True)
    nb = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    print(i, n, nb, flush=True)
    assert int(nb) == n, (i, n, nb)
    lst.append(f"file '{out}'")
open('segs.txt', 'w').write('\n'.join(lst) + '\n')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'segs.txt', '-c', 'copy', 'base_v.mp4'], check=True)
print('base ok')
