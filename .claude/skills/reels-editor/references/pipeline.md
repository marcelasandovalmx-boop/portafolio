# Pipeline técnico de reels (ffmpeg + libass + Playwright)

Todo esto se probó en el entorno cloud "march" (ffmpeg 6.1 con libass, Node 22 con Playwright en `/opt/node22/lib/node_modules`, Python 3 con faster-whisper, PIL solo en `/usr/local/bin/python3`). Script completo de ejemplo: `scripts/build_reel_template.py`.

## 1. Transcripción por palabra

```python
from faster_whisper import WhisperModel
import numpy as np, subprocess
pcm = subprocess.run(["ffmpeg","-v","error","-i","raw/v.mp4","-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
audio = np.frombuffer(pcm, np.float32)
m = WhisperModel("small", compute_type="int8")
segs, _ = m.transcribe(audio, language="es", word_timestamps=True)
```
Guarda `[{ "words": [{"w": " palabra", "s": 1.23, "e": 1.56}, ...]}]`. Pasar numpy evita el error `metadata_errors` de PyAV. El modelo se descarga de Hugging Face (hosts `huggingface.co`, `cdn.hf.co`, `cas-*.xethub.hf.co` permitidos).

## 2. Corte a límites de palabra

```python
def snap_end(t):            # fin de palabra <= t+0.25, más una cola que no invada la siguiente palabra
    c = [w["e"] for w in words if w["e"] <= t + 0.25]
    e = max(c); nxt = [w["s"] for w in words if w["s"] >= e]
    return e + min(0.18, max(0.0, min(nxt) - e))
```
Si la tolerancia incluye la primera palabra de la siguiente frase ("recomienden. A lo"), baja el tiempo del tramo, no la tolerancia.

Corte con audio fiable: `trim/atrim + setpts/asetpts + concat=n=N:v=1:a=1`, `libx264 crf 18`, AAC 160k.

## 3. Mapa de tiempos

`remap(t_original) -> t_nuevo` recorriendo `KEEP` acumulando duraciones; devuelve `None` si la palabra quedó fuera. Todo (subtítulos, placas, cortes) se expresa en la línea nueva. Guarda `seg_bounds` (inicio de cada bloque en la línea nueva): ahí van los whips.

## 4. Subtítulos ASS

- Estilo base por frase: `Playfair Display, 62, blanco, Outline 1.6 (&H82000000), Shadow 2, Alignment 2, MarginL 150, MarginR 230, MarginV 700`. El margen derecho mayor evita la columna de iconos de Instagram.
- Fuentes: `ass=subs.ass:fontsdir=fonts` con las TTF copiadas a `fonts/` (Playfair, Montserrat Bold/ExtraBold). Nombre de familia tal cual el TTF: `Montserrat ExtraBold`, `Montserrat Bold`, `Playfair Display`.
- Chunking por frase: máximo 7 u 8 palabras, 40 caracteres, 3 s; corta en `. ? !`, en coma si ya hay 3 o 4 palabras, y en pausas > 0.45 s. Extiende el fin de cada línea hasta el inicio de la siguiente (máximo +0.35 s).
- Palabra a palabra: un `Dialogue` por palabra desde su inicio hasta el inicio de la siguiente (máximo 1.4 s), `{\an5\pos(500,1130)\fscx84\fscy84\t(0,90,\fscx106\fscy106)\t(90,170,\fscx100\fscy100)}`.
- Typewriter por palabra: un evento por palabra acumulando el texto previo y un `|` final mientras falten palabras.
- Palabras clave: `{\fnMontserrat Bold}palabra{\r}` o color `{\c&H3F7DFA&}` (BGR de `#fa7d3f`).
- Oculta las líneas que se traslapen con placas, tarjetas o polaroids (`visible()` con tolerancia 0.1 a 0.15 s).

## 5. Placas, chips, tarjetas y polaroids (Playwright)

HTML 1080×1920 con `body{background:transparent}`; fuentes con **ruta absoluta** en `@font-face` (una ruta relativa desde `placasN/x.html` apunta al directorio equivocado y Chrome cae a una serif genérica). Captura con `page.screenshot({omitBackground:true})`. Script: `placas.js` recorre `placasN/*.html`.

En ffmpeg cada PNG entra como input en bucle:
```
-loop 1 -framerate 30 -t DUR -i placasN/id.png
[k:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,fade=out:st=DUR-0.25:d=0.25:alpha=1,setpts=PTS+START/TB[ok];
[prev][ok]overlay=x=0:y='-18*(1-min(1\,(t-START)/0.25))':eof_action=pass:enable='between(t,START,START+DUR)'[next];
```
El `y` con expresión da una entrada deslizada de 18 px. Para tarjetas opacas usa fades de 0.12 s sin deslizamiento. **Trampa**: `movie=png` de un solo cuadro + `fade=in` queda transparente para siempre (la única imagen tiene alpha 0); por eso `-loop 1`.

