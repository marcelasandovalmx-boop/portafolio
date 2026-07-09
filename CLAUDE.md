# Portafolio visual de Orangy Integrated Marketing

Sitio one-page (HTML/CSS/JS en un solo archivo: `orangy-portafolio-v2.html`) que muestra el trabajo de identidades visuales de Orangy. Dueña: Marcela Sandoval (March), directora de Orangy, CDMX.

## Reglas de trabajo con March (IMPORTANTES)

1. **El orden que ella indica es sagrado.** Si manda imágenes en un orden (PDF, lista), ese es el orden de los slides. Nunca curar/reordenar por cuenta propia.
2. **Ante la duda, preguntar ANTES de hacer.** No sustituir contenido por "equivalentes".
3. Es diseñadora senior — hablar de diseño de tú a tú, con criterio de brand manager AAA, pero ella decide.

## Sistema de diseño (NO modificar sin su OK)

- **Tipografías: SOLO Montserrat (cuerpo/etiquetas) y Deutschlander (títulos).** Deutschlander se carga por @font-face desde `fonts/Deutschlander.ttf` (archivo PENDIENTE de conseguir; mientras, fallback Montserrat 800). Nunca serif, nunca otra fuente.
- **Paleta oficial:** naranja `#E5501C` (solo acento), gris `#545454`, gris claro `#A6A6A6` (solo si es necesario). Fondo papel `#F4F1EB`, hairlines `#E3DED5`, footer `#3D3D3D`.
- **Barra de color segmentada** = firma visual de March; aparece en hero, manifiesto y footer, animada al aparecer. Colores y proporciones REALES muestreados del brochure: `#E5501C` 48% → `#F27405` 15.5% → `#32A6A6` 27.4% → `#99E9F2` 6.8% (segmentos desiguales, no cuartos).
- **Máximo un bloque naranja sólido** (el marquee). Elegancia = contraste de escala, no de peso; nada de "tics de IA" (números fantasma, fade-ups excesivos, eyebrows en todo).
- **Slides de casos: 4:5, imagen llenando el marco completo** (cover crop centrado en el sujeto). Nada de bandas de color/aire. Excepción: logos sobre su propio color de fondo (ej. slide 1 de Lucía Li).

## Estructura del sitio (reestructura "portafolio primero", jul 2026)

Regla de oro acordada con March: **el trabajo aparece en el segundo scroll**; el texto del brochure va en dosis de portafolio (la web y el brochure cuentan la historia completa, este doc muestra el trabajo).

Hero (Deutschlander gigante + barra, breve) → Marquee naranja → **5 casos** con carrusel (scroll-snap, flechas, arrastre, contador; cada caso con `caso-desc` de una-dos líneas) → Manifiesto de UNA línea ("Orangy existe para traducir valor real en dirección clara") → Carrusel "Más proyectos" (orden sagrado de March: Kalu, JF Group, LC Agency, Tactrick, PikiPuki — Weecom salió del line-up; imágenes en `img/otros/*.jpg`) → Cinta "Marcas que han confiado en nosotros" → Sección compacta "Primero entendemos / Luego ordenamos / Después activamos" + los 4 pilares de "Qué construimos" como lista de títulos → Footer con CTA "Platiquemos de tu proyecto" y cierre "No por velocidad. Por dirección."

### Casos (orden y contenido aprobados por March — PDFs curados, jul 2026, 5 slides c/u)

March mandó un PDF de 5 páginas por marca; el orden de páginas = orden de slides (regla sagrada). Las páginas ya venían en 4:5 (810×1012); se extrajeron a JPG q90 de 1620px sin recorte.

1. **Xcaanda'** — Repostería fina · logo rojo, bolsas, stickers, letrero, collage posts
2. **Kaleia** — Intérprete floral · logo azul, fachada, tarjetas, mandil, collage posts · Resultado: retail, incluida Costco
3. **Lucía Li** — Skincare de lujo · logo azul claro, post Glow-Up, productos, bolsa, aplicación
4. **Xipotle** — Salsas mexicanas · logo morado, botella, post recetas, post pasta, etiqueta colgante
5. **GAMA IP** — Propiedad intelectual · logo negro, tarjetas, piezas digitales, folder, fachada

Cada caso lleva una descripción (`caso-desc`) redactada a partir de las notas que March pasó por chat (jul 2026): qué se hizo (naming/rebranding/ADN/estrategia) y el beneficio. Ella aprueba la redacción final.

Imágenes en `img/caso-1/slide-1..5.jpg` … `img/caso-5/slide-1..5.jpg`. Cinta "Marcas que han confiado en nosotros" (PDF MARCAS de March, orden sagrado): Aeroméxico, Netflix, New Relic, Paramount+, La Europea en `img/logos/*.png` (PNG transparentes tintados `#545454`, extraídos del PDF). Logo Orangy oficial (naranja + hoja teal, "Integrated Marketing") en `img/logo-orangy.png`, extraído del brochure, usado en el nav.

### Copy (basada en el brochure oficial, jul 2026)

Toda la copy sale del PDF "Brochure Orangy" (10 págs) que mandó March — NO inventar texto. Frases clave: "Brand Intelligence & Desarrollo de Negocios", "Arquitectura estratégica que conecta marca, comunicación y crecimiento comercial", "traducir valor real en dirección clara", "Primero entendemos. Luego ordenamos. Después activamos.", los 4 pilares de "Qué construimos" (p7), el Diagnóstico Orangy (p8) y "No por velocidad. Por dirección." (p9). Contacto (p10): hola@orangy.com.mx, 55 71 90 30 21, orangy.com.mx. Cliente ideal: negocios/líderes AAA que piensan a largo plazo (p5, p9). SEO: title/meta description/OG/JSON-LD ProfessionalService con estos datos.

Nota: el sitio orangy.com.mx no se pudo leer desde el entorno remoto (bloqueado por política de red); si hay copy del sitio que deba reflejarse, March la comparte en texto.

## Pendientes

- [ ] **Fuente Deutschlander**: conseguir el .ttf y ponerlo en `fonts/Deutschlander.ttf`.
- [ ] **OK final de March a la copy** (ya está basada en el brochure oficial, pero ella da el visto bueno).
- [ ] Datos de resultado por caso (números duros para los contadores animados, si los hay).
- [ ] Al publicar: renombrar a `index.html`, deploy en Netlify/Vercel, y conectar dominio (posible subdominio de orangy.com.mx).

## Técnica

- Todo inline en un archivo; sin dependencias externas salvo Google Fonts (Montserrat).
- Carruseles: scroll-snap nativo + JS (arrastre pointer, teclado, contador). Nav se oculta al bajar. Reveals con IntersectionObserver, easing `cubic-bezier(.16,1,.3,1)`. `prefers-reduced-motion` respetado.
- Cinta de logos: filtro CSS `brightness(0) invert(.47)` = gris medio uniforme; hover restaura.
- Para procesar imágenes nuevas de casos: recorte cover a 4:5 centrado en el sujeto, JPG calidad 90, ~1400px+ de ancho.
