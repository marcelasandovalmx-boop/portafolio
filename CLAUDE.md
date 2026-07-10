# Portafolio visual de Orangy Integrated Marketing

Sitio one-page (HTML/CSS/JS en un solo archivo: `index.html`, renombrado desde orangy-portafolio-v2.html para publicar) que muestra el trabajo de identidades visuales de Orangy. Dueña: Marcela Sandoval (March), directora de Orangy, CDMX.

## Reglas de trabajo con March (IMPORTANTES)

1. **El orden que ella indica es sagrado.** Si manda imágenes en un orden (PDF, lista), ese es el orden de los slides. Nunca curar/reordenar por cuenta propia.
2. **Ante la duda, preguntar ANTES de hacer.** No sustituir contenido por "equivalentes".
3. Es diseñadora senior — hablar de diseño de tú a tú, con criterio de brand manager AAA, pero ella decide.

## Sistema de diseño (NO modificar sin su OK)

- **Tipografía: SOLO Montserrat** (títulos en 800, cuerpo/etiquetas en 400–700). March decidió (jul 2026) descartar Deutschlander; el @font-face se eliminó. Nunca serif, nunca otra fuente.
- **Paleta oficial:** naranja `#E5501C` (solo acento), gris `#545454`, gris claro `#A6A6A6` (solo si es necesario). Fondo papel `#F4F1EB`, hairlines `#E3DED5`, footer `#3D3D3D`.
- **Barra de color segmentada** = firma visual de March; aparece en hero, manifiesto y footer, animada al aparecer. Colores y proporciones REALES muestreados del brochure: `#E5501C` 48% → `#F27405` 15.5% → `#32A6A6` 27.4% → `#99E9F2` 6.8% (segmentos desiguales, no cuartos).
- **Máximo un bloque naranja sólido** (el marquee). Elegancia = contraste de escala, no de peso; nada de "tics de IA" (números fantasma, fade-ups excesivos, eyebrows en todo).
- **Slides de casos: 4:5, imagen llenando el marco completo** (cover crop centrado en el sujeto). Nada de bandas de color/aire. Excepción: logos sobre su propio color de fondo (ej. slide 1 de Lucía Li).

## Estructura del sitio (reestructura "portafolio primero", jul 2026)

Regla de oro acordada con March: **el trabajo aparece en el segundo scroll**; el texto del brochure va en dosis de portafolio (la web y el brochure cuentan la historia completa, este doc muestra el trabajo).

Hero (Deutschlander gigante + barra, breve) → Marquee naranja → **5 casos** con carrusel (scroll-snap, flechas, arrastre, contador; cada caso con `caso-desc` de una-dos líneas) → Manifiesto de UNA línea ("Orangy existe para traducir valor real en dirección clara") → Carrusel "Más proyectos" (orden sagrado de March: Kalu, JF Group, LC Agency, Tactrick, PikiPuki, Weecom — Weecom regresó al line-up como cierre, jul 2026; imágenes en `img/otros/*.jpg`) → Cinta "Marcas que han confiado en nosotros" → Sección compacta "Primero entendemos / Luego ordenamos / Después activamos" + los 4 pilares de "Qué construimos" como lista de títulos → Footer con CTA "Platiquemos de tu proyecto" y cierre "No por velocidad. Por dirección."

### Casos (orden y contenido aprobados por March — PDFs curados, jul 2026, 5 slides c/u)

March mandó un PDF de 5 páginas por marca; el orden de páginas = orden de slides (regla sagrada). Las páginas ya venían en 4:5 (810×1012); se extrajeron a JPG q90 de 1620px sin recorte. Después mandó más imágenes con posiciones exactas (gorra Kaleia por chat; 4 mockups en PDF "portafolio__4" — los pegados en chat NO llegan como archivo, pedir PDF o Drive). Todos los casos quedaron de 6 slides. Kaleia tiene 25 años de liderazgo (corregido de 35, jul 2026).

1. **Xcaanda'** — Repostería fina · logo rojo, bolsas croissant, stickers, letrero, bolsas de regalo, collage posts
2. **Kaleia** — Intérprete floral · logo azul, fachada, gorra, tarjetas, mandil, collage posts
3. **Lucía Li** — Skincare de lujo · cliente en Machala, Ecuador (etiqueta de industria lo indica: prueba de alcance internacional) · logo azul claro, post Glow-Up, productos, bolsa, aplicación, bolsa listón azul
4. **Xipotle** — Salsas mexicanas · logo morado, botella, tote con llaveros, post recetas, post pasta, etiqueta colgante
5. **GAMA IP** — Propiedad intelectual · logo negro, tarjetas, folder en mano, piezas digitales, folder papelería, fachada

