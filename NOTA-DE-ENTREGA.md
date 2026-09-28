# Nota de entrega · Borrador web Rosa Montero DepiLáser

Documento interno para revisar con el centro. **No forma parte del contenido para visitantes.**

## Qué se entrega

Una página web de una sola pantalla con desplazamiento (`index.html`), en español, preparada como propuesta inicial:

1. **Presentación.** Nombre, «Centro de estética en Huelva», servicios principales y botones «Llamar para solicitar cita» y «Consultar tratamientos».
2. **Servicios.** Depilación láser de diodo (servicio principal), microblading, microshading, visagismo y láser azul.
3. **El centro.** Presentación breve y lo que destacan los clientes en sus opiniones.
4. **Opiniones.** Valoración aportada (4,9 / 5, 90 reseñas) y los cuatro extractos facilitados.
5. **Preguntas frecuentes.** Ubicación, cita y disponibilidad, servicios, precios, horarios, adecuación de tratamientos y redes.
6. **Contacto y ubicación.** Teléfono, dirección, «Cómo llegar» (Google Maps), Instagram y Facebook.

Criterios aplicados:

- El teléfono es el único canal de consulta y cita. Todos los enlaces de llamada usan `tel:+34617713030`.
- No hay formularios, WhatsApp, correo electrónico, sistema de reservas ni confirmaciones de cita.
- No se publican horarios, precios, bonos, ofertas, consultas gratuitas ni políticas de cancelación.
- No se promete depilación definitiva, tratamientos indoloros ni un número concreto de sesiones.
- No se inventan años de experiencia, titulaciones, premios, historia ni equipo.
- Sin fotografías de stock. Las imágenes son ilustraciones propias y dos huecos rotulados («Espacio para fotografía real del centro» y «Fotografía de Rosa y del centro · Pendiente de aportar por el negocio») para mostrar dónde irían las fotos reales.
- La página lleva `noindex` y una franja «Propuesta de web · Borrador para revisión del centro» mientras sea borrador.

## Datos usados como confirmados

