# Sistema de diseño Orangy (portafolio)

Cualquier cambio a esto requiere el OK explícito de March.

## Tipografía
- Solo **Montserrat** vía Google Fonts. Títulos 800; cuerpo y etiquetas 400–700.
- Deutschlander se descartó (jul 2026); no reintroducir `@font-face`. Nunca serif, nunca otra familia.

## Color
| Uso | Hex |
|---|---|
| Acento (solo acento) | `#E5501C` |
| Texto / gris | `#545454` |
| Gris claro (solo si es necesario) | `#A6A6A6` |
| Fondo papel | `#F4F1EB` |
| Hairlines | `#E3DED5` |
| Footer | `#3D3D3D` |

## Barra de color segmentada
Firma visual de March. Aparece en hero, manifiesto y footer, animada al aparecer. Proporciones reales muestreadas del brochure (segmentos desiguales, no cuartos):
`#E5501C` 48% → `#F27405` 15.5% → `#32A6A6` 27.4% → `#99E9F2` 6.8%.

## Principios
- Máximo **un** bloque naranja sólido (el marquee).
- Elegancia = contraste de escala, no de peso.
- Evitar "tics de IA": números fantasma de fondo, fade-ups en todo, eyebrows sobre cada título.
- Animaciones: easing `cubic-bezier(.16,1,.3,1)`, IntersectionObserver, respetar `prefers-reduced-motion`.

## Slides de casos
- Proporción **4:5**, imagen llenando el marco completo (cover, centrado en el sujeto). Sin bandas de color ni aire.
- Excepción: logos sobre su propio color de fondo (ej. slide 1 de Lucía Li) pueden ir contenidos sobre ese color.
- Archivos: `slide-N.jpg` 1620×2025 q90 + `slide-N-sm.jpg` 800×1000 q82.
- Cursor: grab de la pista (March pidió quitar la lupa). Tap/clic abre lightbox; arrastrar no.

## Estructura del sitio (orden)
Hero → Marquee naranja → 5 casos con carrusel → Manifiesto de una línea → "Más proyectos" → Cinta "Marcas que han confiado en nosotros" → "Primero entendemos / Luego ordenamos / Después activamos" + 4 pilares → Footer con CTA "Platiquemos de tu proyecto" y cierre "No por velocidad. Por dirección."

Regla de oro: el trabajo aparece en el segundo scroll; el texto del brochure va en dosis de portafolio.
