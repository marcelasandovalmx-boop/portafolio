import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
src, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
pcm = subprocess.run(["ffmpeg","-v","error","-i",src,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
audio = np.frombuffer(pcm, np.float32)
m = WhisperModel(model, compute_type="int8")
segs, _ = m.transcribe(audio, language="es", word_timestamps=True, beam_size=5,
    initial_prompt="Entrevista de March Sandoval, de Orangy, a Mario Barrera, aliado estratégico de Orangy.")
res=[]
for s in segs:
    res.append({"s":s.start,"e":s.end,"text":s.text,"words":[{"w":w.word,"s":round(w.start,2),"e":round(w.end,2)} for w in s.words]})
json.dump(res, open(out,"w"), ensure_ascii=False)
print("ok", len(res))