| Dato | Valor | Fuentes coincidentes |
|---|---|---|
| Nombre | Rosa Montero DepiLáser (en Google Maps: ROSA MONTERO) | Datos aportados, Facebook |
| Dirección | Calle Rábida, 18, 21001 Huelva, España | Ficha aportada, Facebook, Páginas Amarillas |
| Teléfono | 617 71 30 30 | Ficha aportada, Facebook, Páginas Amarillas |
| Instagram | [@rosamontero_depilaser](https://www.instagram.com/rosamontero_depilaser/) | Perfil |
| Facebook | [Rosa Montero DepiLáser](https://www.facebook.com/RosaMonterodepilaser/) | Página |
| Servicios | Depilación láser de diodo, microblading, microshading, visagismo, láser azul | Descripción de Facebook, biografía y destacado de Instagram, publicación de Facebook |

## Pendiente de confirmar con el centro

| # | Tema | Situación en el borrador | Qué necesitamos |
|---|---|---|---|
| 1 | **Horarios** | Las fuentes consultadas dan datos distintos y hay un destacado de Instagram llamado «Nuevo Horario». La web dice «Consulta nuestros horarios por teléfono». | El horario vigente, si se quiere publicar. |
| 2 | **Precios, bonos y promociones** | No se publican. Se remite al teléfono. | Decidir si se publica alguna tarifa. |
| 3 | **Depilación láser de diodo** | Explicación general y una invitación a consultar zonas, sesiones, precios y si el tratamiento es adecuado. No se nombra ningún equipo. | Zonas disponibles y qué información quiere comunicar el centro. |
| 4 | **Láser azul** | Se presenta como servicio y se remite al teléfono para conocer sus aplicaciones. Sin indicaciones médicas. | Descripción aprobada por el centro de sus aplicaciones concretas. |
| 5 | **Microblading y microshading** | Descripciones generales. Sin duración, pigmentos, protocolos ni retoques. | Información adicional, si se desea. |
| 6 | **Destacados de Instagram** «Depilacion Ceja», «LIFTING», «Tratamientos», «Productos», «Nuevo Horario» | No se han desarrollado: los títulos no indican la técnica de depilación de cejas, el tipo de lifting, el catálogo de productos ni los horarios. | Confirmar si son servicios o productos actuales y cómo describirlos. |
| 7 | **Directorio Ópphalo** | Relaciona a Rosa Montero con depilación láser LS1200, hidrodermoabrasión Ephyra, láser azul Balder y presoterapia Dorsal+, pero indica Calle Rábida, 4 y otro teléfono. **No se ha incorporado nada de esa ficha.** | Confirmar si esos equipos y servicios están vigentes. Si la ficha está desactualizada, conviene corregirla. |
| 8 | **Nombre de presentación** | El perfil de Instagram muestra «Rosa Eugenia». La web usa «Rosa». | Cómo prefiere presentarse. |
| 9 | **Valoración de Google** | Se muestra «4,9 de 5 · 90 reseñas», el dato aportado para el borrador. No es un dato en tiempo real. Se enlaza a Google Maps para ver las opiniones actuales. | Actualizar la cifra al publicar, o dejar solo el enlace. |
| 10 | **Extractos de opiniones** | Los tres primeros aparecen como «Opinión de cliente», sin autor. El cuarto está firmado por Natalia Carrion Moriña. No se presentan como verificados ni se indica la plataforma de origen. | Confirmar de dónde proceden los extractos y la conformidad para citar el nombre. |
| 11 | **Fotografías** | Hay dos huecos rotulados. | Fotos reales de Rosa y del centro, con derechos de uso y consentimiento de las personas que aparezcan. |
| 12 | **Logotipo** | Se usa un monograma «RM» provisional. | El logotipo oficial, si existe. |
| 13 | **Dominio y correo electrónico** | No se incluyen. | Dominio definitivo y, si se desea, un correo de contacto. |
| 14 | **Textos legales** | No se incluyen. | Aviso legal (LSSI), política de privacidad y política de cookies, con titular y NIF aportados por el negocio. |
| 15 | **Enlace de Google Maps** | Búsqueda por «ROSA MONTERO, Calle Rábida 18, 21001 Huelva». | El enlace directo a la ficha del centro, si se prefiere. |
| 16 | **Mapa embebido** | No se incluye, para evitar cookies de terceros. Se usa una ilustración de mapa enlazada. | Decidir si se quiere un mapa interactivo, cargado con consentimiento. |

## Antes de publicar

- [ ] Quitar la franja de borrador (`<div class="draft-bar">` en `index.html`).
- [ ] Quitar `<meta name="robots" content="noindex, nofollow">`.
- [ ] Sustituir los huecos de fotografía por imágenes reales.
- [ ] Revisar la valoración y el número de reseñas.
- [ ] Añadir el dominio definitivo (`og:url`, `url` en el JSON-LD) y una imagen para redes (`og:image`).
- [ ] Añadir los textos legales y enlazarlos desde el pie.
- [ ] Recomendado por privacidad (RGPD): alojar las fuentes (Cormorant Garamond y Manrope) en el propio servidor en lugar de cargarlas desde Google Fonts.

## Textos que conviene revisar con el centro

- **Depilación láser de diodo:** «Depilación láser de diodo en Huelva: una técnica que utiliza la luz del láser para actuar sobre el vello.»
- **Microblading:** «Técnica de micropigmentación que dibuja trazos finos, similares al pelo, para dar forma y definición a las cejas.»
- **Microshading:** «Técnica de cejas con un acabado sombreado y difuminado, de aspecto más suave que el trazo pelo a pelo.»
- **Visagismo:** «Estudio de tus rasgos para diseñar unas cejas en armonía con tu rostro.»
- **Láser azul:** «Llámanos y te contamos para qué se utiliza en el centro y si encaja con lo que buscas.»
- **El centro:** «Rosa Montero DepiLáser es un centro de estética en Huelva. Aquí te atiende Rosa, con el trato amable y cercano que mencionan quienes ya la conocen.»
- **Lo que destacan nuestros clientes en sus opiniones:** Profesionalidad · Trato cercano y amable · Higiene · Satisfacción con los tratamientos.
