# Rosa Montero · Centro de estética en Huelva

Web de una sola página para el centro de estética Rosa Montero (C. Rábida, 18, 21001 Huelva · 617 71 30 30).

Es una web estática: no necesita compilación ni dependencias.

## Cómo verla

```sh
python3 -m http.server 8000
```

y abre <http://localhost:8000>. También puedes abrir `index.html` directamente en el navegador.

## Estructura

```
index.html          Página: inicio, tratamientos, el centro, opiniones, Instagram y contacto
css/estilos.css     Estilos (paleta menta, salvia y piedra; adaptable a móvil)
js/app.js           Menú móvil, cabecera al hacer scroll y animaciones de aparición
assets/negocio/     Fotografías originales del centro
assets/web/         Versiones optimizadas (WebP) y recortes de las fotografías originales
assets/favicon.svg  Icono de la pestaña
```

## Antes de publicar

- Confirmar con Rosa el permiso para usar las fotografías (las de Google Maps las subieron usuarios y los diseños de Instagram pueden incluir imágenes de terceros).
- Añadir el horario completo en la sección de contacto.
- Confirmar que el 617 71 30 30 tiene WhatsApp.
- Cuando haya dominio, poner la URL absoluta en `og:image`.
