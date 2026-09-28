"""Genera las imágenes de la web: estudios de luz (JPG + WebP) y las láminas
de ceja (SVG).

Uso:
    python3 -m pip install numpy scipy pillow
    python3 tools/generar_imagenes.py

Todo es determinista (semilla fija): volver a ejecutarlo produce las mismas
imágenes. Las fotos reales del centro, cuando las haya, pueden sustituir a
estos archivos manteniendo los mismos nombres.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "assets" / "img"
LAMINAS = RAIZ / "assets" / "laminas"
SEMILLA = 1821  # Calle Rábida, 18 · 21001


# --------------------------------------------------------------------------
# Utilidades de revelado
# --------------------------------------------------------------------------

def ruido_suave(rng, h, w, sigma):
    """Ruido de baja frecuencia normalizado a [-1, 1]."""
    n = gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), sigma)
    return n / (np.abs(n).max() + 1e-6)


def revelar(hdr, exposicion=1.0):
    """Curva de película: satura suavemente las altas luces hacia el blanco."""
    return 1.0 - np.exp(-np.clip(hdr, 0, None) * exposicion)


def vineta(h, w, fuerza=0.4, centro=(0.5, 0.5)):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = (x / w - centro[0]) * 1.2
    dy = (y / h - centro[1]) * 1.2 * h / w
    r2 = dx * dx + dy * dy
    return (1.0 - fuerza * np.clip(r2 * 1.6, 0, 1) ** 1.1)[..., None]


def grano(rng, img, cantidad=0.03, tamano=0.7):
    """Grano de película: más visible en los medios tonos que en las luces."""
    h, w, _ = img.shape
    g = gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), tamano)
    g /= g.std() + 1e-6
    lum = img.mean(axis=2, keepdims=True)
    peso = 0.45 + 1.1 * lum * (1.0 - lum) * 2.0
    color = 1.0 + 0.25 * gaussian_filter(rng.standard_normal((h, w, 3)).astype(np.float32), (tamano, tamano, 0))
    return img + g[..., None] * cantidad * peso * color * 0.5 + g[..., None] * cantidad * peso * 0.5


def aberracion(img, px=1.2):
    """Aberración cromática radial muy leve (rojo hacia fuera, azul hacia dentro)."""
    h, w, _ = img.shape
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cy, cx = h / 2, w / 2
    fuera = img.copy()
    for canal, escala in ((0, px), (2, -px)):
        k = escala / max(h, w)
        yy = cy + (y - cy) * (1 - k)
        xx = cx + (x - cx) * (1 - k)
        fuera[..., canal] = map_coordinates(img[..., canal], [yy, xx], order=1, mode="nearest")
    return fuera


def guardar(img, nombre, anchos, calidad_jpg=80, calidad_webp=74):
    img8 = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")
    for ancho in anchos:
        alto = round(img8.height * ancho / img8.width)
        im = img8 if ancho == img8.width else img8.resize((ancho, alto), Image.LANCZOS)
        sufijo = "" if ancho == anchos[0] else f"-{ancho}"
        im.save(IMG / f"{nombre}{sufijo}.jpg", quality=calidad_jpg, optimize=True, progressive=True)
        im.save(IMG / f"{nombre}{sufijo}.webp", quality=calidad_webp, method=6)
    return img8


# --------------------------------------------------------------------------
# Fig. 1 · Línea de luz sobre lino (portada)
# --------------------------------------------------------------------------

def portada_luz(rng, w=1600, h=2000):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)

    # Pliegues de una sábana de lino: crestas casi verticales, deformadas.
    alabeo = ruido_suave(rng, h, w, 140) * 90
    alt = np.zeros((h, w), np.float32)
    for amp, periodo, angulo, fase in ((1.0, 420, 0.18, 0.3), (0.55, 230, -0.10, 1.7),
                                       (0.30, 130, 0.32, 4.1), (0.12, 70, -0.25, 2.2)):
        u = x * np.cos(angulo) + y * np.sin(angulo) + alabeo
        alt += amp * np.sin(2 * np.pi * u / periodo + fase)
    alt += ruido_suave(rng, h, w, 60) * 0.35
    alt /= np.abs(alt).max()

    gy, gx = np.gradient(gaussian_filter(alt, 3) * 60)
    normal = np.stack([-gx, -gy, np.ones_like(gx)], axis=-1)
    normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    luz_sala = np.array([0.45, -0.55, 0.70], np.float32)
    luz_sala /= np.linalg.norm(luz_sala)
    sombreado = np.clip(normal @ luz_sala, 0, 1) ** 1.4

    # La línea proyectada se dobla con los pliegues, como sobre tela real.
    y0 = 0.60 * h
    fila = int(y0)
    desplaz = gaussian_filter(alt[fila], 14) * 34
    y_linea = y0 - desplaz
    pendiente = np.gradient(y_linea)
    dist = (y - y_linea[None, :]) / np.sqrt(1 + pendiente[None, :] ** 2)
    cara = np.clip(normal[fila, :, 2] * 0.6 + 0.4 + gaussian_filter(-np.gradient(desplaz), 4)[None, :] * 0.6, 0.25, 1.3)
    nucleo = np.exp(-(dist ** 2) / (2 * 1.3 ** 2)) * cara
    # Se desvanece hacia los bordes del encuadre.
    borde = np.clip(np.minimum(x, w - x) / 180, 0, 1) ** 0.8
    nucleo *= borde

    halo = (gaussian_filter(nucleo, 5) * 5.0 + gaussian_filter(nucleo, 16) * 11.0
            + gaussian_filter(nucleo, 55) * 26.0 + gaussian_filter(nucleo, 170) * 50.0)

    # Luz ambiente de la sala y rebote rosado de la línea sobre la tela.
    caida = np.exp(-(((y - y0) / 620) ** 2)) * 0.8 + 0.2 * (y / h)
    rebote = np.exp(-np.abs(dist) / 150) * (0.35 + 0.65 * sombreado)

    tierra = np.array([0.62, 0.40, 0.32], np.float32)
    rosa = np.array([1.00, 0.28, 0.30], np.float32)
    blanco = np.array([1.00, 0.86, 0.82], np.float32)

    hdr = (tierra * (0.035 + 0.16 * caida * sombreado)[..., None]
           + rosa * (rebote * 0.42)[..., None]
           + rosa * (halo * 0.55)[..., None]
           + blanco * (nucleo * 7.0)[..., None])
    hdr += (gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), 1.2) * 0.012)[..., None] * tierra

    img = revelar(hdr, 1.25) ** (1 / 1.08)
    img = aberracion(img, 2.0)
    img *= vineta(h, w, 0.55, (0.5, 0.58))
    img = gaussian_filter(img, (0.45, 0.45, 0))
    img = grano(rng, img, 0.042, 0.75)
    return np.clip(img, 0, 1)


# --------------------------------------------------------------------------
# Fig. 2 · Persiana: sol de la tarde en la pared
# --------------------------------------------------------------------------

def persiana(rng, w=1600, h=1100):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)

    # Coordenada a través de las lamas (inclinadas) y a lo largo de la ventana.
    a = np.deg2rad(-17)
    u = y * np.cos(a) + x * np.sin(a)
    b = np.deg2rad(24)
    v = x * np.cos(b) - y * np.sin(b)

    periodo = 58
    fase = (u / periodo) % 1.0
    lamas = (fase > 0.40).astype(np.float32)
    # Ventana: dos hojas con un montante en medio.
    v0, v1, montante, ancho_m = 70, 1420, 760, 30
    ventana = ((v > v0) & (v < v1) & (np.abs(v - montante) > ancho_m / 2)).astype(np.float32)
    # Arriba y abajo se corta el hueco de la ventana.
    ventana *= ((u > 90) & (u < 1150)).astype(np.float32)
    mascara = lamas * ventana

    # Penumbra creciente con la distancia a la ventana (arriba a la izquierda).
    distancia = np.clip((x / w) * 0.65 + (y / h) * 0.55, 0, 1)
    sigmas = (1.5, 4.0, 8.0, 14.0)
    capas = [gaussian_filter(mascara, s) for s in sigmas]
    t = distancia * (len(sigmas) - 1)
    idx = np.clip(t.astype(int), 0, len(sigmas) - 2)
    frac = t - idx
    sol = np.zeros_like(mascara)
    for i in range(len(sigmas) - 1):
        sel = idx == i
        sol[sel] = capas[i][sel] * (1 - frac[sel]) + capas[i + 1][sel] * frac[sel]

    # Sombra difusa de una rama de olivo, lejos de la pared.
    rama = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(rama)
    p0, p1, p2 = np.array([1640, 1180.0]), np.array([1260, 860.0]), np.array([1120, 520.0])
    pts = []
    for t_ in np.linspace(0, 1, 60):
        pts.append(tuple((1 - t_) ** 2 * p0 + 2 * (1 - t_) * t_ * p1 + t_ ** 2 * p2))
    d.line(pts, fill=255, width=12)
    for i, t_ in enumerate(np.linspace(0.08, 0.98, 17)):
        base = (1 - t_) ** 2 * p0 + 2 * (1 - t_) * t_ * p1 + t_ ** 2 * p2
        tang = 2 * (1 - t_) * (p1 - p0) + 2 * t_ * (p2 - p1)
        tang /= np.linalg.norm(tang)
        lado = 1 if i % 2 else -1
        ang = np.arctan2(tang[1], tang[0]) + lado * (0.55 + rng.uniform(-0.15, 0.2))
        largo = rng.uniform(120, 170) * (1.05 - 0.3 * t_)
        ancho = largo * rng.uniform(0.14, 0.2)
        direc = np.array([np.cos(ang), np.sin(ang)])
        perp = np.array([-direc[1], direc[0]])
        hoja = []
        for s in np.linspace(0, 1, 24):
            hoja.append(tuple(base + direc * largo * s + perp * ancho * np.sin(np.pi * s) ** 0.8))
        for s in np.linspace(1, 0, 24):
            hoja.append(tuple(base + direc * largo * s - perp * ancho * np.sin(np.pi * s) ** 0.8))
        d.polygon(hoja, fill=255)
    rama = gaussian_filter(np.asarray(rama, np.float32) / 255, 6)

    luz = sol * (1 - 0.88 * rama)
    luz *= 0.82 + 0.18 * (1 - distancia)

    textura = 1 + ruido_suave(rng, h, w, 1.1) * 0.018 + ruido_suave(rng, h, w, 7) * 0.022 + ruido_suave(rng, h, w, 90) * 0.03
    sombra_col = np.array([0.80, 0.75, 0.69], np.float32)
    sol_col = np.array([1.04, 0.90, 0.70], np.float32)
    img = sombra_col + (sol_col - sombra_col) * luz[..., None]
    img *= textura[..., None]
    img *= 0.94 + 0.08 * (1 - (y / h))[..., None]
    img *= vineta(h, w, 0.28, (0.42, 0.45))
    img = gaussian_filter(img, (0.5, 0.5, 0))
    img = grano(rng, img, 0.02, 0.9)
    return np.clip(img, 0, 1)


# --------------------------------------------------------------------------
# Fig. 5 · Haz de luz azul atravesando bruma
# --------------------------------------------------------------------------

def azul(rng, w=1400, h=1400):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)

    # Bruma: ruido turbulento de varias escalas, algo estirado en horizontal.
    bruma = np.zeros((h, w), np.float32)
    for sigma, peso in ((120, 0.5), (45, 0.3), (14, 0.2)):
        n = gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), (sigma * 0.7, sigma * 1.4))
        bruma += peso * n / (np.abs(n).max() + 1e-6)
    bruma = np.clip(0.4 + 2.0 * bruma, 0.03, 1.8)

    # Haz desde fuera de cuadro (arriba a la izquierda) hasta un punto de impacto.
    ax, ay = -60.0, 0.16 * h
    bx, by = 0.70 * w, 0.66 * h
    dx, dy = bx - ax, by - ay
    largo = np.hypot(dx, dy)
    ux, uy = dx / largo, dy / largo
    s_ = np.clip(((x - ax) * ux + (y - ay) * uy) / largo, 0, 1)
    px, py = ax + s_ * dx, ay + s_ * dy
    d = np.hypot(x - px, y - py)
    antes = (((x - ax) * ux + (y - ay) * uy) <= largo).astype(np.float32)

    nucleo = np.exp(-(d ** 2) / (2 * 1.6 ** 2)) * bruma * (0.55 + 0.45 * s_) * antes
    difuso = np.exp(-(d ** 2) / (2 * 22 ** 2)) * bruma * antes
    humo = np.exp(-d / 260) * bruma * antes

    # Punto de impacto sobre una superficie y su reflejo.
    r2 = (x - bx) ** 2 + (y - by) ** 2
    impacto = np.exp(-r2 / (2 * 5 ** 2))
    charco = np.exp(-(((x - bx) / 260) ** 2 + ((y - by - 18) / 34) ** 2))

    azul_laser = np.array([0.16, 0.36, 1.00], np.float32)
    cian = np.array([0.70, 0.86, 1.00], np.float32)
    fondo = np.array([0.010, 0.014, 0.034], np.float32)

    hdr = fondo * (0.7 + 0.6 * (y / h))[..., None]
    hdr += azul_laser * (humo * 0.10 + difuso * 0.32 + charco * 0.16)[..., None]
    hdr += azul_laser * (gaussian_filter(nucleo + impacto * 3, 8) * 6 + gaussian_filter(nucleo + impacto * 3, 40) * 18)[..., None]
    hdr += cian * (nucleo * 3.2 + impacto * 9.0)[..., None]
    hdr += azul_laser * (gaussian_filter(impacto, 90) * 560)[..., None]

    img = revelar(hdr, 1.2) ** (1 / 1.05)
    img = aberracion(img, 2.5)
    img *= vineta(h, w, 0.5, (0.6, 0.55))
    img = gaussian_filter(img, (0.5, 0.5, 0))
    img = grano(rng, img, 0.04, 0.8)
    return np.clip(img, 0, 1)


# --------------------------------------------------------------------------
# Láminas de ceja (SVG)
# --------------------------------------------------------------------------

def contorno_ceja(n=80):
    """Borde superior e inferior de una ceja en un lienzo de 600 × 220."""
    t = np.linspace(0, 1, n)
    x = 40 + t * 520
    # Arco con el punto alto hacia el 62 % y la cola descendente.
    arriba = 138 - 58 * np.sin(np.pi * np.clip(t / 1.24, 0, 1)) ** 1.05 - 6 * t
    arriba += np.clip(t - 0.62, 0, None) ** 1.5 * 120
    grosor = 64 * (1 - t) ** 0.8 + 3
    # Inicio romo y redondeado.
    grosor[:8] *= np.linspace(0.62, 1, 8) ** 0.5
    arriba[:8] += np.linspace(14, 0, 8) ** 1.2 * 0.6
    abajo = arriba + grosor
    return x, arriba, abajo


def _punto_ceja(x, arriba, abajo, t):
    i = t * (len(x) - 1)
    i0 = int(i)
    f = i - i0
    i1 = min(i0 + 1, len(x) - 1)
    cx = x[i0] * (1 - f) + x[i1] * f
    ya = arriba[i0] * (1 - f) + arriba[i1] * f
    yb = abajo[i0] * (1 - f) + abajo[i1] * f
    return cx, ya, yb


def svg_trazo(rng):
    """Microblading: pelos finos en espiga (los de abajo suben, los de arriba bajan)."""
    x, arriba, abajo = contorno_ceja()
    trazos = []
    for _ in range(230):
        t = rng.uniform(0.0, 0.96)
        cx, ya, yb = _punto_ceja(x, arriba, abajo, t)
        alto = yb - ya
        cola = np.clip((t - 0.55) / 0.45, 0, 1)
        de_abajo = rng.uniform() < 0.62
        # Los de abajo nacen en el borde inferior y suben; los de arriba caen desde el borde superior.
        if de_abajo:
            s = rng.uniform(0.0, 0.45)
            ang = -30 + 18 * cola
        else:
            s = rng.uniform(0.55, 1.0)
            ang = 9 - 4 * cola
        if t < 0.13:
            s = rng.uniform(0.0, 0.5)
            ang = -78 + 40 * (t / 0.13)
        py = yb - alto * s
        cx2, ya2, _ = _punto_ceja(x, arriba, abajo, min(t + 0.01, 1))
        ang += np.degrees(np.arctan2(ya2 - ya, cx2 - cx + 1e-6))
        ang = np.deg2rad(ang + rng.normal(0, 3.5))
        largo = np.clip(alto * rng.uniform(0.7, 1.05), 8, 34)
        ex, ey = cx + np.cos(ang) * largo, py + np.sin(ang) * largo
        curva = rng.uniform(1.0, 3.0) * (1 if de_abajo else -1)
        mx = (cx + ex) / 2 + np.sin(ang) * curva
        my = (py + ey) / 2 - np.cos(ang) * curva
        ancho = rng.uniform(0.6, 1.1)
        op = rng.uniform(0.5, 0.92)
        trazos.append(f'<path d="M{cx:.1f} {py:.1f}Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}" '
                      f'stroke-width="{ancho:.2f}" stroke-opacity="{op:.2f}"/>')
    cuerpo = "\n    ".join(trazos)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 55 560 160" role="img" aria-label="Ceja dibujada trazo a trazo">
  <g fill="none" stroke="#1A1614" stroke-linecap="round">
    {cuerpo}
  </g>
</svg>
"""


