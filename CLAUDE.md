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

### Casos (orden y contenido aprobados por March — PDFs curados, jul 2026, 5 slides c/u)

March mandó un PDF de 5 páginas por marca; el orden de páginas = orden de slides (regla sagrada). Las páginas ya venían en 4:5 (810×1012); se extrajeron a JPG q90 de 1620px sin recorte.

1. **Xcaanda'** — Panadería artesanal · logo rojo, bolsas, stickers, letrero, collage posts
2. **Kaleia** — Intérprete floral · logo azul, fachada, tarjetas, mandil, collage posts · Resultado: llegó a Costco
3. **Lucía Li** — Skincare de lujo · logo azul claro, post Glow-Up, productos, bolsa, aplicación
4. **Xipotle** — Salsas mexicanas · logo morado, botella, post recetas, post pasta, etiqueta colgante
5. **GAMA IP** — Firma legal · logo negro, tarjetas, piezas digitales, folder, fachada

Imágenes en `img/caso-1/slide-1..5.jpg` … `img/caso-5/slide-1..5.jpg`. Logos de la cinta en `img/logos/` y logo Orangy en `img/logo-orangy.png` (ambos PENDIENTES; mientras, la cinta y el nav usan wordmarks de texto).

## Pendientes

- [ ] **Grid "Más proyectos"**: falta imagen + industria de Weecom, Kalu, LC Agency y Pikipuki (sus brandbooks PDF los tiene March; extraer 1 imagen por cliente con su aprobación). Actualizar los `mini-proyecto` del HTML (hoy son placeholders de texto).
- [ ] **Fuente Deutschlander**: conseguir el .ttf y ponerlo en `fonts/Deutschlander.ttf`.
- [ ] **Cinta de logos**: conseguir los archivos de logo (PNG/SVG) para `img/logos/` y el logo Orangy (`img/logo-orangy.png`); hoy son wordmarks de texto.
- [ ] **Revisar con March la copy** de hero, manifiesto, metodología, tríada y pilares (redactada en la reconstrucción de jul 2026; el HTML original no llegó al repo).
- [ ] Confirmar el correo del CTA "Solicitar diagnóstico" (hoy apunta a hola@orangy.com.mx).
- [ ] Datos de resultado por caso (números duros para los contadores animados, si los hay).
- [ ] Al publicar: renombrar a `index.html`, deploy en Netlify/Vercel, y conectar dominio (posible subdominio de orangy.com.mx).

## Técnica

- Todo inline en un archivo; sin dependencias externas salvo Google Fonts (Montserrat).
- Carruseles: scroll-snap nativo + JS (arrastre pointer, teclado, contador). Nav se oculta al bajar. Reveals con IntersectionObserver, easing `cubic-bezier(.16,1,.3,1)`. `prefers-reduced-motion` respetado.
- Cinta de logos: filtro CSS `brightness(0) invert(.47)` = gris medio uniforme; hover restaura.
- Para procesar imágenes nuevas de casos: recorte cover a 4:5 centrado en el sujeto, JPG calidad 90, ~1400px+ de ancho.
