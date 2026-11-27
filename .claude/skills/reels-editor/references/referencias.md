# Referencias que March ha mandado (y qué tomar de cada una)

## Tapioca · Homshuk Henao (@tapioca_agencia) · reels Dede_rVtNh- y DeI5xu3t6NS (nov 2026)

- 60 a 67 s, ~20 cortes (uno cada 3 s), todos a corte seco pero con **cambio de escala** entre tres encuadres (abierto, medio, cerrado) desde la misma toma. Eso hace que los saltos se sientan decididos.
- **Título tipográfico de entrada** (2 a 3.5 s): lockup de tres estilos (serif condensada en caps + script + sans bold o serif itálica), centrado sobre el pecho. Es el único texto grande del video.
- **Subtítulos diminutos**, lowercase, sans regular, blancos sin fondo, por frase, al 55 a 58 % de altura. Discretos a propósito: el video no depende de leerlos.
- Insertos ocasionales (capturas de audios) y cierre con la silla vacía.
- Grade cálido, negros levantados, saturación baja.
- Lo que March valoró: "no quiero subtítulos de edit", elegancia. Lo que no le funcionó: sentía poca transición y subtítulos genéricos (la primera traducción fue demasiado literal).

## Tati Uribe (@tatiuribem) · reel DfINcwjPPWZ (163 s, "13 años creando contenido")

- Grabado de día, luz natural, cámara trasera: la "calidad" viene de ahí. Casi sin cortes (12 en 163 s).
- **Captions que se escriben solas** con cursor `|`, en serif Didone grande + palabras clave en sans bold; una frase corta por vez al centro-bajo.
- **Insertos** constantes: memes/GIF en marco polaroid, capturas de notificaciones y mensajes, chips ("♡ mis hijos", "✓ Tecnología"), números grandes ("16 → 4 horas al día"), momentos con pantalla oscurecida y texto grande ("si yo", "wow, esto es irreal"), flashes en blanco y negro.
- Lo que March valoró: "textos que causen relevancia", música clásica, "que se note que lo hizo alguien profesional".

## Tati Uribe · reel DfAvMzNh4xi (36 s, "este video fue editado con IA")

- Muy producido: **titular arriba** (serif itálica pequeña + condensada bold en caps con palabra en amarillo/naranja) que cambia por idea cada 3 a 5 s, con pop; **una palabra a la vez** al centro en sans bold amarilla; tarjetas a pantalla completa (gris oscuro con tipografía crema/naranja); b-roll familiar; capturas de pantalla; gráficos (puntos de color, onda de audio); cierre "COMENTA «YO»" sobre crema con flecha.
- Funciona porque su encuadre tiene aire arriba de la cabeza y el titular queda a la altura de los ojos.
- Con el material actual de March (cara arriba, techo vacío) esta lógica no traduce: los titulares quedaron flotando y ella los sintió "por hacer". Reservarla para una grabación con aire o un formato distinto.

## Conclusiones para March

1. Lo que más le gusta de estas referencias es la **tipografía con intención** (editorial, serif, pocas cosas) y los **insertos con contenido real**, no la cantidad de efectos.
2. Cualquier sistema se adapta a su marca: Montserrat 800 caps, Playfair, sus scripts, placa roja, chips, teal en detalles.
3. El siguiente salto de calidad está en la grabación, no en la edición: luz natural o de ventana, cámara trasera en 4K, aire sobre la cabeza, foco y exposición bloqueados, micrófono de solapa.

## March Sandoval · testimonial de Ale, Kaleia (@march.sandoval) · reel Dc2MFA5RWzN (172 s) · referencia para testimoniales de clientes y aliados (nov 2026)

- Formato entrevista: March pregunta fuera de cámara, la persona responde a cuadro. Casi una sola toma; los cortes visibles son entradas y salidas de b-roll con material real (empaques, logos, videollamadas).
- **Contorno blanco de sticker** alrededor de la persona **solo mientras March pregunta**. Es la señal visual de "ahora escucha". Se quita cuando empieza la respuesta.
- **Captions en caja blanca redondeada**, sans bold, 2 a 4 palabras por caja, centradas al 73 % de la altura. La palabra dicha va en naranja Orangy y las que faltan en naranja claro (karaoke por palabra).
- **Placa de nombre** en los primeros segundos: caja blanca con el nombre en caps negras naranjas que entra palabra por palabra, y debajo una caja naranja más ancha, corrida a la izquierda, con el cargo en texto oscuro delgado. Dura unos 5 s.
- Sin tarjeta final: cierra con "¿dónde te podemos encontrar?" y la respuesta.
- Este formato lleva identidad **Orangy** (Montserrat, naranja `#E5501C`), no la marca personal de March.
- Aplicado a Mario Barrera, aliado estratégico (nov 2026): scratchpad `mario/work` (`edl.py` cortes, `render_segs.py` base, `caps.py` subtítulos, `comp.py` compositor).

## Referencia "caja amarilla" · reel propio de March (DfoHPUTR-Mk, nov 2026)

March la mandó con la instrucción "que quede así la edición" para el reel "El efecto gimnasio en enero". 72 s, cortes cada 2 a 4 s.