def svg_sombra(rng):
    """Microshading: punteado en degradado, agrupado por tamaño de punto."""
    x, arriba, abajo = contorno_ceja()
    grupos = {0.9: [], 1.4: [], 1.9: []}
    total = 0
    while total < 3000:
        t = rng.uniform(0, 1)
        cx, ya, yb = _punto_ceja(x, arriba, abajo, t)
        s = rng.uniform(0, 1)
        # Degradado: suave en el inicio, más denso en el arco y el borde inferior.
        densidad = np.clip(0.18 + 0.9 * t ** 0.7, 0, 1) * (0.55 + 0.45 * s)
        if rng.uniform() > densidad:
            continue
        py = ya + (yb - ya) * s
        d = rng.uniform(0.9, 2.1) * (0.8 + 0.4 * t)
        grosor = min(grupos, key=lambda k: abs(k - d))
        grupos[grosor].append(f"M{cx:.1f} {py:.1f}h0")
        total += 1
    capas = "".join(f'<path stroke-width="{k}" d="{"".join(v)}"/>' for k, v in grupos.items())
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 55 560 160" role="img" aria-label="Ceja sombreada punto a punto">
  <g fill="none" stroke="#1A1614" stroke-opacity=".82" stroke-linecap="round">{capas}</g>
</svg>
"""


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    LAMINAS.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEMILLA)
    portada = portada_luz(rng)
    im = guardar(portada, "portada-luz", (1600, 900))
    # Imagen para compartir en redes: recorte horizontal alrededor de la línea.
    alto = round(im.width * 630 / 1200)
    centro = int(0.60 * im.height)
    og = im.crop((0, centro - alto // 2, im.width, centro + alto // 2)).resize((1200, 630), Image.LANCZOS)
    og.save(IMG / "og.jpg", quality=84, optimize=True, progressive=True)

    guardar(persiana(np.random.default_rng(SEMILLA + 1)), "persiana", (1600, 900))
    guardar(azul(np.random.default_rng(SEMILLA + 2)), "azul", (1400, 800))

    (LAMINAS / "trazo.svg").write_text(svg_trazo(np.random.default_rng(SEMILLA + 3)), encoding="utf-8")
    (LAMINAS / "sombra.svg").write_text(svg_sombra(np.random.default_rng(SEMILLA + 4)), encoding="utf-8")

    for p in sorted(list(IMG.iterdir()) + list(LAMINAS.iterdir())):
        print(f"{p.relative_to(RAIZ)}  {p.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