Momento "dim": `drawbox=x=0:y=0:w=1080:h=1920:color=black@0.55:t=fill:enable='between(t,a,b)'` antes de las placas.

## 6. Planos con asentamiento y push-in (sin xfade)

```
[0:v]trim=start=A:end=B,setpts=PTS-STARTPTS,
scale=w='2*round(1080*S*(1+0.022*t/D)*(1+0.05*max(0\,1-t/0.4))/2)':h='2*round(1920*.../2)':eval=frame:flags=lanczos,
crop=1080:1920:x='(iw-1080)/2':y='min(max(560*iw/1080-560\,0)\,ih-1920)'[pN];
```
`560` es la altura de la cara en el origen: la mantiene fija al hacer zoom. Escalas: alterna 1.0 / 1.08 / 1.04 / 1.12; nunca más de 1.12 con fuente 1080p. Asentamiento 0.07 en saltos de bloque, 0.035 dentro del bloque. Luego `concat=n=N:v=1:a=0`.

**No uses `xfade`** entre planos: acorta la duración (a 83 s de 93) y desincroniza con el audio; además con `-shortest` corta el final.

## 7. Whip de desenfoque en saltos de bloque

```
sendcmd=f=whip.cmd,gblur@whip=sigma=0.01:sigmaV=0.01:steps=2
```
`whip.cmd`:
```
27.890-28.020 [expr] gblur@whip sigma 'lerp(0.01,38,TI)';
28.020-28.190 [expr] gblur@whip sigma 'lerp(38,0.01,TI)', [leave] gblur@whip sigma 0.01;
```
(0.13 s antes del corte sube, 0.17 s después baja). Horizontal porque `sigmaV` queda en 0.01.

## 8. Color y limpieza

Fuente oscura/ruidosa (cámara frontal de noche):
```
hqdn3d=2.5:2:4:4,eq=brightness=0.055:gamma=1.17:contrast=1.06:saturation=1.0,
curves=master='0/0.02 0.2/0.21 0.5/0.55 0.8/0.84 1/1',colorbalance=rm=.03:bm=-.03:rh=.02:bh=-.03,
unsharp=5:5:0.5,vignette=PI/6.5:mode=forward,fade=in:st=0:d=0.5,fade=out:st=T-0.8:d=0.8
```
Grade "Tapioca" (cálido, negros levantados): `curves=master='0/0.035 0.25/0.24 0.5/0.52 0.75/0.78 1/0.985',eq=saturation=0.93:contrast=1.03,colorbalance=rs=.03:bs=-.04:rm=.02:bm=-.03`.
Si el video llega ya corregido en color, no apliques `eq/curves/colorbalance`; como mucho `hqdn3d` suave.

## 9. Música con ducking

```
[M:a]atrim=0:T,asetpts=PTS-STARTPTS,volume=0.16,afade=in:st=0:d=1.5,afade=out:st=T-3:d=3[m];
[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600:makeup=1[md];
[v1][md]amix=inputs=2:duration=first:normalize=0[a]
```
Entrada de música con `-stream_loop -1 -i music.mp3`. Ajusta `volume` entre 0.12 y 0.2 según la pista.

## 10. Export y revisión

```
-c:v libx264 -preset slow -crf 16 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -shortest
```
Revisión: hoja `fps=1/3,scale=270:480,tile=10x3 -frames:v 1 -update 1`; cuadros a tamaño real con `-ss T -i out.mp4 -frames:v 1 -update 1`; tira de cortes `select='lt(n,13)',tile=13x1 -frames:v 1`; máscara de zonas seguras con `drawbox ... color=red@0.25:t=fill`; `ffprobe` duración y `nb_frames` (= 30 × segundos).

## 11. Bajar referencias de Instagram

`yt-dlp -f "bv*+ba/b" --merge-output-format mp4 -o ID.mp4 https://www.instagram.com/reel/ID/` (instalado con pip). El video vive en `scontent-ord5-*.cdninstagram.com`; si aparece otro host, pedir permiso para agregarlo al entorno. `--dump-json` da autor y caption. Cortes: `select='gt(scene,0.25)',showinfo` y leer `pts_time`.

## 12. Testimonial con contorno, placa y karaoke (compositor en Python)

Cuando el sistema de texto necesita caja redondeada con palabras que se pintan y contorno de sticker, ASS y overlays de PNG se quedan cortos. Se arma en dos etapas:

