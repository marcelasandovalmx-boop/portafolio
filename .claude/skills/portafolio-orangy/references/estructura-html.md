# Snippets de `index.html`

Copia el patrón exacto; los atributos `srcset`/`sizes` deben coincidir con los demás slides.

## Slide de un caso
```html
<div class="slide"><img src="img/caso-3/slide-2.jpg" srcset="img/caso-3/slide-2-sm.jpg 800w, img/caso-3/slide-2.jpg 1620w" sizes="(max-width:640px) 78vw, 420px" alt="Lucía Li — post Glow Up" loading="lazy"></div>
```
- `src` = full-res (la usa el lightbox).
- `alt` = "Marca — qué se ve", en español. Escapa `&` como `&amp;`.

## Caso completo
```html
<!-- Caso N: Marca -->
<article class="caso reveal">
  <div class="caso-head">
    <h3><span class="idx">0N</span>Marca</h3>
    <p class="industria">Industria</p>
  </div>
  <p class="caso-desc">Una o dos líneas, con copy aprobada por March.</p>
  <div class="carrusel">
    <div class="pista" tabindex="0" aria-label="Carrusel Marca">
      <!-- slides -->
    </div>
    <div class="carrusel-ui">
      <button class="flecha prev" aria-label="Slide anterior">←</button>
      <button class="flecha next" aria-label="Slide siguiente">→</button>
      <p class="contador">1 / 5</p>
    </div>
  </div>
  <div class="caso-metricas">
    <p class="metrica"><span class="mlabel">Resultado</span>Texto cualitativo o con dato.</p>
    <p class="metrica"><span class="mlabel">Proyección</span><span class="dato">+<span class="dato-num" data-val="25">0</span>–<span class="dato-num" data-val="30">0</span>%</span> en ventas…</p>
  </div>
</article>
```
- El contador lo actualiza el JS al cargar; el texto inicial no importa.
- Etiquetas válidas en `mlabel`: Resultado, Proyección, Siguiente etapa.

## Slide de "Más proyectos"
```html
<div class="slide"><img src="img/otros/kalu.jpg" srcset="img/otros/kalu-sm.jpg 800w, img/otros/kalu.jpg 1620w" sizes="(max-width:640px) 78vw, 420px" alt="Kalu Cakes &amp; More — identidad y empaque" loading="lazy"></div>
```
Va dentro de `<section class="mas">` → `.pista`.
