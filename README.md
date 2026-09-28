# Rosa Montero · Centro de estética en Huelva

Web de una sola página para Rosa Montero DepiLáser (Calle Rábida, 18 · 21001 Huelva · 617 71 30 30), con un estilo editorial de revista.

Es una página estática. No necesita compilación, no usa cookies ni carga nada de terceros: las fuentes están alojadas en el propio proyecto.

## Cómo verla

```sh
python3 -m http.server 8000
# y abre http://localhost:8000
```

## Estructura

```
index.html                  Portada, la casa, tratamientos, capítulos I–V, opiniones y visítanos
css/estilos.css             Paleta, tipografía y maquetación (adaptable a móvil)
js/main.js                  Menú en móvil, sombra de la barra y el día de hoy en el horario
assets/fonts/               Bodoni Moda y Schibsted Grotesk (woff2, subconjunto latino)
assets/img/                 Estudios de luz: portada-luz, persiana, azul y og.jpg (para redes)
assets/laminas/             trazo.svg (microblading) y sombra.svg (microshading)
assets/favicon.svg          Monograma
tools/generar_imagenes.py   Genera todas las imágenes de assets/img y assets/laminas
```

Las dos láminas grandes (el corte de piel y las medidas del visagismo) están dibujadas en SVG dentro de `index.html`.

## Imágenes

Ninguna imagen es una foto del centro. Las figuras son estudios de luz y láminas dibujadas para esta web, generadas por código y reproducibles:

```sh
python3 -m pip install numpy scipy pillow
python3 tools/generar_imagenes.py
```

Para usar fotos reales, sustituye los archivos de `assets/img/` manteniendo el nombre y la proporción (cada imagen tiene una versión grande y otra reducida, en JPG y WebP). Después actualiza el texto `alt` y el pie de foto en `index.html`.

| Imagen | Proporción | Tamaños |
|---|---|---|
| `portada-luz` | 4:5 | 1600 y 900 px de ancho |
| `persiana` | 16:11 | 1600 y 900 px |
| `azul` | 1:1 | 1400 y 800 px |
| `og.jpg` | 1200 × 630 | imagen al compartir en redes |

## Datos que conviene confirmar con el centro

- **Horario.** Se ha tomado de los listados públicos: de lunes a viernes de 10:00 a 14:00 y de 16:30 a 20:00, y los sábados de 10:00 a 13:30. Coincide con el cierre a las 20:00 que muestra Google.
- **Valoración.** «4,9 con 90 reseñas» es una cifra fija. Hay que actualizarla de vez en cuando.
- **Reseñas citadas.** Son de Google y van firmadas solo con iniciales (Elena R., Natalia C., T. A. M.).
- **Láser azul.** El texto no describe usos concretos. Conviene que el centro diga para qué lo utiliza.

## Antes de publicar

- Cambia `og:image` por la URL absoluta cuando haya dominio y añade `og:url`.
- Añade el aviso legal y la política de privacidad, y enlázalos desde el pie.