1. **Base** (`render_segs.py`): un ffmpeg por tramo con `-ss/-t` de entrada, `trim=end_frame`, `crop`, `scale=1080:1920`, y se unen con el demuxer `concat -c copy`. Abrir todos los tramos 4K en un solo `filter_complex` mata el proceso por memoria.
2. **Compositor** (`comp.py`, `/usr/bin/python3` con PIL, numpy y onnxruntime): lee la base por pipe en rgb24, compone y escribe a libx264 con el audio ya cortado.

Piezas:
- **Material iPhone HDR** (HEVC 10 bit, `arib-std-b67`, rotación −90): convertir con `zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p` **después** de recortar y escalar (cuatro veces más rápido que hacerlo en 4K). Con fuente 4K se puede acercar hasta 1.3 sin perder nitidez en 1080.
- **Contorno**: matte con MODNet (`huggingface.co/Xenova/modnet`, `onnx/model.onnx`, 25 MB, entrada 512×896 normalizada a −1..1). Umbral 0.5, `MaxFilter(17)` a media resolución, desenfoque y anillo = dilatado × (1 − interior). Calcular un cuadro sí y uno no y promediar con el anterior para que no vibre. Cerca de 0.7 s por inferencia en 4 núcleos.
- **Corte suave**: al quitar silencios sin cambiar de encuadre, mezclar los 3 primeros cuadros del tramo nuevo con el último del anterior (25, 50 y 75 %). El salto deja de verse. Los cortes de contenido sí cambian de encuadre (1.0 / 1.14 / 1.28) y van secos.
- **Silencios**: `silencedetect=noise=-30dB:d=0.35`. La voz de March fuera de cámara llega por debajo del umbral, así que **no se recortan silencios dentro de sus preguntas** o se pierden palabras completas.
- **Verificación de cortes**: transcribir el audio ya cortado con `faster-whisper large-v3` y leerlo de corrido. Si un corte mordió una palabra, aparece como frase rara. Esa misma transcripción da los tiempos por palabra para los captions.
- **Captions**: máximo 23 caracteres por caja con Montserrat ExtraBold 52 px para no entrar a la columna de iconos (caja de hasta 780 px centrada).
- Usuarios de redes y dominios que suenan en el audio no se escriben hasta que March confirme la ortografía.

## 13. Palabras clave en bloque, letras que navegan y efectos de sonido (v2 del testimonial, nov 2026)

Pedido de March sobre el reel de Mario: placa de nombre más grande y centrada, palabras clave que pausen el subtítulo y aparezcan en grande, letras que "avanzan en fila de derecha a izquierda", y efectos de sonido. La música la pone ella. Todo vive en `scripts/testimonial/comp2.py` y `sfx.py`.

- **Placa**: caja blanca centrada con el nombre en tipografía ancha y pesada (ella usa **Horizon**; mientras no mande el archivo se usa Unbounded 900 de Google Fonts, variable `FUENTE_NOMBRE`). Debajo, pleca naranja centrada que se abre desde el centro, con el cargo en Montserrat Bold blanco. Ancho total menor a 800 px para no tocar la columna de iconos.
- **Bloque de palabra clave**: sustituye al caption mientras dura. Caja naranja con texto blanco (o blanca con texto naranja para el "antes"), cada línea ajustada al ancho común como lockup, tope 132 px. Entra con rebote y las letras llegan una por una desde la derecha (28 ms entre letras, 0.24 s de viaje, recortadas al borde de la caja). De 5 a 7 momentos por reel; se eligen resultados y lo que se quiere potenciar, siempre con palabras que la persona sí dijo.
- **Bloques encadenados** ("seguimiento, planificación, estrategia"; "cero alcance" a "cifras inimaginables"): el bloque se sostiene hasta que entra el siguiente para que no parpadee el caption en medio.
- **Efectos de sonido sintetizados** con numpy (sin librerías con licencia): `pop` (seno que cae de 560 a 190 Hz), `tick` (ráfaga de 18 ms), `whoosh` (ruido con pasa banda que barre), `swipe` (barrido descendente al entrar el contorno) e `impacto` (seno grave más golpe). Pico de la pista cerca de −7.5 dBFS contra voz a −1; se mezclan con `amix normalize=0` y `alimiter`. No se pueden escuchar desde aquí: avisar a March para que valide niveles.
- **Render por tramos en paralelo**: `comp2.py t_ini t_fin salida` en tres procesos cortados en cortes secos que no caigan dentro de una pregunta, y unión con `concat -c copy` (`-video_track_timescale 15360` en todos). Baja de 22 a 9 minutos.
