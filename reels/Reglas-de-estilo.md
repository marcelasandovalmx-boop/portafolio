# Reglas de estilo · Reels Orangy

Guía de March (Marcela Sandoval), directora de Orangy Integrated Marketing. Toda edición de reels la sigue al pie de la letra. Si una instrucción choca con esta guía, se pregunta a March cuál manda.

Del kit de Viegas Estudio solo se toma el **método** (5 pasadas, zona segura, revisión final, notas). Su estilo (Bebas Neue, Rajdhani, JetBrains Mono, violeta, oro, tarjetas de cristal, brillos, synthwave) **no se usa**.

## Marca y tono
- Orangy: Brand Intelligence & Desarrollo de Negocios. Público: negocios y líderes AAA que piensan a largo plazo.
- Tono editorial pausado: premium, cercano y claro. "No por velocidad. Por dirección."
- Elegancia = contraste de escala, no de peso ni de efectos.
- Copy y cifras: solo lo que dice March en el video o lo que ella aprueba. Nunca inventar datos.

## Lienzo y zona segura
- 1080×1920, 30 fps, H.264, audio AAC 48 kHz.
- Zona segura de Instagram: nada importante en los **220 px de arriba**, los **380 px de abajo** ni los **140 px de la derecha**. Margen izquierdo de 64 px.
- Área útil para texto y gráficos: x 64–940, y 220–1540 (876×1320 px).

## Tipografía
- **Solo Montserrat.** Nunca serif, nunca otra familia.
- Palabra clave: Montserrat 800, 150 px (130–170 según el largo), tracking −0.02em, minúsculas como se dice (mayúscula inicial solo si inicia frase).
- Subtítulo de apoyo: Montserrat 600, 64 px, tracking −0.01em, interlineado 1.1.
- Títulos a pantalla completa: Montserrat 800, 120–160 px, tracking −0.02em, máximo 3 líneas.
- Etiquetas (solo cuando hacen falta, nunca encima de cada título): Montserrat 600, 30 px, mayúsculas, tracking .14em.
- Máximo 2 pesos en pantalla a la vez.

## Color
| Uso | HEX |
|---|---|
| Acento: palabra clave y barra (solo acento) | `#E5501C` |
| Texto principal | `#545454` |
| Gris claro (solo si es necesario: etiquetas secundarias) | `#A6A6A6` |
| Fondo papel | `#F4F1EB` |
| Hairlines / bordes | `#E3DED5` |
| Gris oscuro (sombra de legibilidad, fondo de cierre si March lo pide) | `#3D3D3D` |

- Nunca fondos naranja sólido. El naranja vive en la palabra clave y en la barra.
- Una sola palabra naranja en pantalla a la vez.
- Fuera de esta tabla no entra ningún color de interfaz (la barra usa además `#F27405`, `#32A6A6`, `#99E9F2`, solo dentro de ella).

## Fondo
- **Fondo real** la mayor parte del reel.
- **Papel `#F4F1EB`** (March recortada encima) solo en momentos clave: el gancho (0–2 s), los títulos y enseñanzas clave a pantalla completa y el cierre.
- Sobre papel, el texto va en `#545454`. Sobre el fondo real, el texto va en `#F4F1EB` con sombra suave `0 4px 24px rgba(61,61,61,.45)`. Sin contorno ni brillo.

## Barra segmentada (firma de March)
- Proporciones reales: `#E5501C` 48% → `#F27405` 15.5% → `#32A6A6` 27.4% → `#99E9F2` 6.8%. Segmentos desiguales, esquinas rectas.
- Medidas en reel: 600×10 px (ancho completo del bloque de texto si este mide menos).
- Aparece **solo en el gancho y en el cierre**. Se dibuja de izquierda a derecha: cada segmento 1.0 s, desfasado 0.12 s, easing `cubic-bezier(.16,1,.3,1)`.

