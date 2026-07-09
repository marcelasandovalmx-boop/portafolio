# Portafolio visual de Orangy Integrated Marketing

Sitio one-page (HTML/CSS/JS en un solo archivo: `orangy-portafolio-v2.html`) que muestra el trabajo de identidades visuales de Orangy. Dueña: Marcela Sandoval (March), directora de Orangy, CDMX.

## Reglas de trabajo con March (IMPORTANTES)

1. **El orden que ella indica es sagrado.** Si manda imágenes en un orden (PDF, lista), ese es el orden de los slides. Nunca curar/reordenar por cuenta propia.
2. **Ante la duda, preguntar ANTES de hacer.** No sustituir contenido por "equivalentes".
3. Es diseñadora senior — hablar de diseño de tú a tú, con criterio de brand manager AAA, pero ella decide.

## Sistema de diseño (NO modificar sin su OK)

- **Tipografías: SOLO Montserrat (cuerpo/etiquetas) y Deutschlander (títulos).** Deutschlander se carga por @font-face desde `fonts/Deutschlander.ttf` (archivo PENDIENTE de conseguir; mientras, fallback Montserrat 800). Nunca serif, nunca otra fuente.
- **Paleta oficial:** naranja `#E5501C` (solo acento), gris `#545454`, gris claro `#A6A6A6` (solo si es necesario). Fondo papel `#F4F1EB`, hairlines `#E3DED5`, footer `#3D3D3D`.
- **Barra de color segmentada** (naranja→rojo→teal→aqua) = firma visual de March; aparece en hero, manifiesto y footer, animada al aparecer.
- **Máximo un bloque naranja sólido** (el marquee). Elegancia = contraste de escala, no de peso; nada de "tics de IA" (números fantasma, fade-ups excesivos, eyebrows en todo).
- **Slides de casos: 4:5, imagen llenando el marco completo** (cover crop centrado en el sujeto). Nada de bandas de color/aire. Excepción: logos sobre su propio color de fondo (ej. slide 1 de Lucía Li).

## Estructura del sitio

Hero (Deutschlander gigante + barra) → Marquee naranja → Manifiesto → Brand Intelligence (metodología, 4 puntos) → Tríada "Primero entendemos / Luego ordenamos / Después activamos" → **5 casos** con carrusel (scroll-snap, flechas, arrastre, contador) → Grid "Más proyectos" → Cinta de logos gris → Qué construimos (4 pilares) → Footer con CTA "Solicitar diagnóstico" y cierre "No por velocidad. Por dirección."

### Casos (orden y contenido aprobados por March)

1. **Xcaanda'** — Panadería artesanal · 7 slides (bolsas, letrero, panadera, 3 posts, collage stickers)
2. **Kaleia** — Intérprete floral · 7 slides (fachada, tarjetas, ramo, mandil, 3 posts) · Resultado: llegó a Costco
3. **Lucía Li** — Skincare de lujo · 6 slides (logo azul, productos, post, arco, bolsa, doctora)
4. **Xipotle** — Salsas mexicanas · 6 slides (extraídos del brandbook; orden NO revisado aún por March)
5. **GAMA IP** — Firma legal · 6 slides (extraídos del brandbook; orden NO revisado aún por March)

Imágenes en `img/caso-1/` … `img/caso-5/`, logos de la cinta en `img/logos/`, logo Orangy en `img/logo-orangy.png`.

## Pendientes

- [ ] **Grid "Más proyectos"**: falta imagen + industria de Weecom, Kalu, LC Agency y Pikipuki (sus brandbooks PDF los tiene March; extraer 1 imagen por cliente con su aprobación). Actualizar los `mini-proyecto` del HTML.
- [ ] **Fuente Deutschlander**: conseguir el .ttf y ponerlo en `fonts/Deutschlander.ttf`.
- [ ] Revisar con March el orden de slides de Xipotle y GAMA IP.
- [ ] Datos de resultado por caso (números duros para los contadores animados, si los hay).
- [ ] Al publicar: renombrar a `index.html`, deploy en Netlify/Vercel, y conectar dominio (posible subdominio de orangy.com.mx).

## Técnica

- Todo inline en un archivo; sin dependencias externas salvo Google Fonts (Montserrat).
- Carruseles: scroll-snap nativo + JS (arrastre pointer, teclado, contador). Nav se oculta al bajar. Reveals con IntersectionObserver, easing `cubic-bezier(.16,1,.3,1)`. `prefers-reduced-motion` respetado.
- Cinta de logos: filtro CSS `brightness(0) invert(.47)` = gris medio uniforme; hover restaura.
- Para procesar imágenes nuevas de casos: recorte cover a 4:5 centrado en el sujeto, JPG calidad 90, ~1400px+ de ancho.