Cada caso lleva descripción (`caso-desc`) y bloque de métricas (`caso-metricas`) con etiquetas **Resultado** (logrado, cualitativo), **Proyección** (objetivo esperado, con cifras) y **Siguiente etapa** (en ejecución). Las cifras son las que dio March (jul 2026): Xcaanda' +25–30% ventas (proyección), Kaleia +15–25% retail incl. Costco y +15–20% por capacitación de piso (proyecciones), Xipotle +20% ventas MX/EUA (proyección), GAMA IP +10–12% cierre de propuestas (proyección), Lucía Li +18% en venta de productos (RESULTADO logrado, por naming de línea y universo sensorial) + agenda llena. Los números van en `.dato` (naranja, bold, 1.6em) con contador animado (`.dato-num[data-val]`, IntersectionObserver, respeta reduced-motion). OJO Kaleia: Costco NO es resultado de Orangy (ya estaban ahí antes); es contexto en la descripción. NUNCA inventar cifras: solo las que dé March.

Imágenes en `img/caso-1/slide-1..5.jpg` … `img/caso-5/slide-1..5.jpg`. Cinta "Marcas que han confiado en nosotros" (PDF MARCAS de March, orden sagrado): Aeroméxico, Netflix, New Relic, Paramount+, La Europea en `img/logos/*.png` (PNG transparentes tintados `#545454`, extraídos del PDF). Logo Orangy oficial (naranja + hoja teal, "Integrated Marketing") en `img/logo-orangy.png`, extraído del brochure, usado en el nav.

### Copy (basada en el brochure oficial, jul 2026)

Toda la copy sale del PDF "Brochure Orangy" (10 págs) que mandó March — NO inventar texto. Frases clave: "Brand Intelligence & Desarrollo de Negocios", "Arquitectura estratégica que conecta marca, comunicación y crecimiento comercial", "traducir valor real en dirección clara", "Primero entendemos. Luego ordenamos. Después activamos.", los 4 pilares de "Qué construimos" (p7), el Diagnóstico Orangy (p8) y "No por velocidad. Por dirección." (p9). Contacto (p10): hola@orangy.com.mx, 55 71 90 30 21, orangy.com.mx. Cliente ideal: negocios/líderes AAA que piensan a largo plazo (p5, p9). SEO: title/meta description/OG/JSON-LD ProfessionalService con estos datos.

Nota: el sitio orangy.com.mx no se pudo leer desde el entorno remoto (bloqueado por política de red); si hay copy del sitio que deba reflejarse, March la comparte en texto.

## Página de enlaces (linktree propio)

`links/index.html` — mini página con identidad Orangy (logo, barra, Montserrat, fondo papel) publicada en `/links/`. Botones: Ver portafolio (naranja sólido, el único), WhatsApp, sitio web, correo. En el HTML hay botones comentados para YouTube/Instagram esperando que March pase las URLs exactas (NUNCA adivinarlas).

## Pendientes

- [ ] **Publicar**: March activa GitHub Pages (Settings → Pages → Deploy from a branch) o sube la carpeta a Netlify; después conectar subdominio (posible portafolio.orangy.com.mx).
- [ ] URLs de YouTube/Instagram (u otras redes) de March para activar sus botones en `links/index.html`.

## Decisiones cerradas (jul 2026)

- Analytics: Google Analytics 4 con la cuenta Google de March, ID `G-RX21D5W3EB`, etiqueta gtag instalada en `index.html` y `links/index.html`. Dashboard privado en analytics.google.com (login de March).

- WhatsApp del CTA confirmado por March: 55 7190 3021 (wa.me/525571903021).
- Deutschlander descartada; títulos en Montserrat 800 definitivo.
- Copy y resultados de casos aprobados por March al dar la orden de publicar.

## Técnica

- Todo inline en un archivo; sin dependencias externas salvo Google Fonts (Montserrat).
- Carruseles: scroll-snap nativo + JS (arrastre pointer, teclado, contador). Nav se oculta al bajar. Reveals con IntersectionObserver, easing `cubic-bezier(.16,1,.3,1)`. `prefers-reduced-motion` respetado.
- **Lightbox**: tap/clic en slide abre la imagen full-res a pantalla completa (se detecta la imagen en pointerdown porque la pista captura el puntero; el arrastre NO abre). Esc o clic cierra. March pidió quitar el cursor de lupa (jul 2026): los slides usan el cursor grab de la pista, la función de abrir se mantiene.
- **Imágenes responsivas**: cada slide tiene versión `-sm.jpg` (800w, q82) + original 1620w vía `srcset/sizes`; el `src` queda apuntando a la full-res (la usa el lightbox).
- **Compartir**: `img/og-image.png` (1200×630, logo+barra) como og:image con URL ABSOLUTA (actualizarla si cambia el dominio), favicon naranjita (`img/favicon*.png`, generados de HTML con Montserrat).
- Cinta de logos: filtro CSS `brightness(0) invert(.47)` = gris medio uniforme; hover restaura.
- Para procesar imágenes nuevas de casos: recorte cover a 4:5 centrado en el sujeto, JPG calidad 90, ~1400px+ de ancho.