## Subtítulos
- De 1 a 3 palabras a la vez; cada palabra aparece cuando March la dice (tiempos de `words.json`).
- Una palabra clave por frase, en Montserrat 800 naranja `#E5501C`; el resto, Montserrat 600 64 px.
- Cada subtítulo, **mínimo 0.4 s** en pantalla.
- Nunca encima de la cara: a la altura del pecho, línea base entre y 1250 y y 1500, alineado a la izquierda en x 64 (o centrado si el encuadre lo pide).
- Ancho máximo 812 px. Sin emojis, sin cajas de fondo.
- Entrada: aparece con opacidad 0→1 y 12 px de subida en 0.2 s. Salida seca.

## Motion graphics
- Una idea por escena. Contenido real (capturas, piezas del portafolio, logos oficiales) antes que ilustraciones.
- Entrada de 0.2 a 0.35 s con easing `cubic-bezier(.16,1,.3,1)`, desplazamiento máximo 24 px; se mantiene; sale limpia en 0.2 s.
- Tarjetas (si hacen falta): fondo `#F4F1EB`, borde 2 px `#E3DED5`, esquinas rectas, sin sombra, sin cristal, sin brillo.
- Texto detrás de March solo en el gancho y en palabras grandes, usando el mate del recorte.
- Zoom: punch-in de **4% como máximo**; corte seco para enfatizar, lento (≥1.5 s) para tensión. Cada zoom necesita una razón.

## Ritmo y cortes
- Cortar pausas de más de 0.4 s; dejar 0.1 s de respiración a cada lado del corte.
- Tomas repetidas: se queda la última toma buena.
- Un cambio visual cada 3–4 s (subtítulo clave, gráfico, zoom o cambio de fondo).

## Sonido
- Voz siempre encima: limpia (paso alto 80 Hz, de-esser suave).
- Música: lo-fi suave (SynthFlow, género Lo-Fi), 18 dB debajo de la voz, con ducking de 7 dB mientras March habla (ataque 40 ms, relajación 450 ms). Entrada 0.6 s, fundido final 1.5 s.
- Efectos mínimos: solo un whoosh suave en cada cambio de escena y un toque al cierre, 20–25 dB debajo de la voz. Sin golpes, sin braaam, sin glitch, sin riser.
- Máster: **−14 LUFS integrados**, pico real por debajo de **−1 dBTP**.

## Marcas y logos
- Logo Orangy oficial (`img/logo-orangy.png`), nunca recreado. Solo en el **cierre**: 1.5–2 s sobre papel, 560 px de ancho, centrado, con la barra debajo y `orangy.com.mx` en Montserrat 600 40 px `#545454`.
- Logos de clientes: los oficiales del portafolio, nunca recreados; cifras solo las aprobadas por March.

## Portada
- Una palabra (o dos cortas) en Montserrat 800, ≥ 220 px, legible en miniatura; fondo papel o fotograma real con March, dentro de la zona segura.

## Prohibido
- Cualquier fuente que no sea Montserrat; serif.
- Colores fuera de la paleta Orangy (incluye violeta, oro, lavanda del kit de Viegas).
- Fondos naranja sólido; más de una palabra naranja a la vez.
- Contorno blanco alrededor de March, brillos, glow, tarjetas de cristal.
- Gráficos o subtítulos encima de la cara.
- Datos o cifras sin fuente o no aprobados por March.
- Emojis en subtítulos.
- "Tics de IA": números fantasma de fondo, animaciones de entrada en todo, etiquetas encima de cada título.

## Revisión final (antes de publicar, informe ✓/✗)
1. Ningún texto ni gráfico importante en los 220 px de arriba, 380 px de abajo o 140 px de la derecha.
2. Ningún subtítulo dura menos de 0.4 s.
3. Nada tapa la cara en ningún fotograma.
4. Todo cumple esta guía: solo Montserrat, paleta Orangy, barra solo en gancho y cierre, movimiento.
5. Volumen: −14 LUFS integrados y pico real < −1 dBTP (medidos).
6. La portada tiene una palabra grande, legible en miniatura.
