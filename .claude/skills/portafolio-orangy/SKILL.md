---
name: portafolio-orangy
description: Mantiene y actualiza el portafolio web de Orangy Integrated Marketing (index.html one-page de March / Marcela Sandoval) — agregar o reemplazar slides de casos, sumar un caso o proyecto a "Más proyectos", procesar imágenes o PDFs que manda March a 4:5, cambiar copy, cifras de resultados/proyecciones, logos de la cinta de marcas o la página de enlaces /links/. Úsala siempre que March pida cualquier cambio al portafolio, mande imágenes o un PDF "para el portafolio", mencione un caso (Xcaanda', Kaleia, Lucía Li, Xipotle, GAMA IP, Kalu, JF Group, LC Agency, Tactrick, PikiPuki, Weecom), slides, carrusel, métricas, la cinta de marcas o el linktree — aunque no diga la palabra "portafolio".
---

# Portafolio Orangy

Sitio one-page de Orangy Integrated Marketing (CDMX) que muestra el trabajo de identidades visuales. Todo vive en un solo `index.html` (HTML/CSS/JS inline) más la carpeta `img/`. La dueña es March (Marcela Sandoval), directora de Orangy y diseñadora senior.

**Si existe `CLAUDE.md` en el repo, léelo primero**: es la bitácora viva (casos actuales, cifras, decisiones, pendientes) y manda sobre lo que diga esta skill si difieren. Al terminar un cambio, actualízalo para que la siguiente sesión herede el contexto.

## Cómo trabajar con March

Estas reglas existen porque March cuida su trabajo como brand manager AAA; romperlas le cuesta tiempo y confianza.

1. **El orden que ella manda es sagrado.** Si las imágenes llegan en un orden (páginas de PDF, lista, numeración en el chat), ese es el orden de los slides. No reordenes "para que fluya mejor": la curaduría ya la hizo ella.
2. **Ante la duda, pregunta antes de hacer.** No sustituyas una imagen, una frase o una cifra por un "equivalente". Si falta algo, dilo y espera.
3. **Nunca inventes cifras ni copy.** Los números de resultados son solo los que ella da; la copy sale del brochure oficial o de lo que ella escribe. Distingue *Resultado* (logrado) de *Proyección* (esperado): confundirlos es una promesa falsa ante un cliente.
4. **Las imágenes pegadas en el chat no llegan como archivo.** Si dice que mandó imágenes y no aparecen en disco, pídele un PDF o un enlace de Drive (puedes buscarlo con el conector de Google Drive si está disponible).
5. Habla de diseño de tú a tú, con criterio; da tu recomendación, pero ella decide.

## Sistema de diseño (no modificar sin su OK)

Resumen; el detalle está en `references/sistema-diseno.md`.

- Tipografía: **solo Montserrat** (títulos 800, cuerpo 400–700). Nada de serif ni otra fuente.
- Paleta: naranja `#E5501C` (solo acento), gris `#545454`, gris claro `#A6A6A6`, papel `#F4F1EB`, hairlines `#E3DED5`, footer `#3D3D3D`.
- Barra segmentada (firma de March): `#E5501C` 48% → `#F27405` 15.5% → `#32A6A6` 27.4% → `#99E9F2` 6.8%.
- Un solo bloque naranja sólido (el marquee). Elegancia por contraste de escala; nada de "tics de IA" (números fantasma, fade-ups excesivos, eyebrows en todo).

## Flujo: imágenes nuevas para un caso o "Más proyectos"

1. **Identifica destino y orden.** ¿Qué caso (`img/caso-N/`) o si va a `img/otros/`? ¿En qué posición exacta? Si no está claro, pregunta.
2. **Procesa con el script** (no lo hagas a mano; garantiza los tamaños que espera el `srcset`):

   ```bash
   # PDF: cada página -> un slide, en el orden del PDF
   python3 .claude/skills/portafolio-orangy/scripts/procesar_slides.py pdf ruta/portafolio.pdf img/caso-3 --desde 1
   # Imágenes sueltas, en el orden en que se pasan
   python3 .claude/skills/portafolio-orangy/scripts/procesar_slides.py img foto1.jpg foto2.png --salida img/caso-2 --desde 4
   # Proyecto de "Más proyectos" con nombre fijo
   python3 .claude/skills/portafolio-orangy/scripts/procesar_slides.py img kalu.png --salida img/otros --nombre kalu
   ```

   Genera `slide-N.jpg` (1620×2025, q90) y `slide-N-sm.jpg` (800×1000, q82). El recorte es *cover* 4:5 centrado; usa `--foco x,y` (0–1) cuando el sujeto no está al centro, y `--fondo "#hex"` con `--contener` para logos que deben verse completos sobre su propio color (ej. slide 1 de Lucía Li). Si una imagen sale cortando el sujeto, revísala visualmente (Read sobre el JPG) antes de seguir.
   Insertar en medio de un caso implica renumerar: renombra primero los archivos posteriores (de atrás hacia adelante) para no pisarlos.
3. **Edita el HTML** siguiendo los snippets de `references/estructura-html.md`: un `<div class="slide">` por imagen, con `src` a la full-res (la usa el lightbox), `srcset`/`sizes` idénticos a los demás y un `alt` descriptivo "Marca — qué se ve".
4. **Verifica**: `python3 .claude/skills/portafolio-orangy/scripts/verificar.py` (rutas existentes, versiones `-sm`, proporción 4:5, solo Montserrat). Si puedes, abre el sitio con Playwright y toma una captura del carrusel tocado.
5. **Actualiza `CLAUDE.md`** (lista de slides del caso, decisiones nuevas) y haz commit con un mensaje en español que diga qué cambió.

## Flujo: copy y métricas

- La copy sale del brochure; frases clave y contacto en `references/copy-y-casos.md`.
- Cada caso tiene `caso-desc` (una o dos líneas) y `caso-metricas` con etiquetas **Resultado**, **Proyección** y/o **Siguiente etapa**. Los números van en `<span class="dato">` con `<span class="dato-num" data-val="N">0</span>` para el contador animado (el texto inicial es `0`, el valor real en `data-val`).
- Antes de tocar una cifra, confirma cuál etiqueta le corresponde. Ejemplo real: en Kaleia, Costco es contexto (ya estaban ahí), no resultado de Orangy.

## Otras piezas

- **Cinta de marcas** (`img/logos/*.png`): PNG transparentes; el CSS los tiñe a gris con `brightness(0) invert(.47)`. Orden = el que mande March.
- **Página de enlaces** (`links/index.html`): un solo botón naranja sólido (Ver portafolio). Hay botones comentados para redes esperando URLs exactas de March; nunca las adivines.
- **SEO/compartir**: `og:image` usa URL absoluta; si cambia el dominio, actualízala. GA4 `G-RX21D5W3EB` vive en ambos HTML; no lo quites.

## Publicar

Commit y push a la rama indicada. El sitio se publica con GitHub Pages o Netlify (ver pendientes en `CLAUDE.md`). No abras PR a menos que March lo pida.