- **Texto**: un solo sistema. Captions en Montserrat Bold caps, blancos, 2 líneas máximo de unas 18 letras, centrados sobre el pecho (y ≈ 1200 a 1300). Una caja amarilla redondeada (`#F0B818`) salta de palabra en palabra detrás de la palabra que se está diciendo; el texto no cambia de color. La segunda línea aparece cuando se llega a ella.
- **Palabras clave**: de 8 a 12 por reel salen solas y grandes (ExtraBold ~100 px, caja amarilla, texto blanco) en la misma posición.
- **Insertos**: b-roll de stock a pantalla completa con los captions encima; a veces entra como recuadro con filo blanco y cursor que se expande. Requiere clips con licencia que March sube a Drive; nunca buscarlos por cuenta propia.
- **Transición**: círculo naranja con punto teal que crece y se encoge (12 cuadros en total, lleno 2 o 3 cuadros). Una por reel, en el salto de contenido más grande.
- **Planos**: punch-in alternado, sin título de apertura ni placas.
- **Cómo se hizo**: los captions no salen con ASS (no da cajas redondeadas por palabra). Se renderiza un PNG 1080×400 con alfa por cada estado con Playwright y se arma con el demuxer `concat` (`duration` por estado), luego un solo `overlay` en y=1050. Los planos se renderizan uno por uno y se concatenan: un filtergraph con más de 30 `trim` del mismo archivo se queda sin memoria.

## Referencia "titular arriba + una palabra" · reel DgGRUprB527 (120 s, nov 2026)

March la mandó con la instrucción "este es el ejemplo de la edición que quiero, solo adecua sus letras y colores" para una prueba de video de una clienta (webinar).

- **Franja superior fija**: degradado oscuro en el tercio de arriba. Ahí vive el titular por idea: renglón chico (serif itálica en la referencia) + renglón grande en caps condensadas con placa de color. Cambia cada 3 a 6 s y entra con pop.
- **Una palabra a la vez** al pecho (y ≈ 62 a 65 %), minúsculas, sans, blanca; las palabras clave cambian a un color de acento. Nunca se detiene, ni en los momentos oscuros.
- **Insertos en la franja de arriba**: tarjetas claras que se van llenando conforme ella enumera (la matriz), siempre arriba de la cabeza.
- **Momentos "dim"**: video desenfocado y oscurecido con tarjetas o capturas flotando (testimonios, esquema). De 2 a 4 por reel.
- **Cortes**: misma toma con tres encuadres (abierto, medio, cerrado), corte seco en inicio de frase.
- **Cierre**: tarjeta a pantalla completa con la llamada a la acción mientras sigue el audio.
- **Cómo se adaptó a otra marca**: mismos lugares y tiempos, pero tipografía y colores de la invitación de la clienta (sans redonda bold con palabra en dorado, velo ciruela arriba y abajo, píldora de fecha, chips crema numerados, fotos circulares con aro dorado). Scratchpad `sembremos/work`: `overlay.html` con una función `render(t)` que dibuja todo el estado en el tiempo t, `render.js` saca un PNG con alfa por cuadro (4 páginas en paralelo, unos 1,600 cuadros) y ffmpeg lo superpone a `base.mp4` (punch-ins con `scale eval=frame`, desenfoque de los "dim" con dos ramas `gblur` + `fade alpha`).
- **Trampa**: cuando el encuadre no tiene aire arriba, ancla el zoom arriba (`crop y = (ih-1920)*0.12`) para que el punch-in baje la cabeza en vez de meterla en el titular.

## Tati Uribe · reel DgOPrGbKX5d (77 s, "3 hábitos para tu primer millón") · referencia "titular + tarjetas animadas" (nov 2026)

March la mandó para editar un video propio "con mis colores".

- **Dos estados que se alternan cada 6 a 9 s**: ella a cuadro, y tarjeta a pantalla completa (el mismo video desenfocado y oscurecido, el audio sigue).
- **A cuadro**: píldora blanca chica con la frase resumida y puntos suspensivos donde va la palabra clave, y debajo la palabra clave gigante en caps (se escribe letra por letra). Subtítulos chicos al pecho que crecen palabra por palabra. Unos 12 titulares en 77 s.
- **Tarjetas** (8 en 77 s): arriba la frase en chico, que también crece palabra por palabra; al centro un gráfico de línea muy simple que se anima con lo que dice (gráfica que sube, notas adhesivas que aparecen una por una, barras, anillo que se llena, reloj, corazón que se dibuja); abajo un rótulo en caps a dos tonos.
- **Paleta de un solo tono** (crema sobre café oscuro). Nada de emojis ni fotos de archivo.
- **Tarjeta de nombre** cerca del final (nombre + a qué se dedica) y cierre con "sígueme".
- **Cómo se adaptó a March** (scratchpad `video-nov27/`): píldora en placa roja `#c92520`, palabra clave crema `#EFEDEA` en Montserrat 800, tarjetas con crema y un solo acento rojo por tarjeta, teal solo en detalles. Como su material no tiene aire arriba (cara en la mitad superior), el titular va al pecho (y 1066 a 1300) y el subtítulo debajo (y 1368), todo dentro de zonas seguras. `overlay.html` con `render(t)` + `render.js` (PNG con alfa por cuadro) y el desenfoque con `maskedmerge` y una máscara `geq` de 16×16 que sigue los tiempos de las tarjetas.
