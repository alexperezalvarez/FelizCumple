from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

W, H = 1600, 1100
BG = (248, 243, 232)
INK = (35, 30, 25)
GRAY = (120, 115, 108)
BLUE = (22, 50, 105)
RED = (145, 30, 30)
GREEN = (30, 85, 50)
BROWN = (100, 62, 35)
GOLD = (190, 150, 20)
PINK = (195, 75, 115)
ORANGE = (195, 105, 25)
SOFT_PINK = (255, 230, 235)

random.seed(42)

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_PATH_BOLD = "C:/Windows/Fonts/arialbd.ttf"
f_normal = f_small = f_tiny = f_title = f_sub = f_bold = None
if os.path.exists(FONT_PATH):
    f_normal = ImageFont.truetype(FONT_PATH, 11)
    f_small = ImageFont.truetype(FONT_PATH, 9)
    f_tiny = ImageFont.truetype(FONT_PATH, 7.5)
    f_title = ImageFont.truetype(FONT_PATH, 17)
    f_sub = ImageFont.truetype(FONT_PATH, 13)
if os.path.exists(FONT_PATH_BOLD):
    f_bold = ImageFont.truetype(FONT_PATH_BOLD, 11)

def jit(pts, amp=1.0):
    return [(x + random.uniform(-amp, amp), y + random.uniform(-amp, amp)) for x, y in pts]

def sketch_line(draw, pts, fill=INK, width=1, rough=0.8, passes=1):
    if len(pts) < 2: return
    for _ in range(passes):
        p = jit(pts, rough)
        draw.line(p, fill=fill, width=width)

def sketch_rect(draw, xy, fill=None, outline=INK, width=1, rough=0.8):
    x1, y1, x2, y2 = xy
    t = jit([(x1, y1), (x2, y1)], rough)
    r = jit([(x2, y1), (x2, y2)], rough)
    b = jit([(x2, y2), (x1, y2)], rough)
    l = jit([(x1, y2), (x1, y1)], rough)
    if fill:
        draw.polygon(t + r + b + l, fill=fill)
    sketch_line(draw, t, outline, width, rough)
    sketch_line(draw, r, outline, width, rough)
    sketch_line(draw, b, outline, width, rough)
    sketch_line(draw, l, outline, width, rough)

def sketch_rrect(draw, xy, fill=None, outline=INK, width=1, rough=0.8, r=6):
    x1, y1, x2, y2 = xy
    pts = [(x1+r, y1), (x2-r, y1), (x2, y1+r), (x2, y2-r), (x2-r, y2), (x1+r, y2), (x1, y2-r), (x1, y1+r)]
    if fill:
        draw.polygon(jit(pts, rough), fill=fill)
    sketch_line(draw, [(x1+r, y1), (x2-r, y1)], outline, width, rough)
    sketch_line(draw, [(x2, y1+r), (x2, y2-r)], outline, width, rough)
    sketch_line(draw, [(x2-r, y2), (x1+r, y2)], outline, width, rough)
    sketch_line(draw, [(x1, y2-r), (x1, y1+r)], outline, width, rough)

def arrow(draw, start, end, fill=INK, width=1, rough=0.8):
    sx, sy = start; ex, ey = end
    a = math.atan2(ey - sy, ex - sx)
    hl = 7
    sketch_line(draw, jit([(sx, sy), (ex, ey)], rough), fill, width, rough)
    sketch_line(draw, jit([(ex, ey), (ex - hl * math.cos(a - 0.45), ey - hl * math.sin(a - 0.45))], rough), fill, width, rough)
    sketch_line(draw, jit([(ex, ey), (ex - hl * math.cos(a + 0.45), ey - hl * math.sin(a + 0.45))], rough), fill, width, rough)

def lbl(draw, xy, txt, fill=INK, font=None, align="center"):
    x, y = xy
    f = font or f_normal
    b = draw.textbbox((0, 0), txt, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    if align == "center": px = x - tw / 2
    elif align == "left": px = x
    else: px = x - tw
    dr = random.uniform(-0.3, 0.3)
    draw.text((px, y - th / 2 + dr), txt, fill=fill, font=f)

def crosshatch(draw, xy, color=(200, 195, 185), spacing=6):
    x1, y1, x2, y2 = xy
    for i in range(int(x1), int(x2), spacing):
        offset = random.uniform(-0.5, 0.5)
        draw.line([(i + offset, y1), (i + spacing * 0.3 + offset, y2)], fill=color, width=1)

def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Paper edge - multiple lines
    for i in range(3):
        o = i * 2 + 1
        draw.rectangle([o, o, W - o - 1, H - o - 1], outline=(215 + i * 2, 210 + i * 2, 200 + i * 2), width=1)

    # Decorative corner folds
    for cx, cy in [(5, 5), (W - 5, 5), (5, H - 5), (W - 5, H - 5)]:
        sketch_line(draw, [(cx - 5, cy + 15), (cx - 5, cy - 5), (cx + 15, cy - 5)], GRAY, 1, 0.5)

    # Title area
    lbl(draw, (W // 2, 18), "BOCETO DEL PROYECTO — FELIZ CUMPLEANOS", INK, f_title)
    sketch_line(draw, [(350, 36), (1250, 36)], INK, 1, 0.5, 2)
    lbl(draw, (W // 2, 48), "Vista previa de la pagina (izquierda)  ·  Arquitectura y componentes (derecha)", GRAY, f_sub)

    # ===================================================================
    # LEFT PANEL: VISUAL MOCKUP (hand-drawn scene)
    # ===================================================================
    lx, ly = 25, 65
    lw, lh = 740, 990
    sketch_rrect(draw, (lx, ly, lx + lw, ly + lh), fill=(255, 250, 242), outline=GRAY, width=1, r=10)

    lbl(draw, (lx + lw // 2, ly + 10), "VISTA PREVIA — COMO SE VE LA PAGINA", GRAY, f_small)
    sketch_line(draw, [(lx + 20, ly + 22), (lx + lw - 20, ly + 22)], GRAY, 1, 0.3)

    # Background area (pink scene)
    scene_x = lx + 18
    scene_y = ly + 30
    scene_w = lw - 36
    scene_h = 560
    draw.rectangle([scene_x, scene_y, scene_x + scene_w, scene_y + scene_h], fill=(255, 240, 243, 120))
    sketch_rect(draw, (scene_x, scene_y, scene_x + scene_w, scene_y + scene_h), outline=None)

    # Confetti dots in background
    for _ in range(45):
        cx = scene_x + random.randint(5, scene_w - 5)
        cy = scene_y + random.randint(5, scene_h - 5)
        r = random.randint(2, 4)
        col = random.choice([(255, 180, 180), (255, 200, 200), (255, 210, 180), (220, 200, 255), (200, 230, 255)])
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    # ---- TABLE ----
    tab_x = scene_x + 40
    tab_y = scene_y + scene_h - 80
    tab_w = scene_w - 80
    tab_h = 30
    sketch_rect(draw, (tab_x, tab_y, tab_x + tab_w, tab_y + tab_h), fill=(200, 185, 170), outline=BROWN, width=1)
    # Wood grain
    for g in range(3):
        gy = tab_y + 6 + g * 8
        sketch_line(draw, [(tab_x + 10, gy), (tab_x + tab_w - 10, gy)], (180, 165, 150), 1, 0.5)
    # Table legs
    sketch_line(draw, [(tab_x + 30, tab_y + tab_h), (tab_x + 15, tab_y + tab_h + 50)], BROWN, 2, 0.8, 2)
    sketch_line(draw, [(tab_x + tab_w - 30, tab_y + tab_h), (tab_x + tab_w - 15, tab_y + tab_h + 50)], BROWN, 2, 0.8, 2)
    # Crossbar
    sketch_line(draw, [(tab_x + 15, tab_y + tab_h + 30), (tab_x + tab_w - 15, tab_y + tab_h + 30)], BROWN, 1, 0.5)
    lbl(draw, (tab_x + tab_w // 2, tab_y + tab_h // 2 - 1), "Mesa de madera (CSS)", BROWN, f_small)

    # ---- PICTURE FRAME ----
    fr_x = scene_x + (scene_w - 220) // 2
    fr_y = scene_y + 20
    fr_w, fr_h = 220, 165
    # Frame outer (wood with grain)
    sketch_rect(draw, (fr_x - 10, fr_y - 10, fr_x + fr_w + 10, fr_y + fr_h + 10), fill=(170, 120, 70), outline=(130, 85, 45), width=2)
    sketch_rect(draw, (fr_x - 7, fr_y - 7, fr_x + fr_w + 7, fr_y + fr_h + 7), fill=(160, 110, 60), outline=None)
    # Inner frame edge
    sketch_rect(draw, (fr_x, fr_y, fr_x + fr_w, fr_y + fr_h), fill=(190, 200, 210), outline=INK, width=1)
    # "Screen" content
    draw.rectangle([fr_x + 5, fr_y + 5, fr_x + fr_w - 5, fr_y + fr_h - 5], fill=(180, 195, 210))
    # Video scene sketch inside frame - mountains/water
    sketch_line(draw, [(fr_x + 20, fr_y + fr_h - 30), (fr_x + 60, fr_y + fr_h - 60), (fr_x + 100, fr_y + fr_h - 40), (fr_x + 140, fr_y + fr_h - 55), (fr_x + 200, fr_y + fr_h - 30)], (100, 130, 160), 1, 0.8, 2)
    sketch_line(draw, [(fr_x + 15, fr_y + fr_h - 15), (fr_x + 205, fr_y + fr_h - 15)], (150, 165, 180), 1, 0.5)
    # "Play" triangle
    cx = fr_x + fr_w // 2 + 15
    cy = fr_y + fr_h // 2
    draw.polygon(jit([(cx - 5, cy - 8), (cx - 5, cy + 8), (cx + 8, cy)], 0.5), fill=(100, 120, 140))
    lbl(draw, (fr_x + fr_w // 2, fr_y + fr_h // 2 + 16), "Mar.mp4", (120, 130, 140), f_small)

    # Frame label
    sketch_line(draw, [(fr_x + fr_w // 2 - 25, fr_y - 18), (fr_x + fr_w // 2 + 25, fr_y - 18)], INK, 1, 0.3)
    lbl(draw, (fr_x + fr_w // 2, fr_y - 22), "Portarretrato", BROWN, f_small)

    # ---- HAPPY BIRTHDAY TEXT ----
    hb_x = scene_x + scene_w // 2
    hb_y = fr_y + fr_h + 20
    lbl(draw, (hb_x, hb_y), "Happy Birthday!", PINK, f_title)
    lbl(draw, (hb_x, hb_y + 20), "~ animacion flotar + brillo ~", GRAY, f_small)

    # Decorative line around text
    sketch_line(draw, [(hb_x - 100, hb_y + 32), (hb_x + 100, hb_y + 32)], (PINK[0], PINK[1], PINK[2], 100), 1, 0.3)

    # ---- CAKE ----
    c_x = scene_x + (scene_w // 2) - 80
    c_y = hb_y + 55
    c_w, c_h = 110, 85

    # Cake layers (3 tiers)
    for i in range(3):
        off = i * 6
        layer_h = 22
        ly2 = c_y + i * layer_h
        fill_c = [(235, 200, 180), (225, 190, 170), (215, 180, 160)][i]
        sketch_rect(draw, (c_x - off + i * 5, ly2, c_x + c_w + off - i * 5, ly2 + layer_h), fill=fill_c, outline=BROWN, width=1)
        # Frosting drip
        if i == 0:
            for d in range(4):
                dx = c_x + 15 + d * 22 + random.randint(-3, 3)
                dy = ly2 + layer_h
                sketch_line(draw, [(dx, dy), (dx + random.randint(-2, 2), dy + 4)], (200, 170, 155), 1, 0.3)

    # Chocolate frosting top
    frosting_y = c_y - 6
    sketch_rect(draw, (c_x - 8, frosting_y, c_x + c_w + 8, frosting_y + 10), fill=(90, 55, 35), outline=BROWN, width=1)

    # Candle
    v_x = c_x + c_w // 2 - 3
    v_y = c_y - 35
    sketch_rect(draw, (v_x, v_y, v_x + 6, c_y - 6), fill=(255, 252, 240), outline=INK, width=1)
    # Candle stripe
    sketch_line(draw, [(v_x + 1, v_y + 10), (v_x + 5, v_y + 10)], (200, 180, 220), 1, 0.2)
    sketch_line(draw, [(v_x + 1, v_y + 20), (v_x + 5, v_y + 20)], (200, 180, 220), 1, 0.2)
    # Flame
    f_top = (v_x + 3, v_y - 2)
    f_l = (v_x - 5, v_y + 8)
    f_r = (v_x + 11, v_y + 8)
    draw.polygon(jit([f_top, f_l, f_r], 1.5), fill=(255, 200, 60))
    draw.polygon(jit([(v_x + 3, v_y + 1), (v_x, v_y + 7), (v_x + 6, v_y + 7)], 0.8), fill=(255, 255, 220))
    # Glow around flame
    draw.ellipse(jit([(v_x - 8, v_y - 6), (v_x + 14, v_y + 14)], 1), fill=(255, 220, 100, 30))

    # Cake label
    lbl(draw, (c_x + c_w // 2, c_y + c_h + 6), "Torta + vela + llama parpadeante", BROWN, f_small)

    # ---- GIFT BOX ----
    g_x = c_x + c_w + 55
    g_y = c_y + 8
    g_s = 60
    # Box body
    sketch_rect(draw, (g_x, g_y, g_x + g_s, g_y + g_s), fill=(255, 205, 205), outline=RED, width=2)
    # Ribbon vertical
    sketch_line(draw, [(g_x + g_s // 2, g_y), (g_x + g_s // 2, g_y + g_s)], RED, 2, 0.5, 2)
    # Ribbon horizontal
    sketch_line(draw, [(g_x, g_y + g_s // 2), (g_x + g_s, g_y + g_s // 2)], RED, 2, 0.5, 2)
    # Bow
    draw.polygon(jit([(g_x + g_s // 2, g_y - 2), (g_x + g_s // 2 - 10, g_y - 14), (g_x + g_s // 2 + 10, g_y - 14), (g_x + g_s // 2, g_y - 2)], 0.5), fill=(220, 50, 50))
    draw.polygon(jit([(g_x + g_s // 2, g_y - 2), (g_x + g_s // 2 - 6, g_y - 10), (g_x + g_s // 2 + 6, g_y - 10), (g_x + g_s // 2, g_y - 2)], 0.5), fill=(240, 80, 80))
    # Lid
    sketch_rect(draw, (g_x - 4, g_y - 7, g_x + g_s + 4, g_y), fill=(255, 215, 215), outline=RED, width=1)
    # Stars
    for s in range(5):
        sx_ = g_x + 8 + s * 12
        sy_ = g_y + 10 + (s * 17) % 45
        draw.polygon(jit([
            (sx_, sy_ - 5), (sx_ + 2, sy_ - 1), (sx_ + 5, sy_),
            (sx_ + 2, sy_ + 1), (sx_, sy_ + 5), (sx_ - 2, sy_ + 1),
            (sx_ - 5, sy_), (sx_ - 2, sy_ - 1)
        ], 0.5), fill=GOLD)

    lbl(draw, (g_x + g_s // 2, g_y + g_s + 6), "Regalo (rebote + estrellas)", BROWN, f_small)

    # ---- MODAL LETTER SKETCH (small) ----
    mod_x = g_x + 70
    mod_y = g_y - 5
    mod_w, mod_h = 100, 70
    # Speech bubble / letter indicator
    sketch_rrect(draw, (mod_x, mod_y, mod_x + mod_w, mod_y + mod_h), fill=(255, 245, 245), outline=RED, width=1, r=4)
    sketch_line(draw, [(mod_x + 15, mod_y + mod_h), (mod_x + 10, mod_y + mod_h + 8), (mod_x + 25, mod_y + mod_h)], RED, 1, 0.3)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 12), "Carta de amor", PINK, f_small)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 28), "Mensaje para Mar", GRAY, f_small)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 42), "~ de Alex ~", PINK, f_small)
    sketch_line(draw, [(mod_x + 10, mod_y + mod_h - 8), (mod_x + mod_w - 10, mod_y + mod_h - 8)], (PINK[0], PINK[1], PINK[2], 80), 1, 0.3)

    # Dashed line pointing from gift box to letter
    arrow(draw, (g_x + g_s, g_y + 20), (mod_x, mod_y + 30), RED, 1, 0.5)

    # ---- OVERLAY INDICATOR ----
    ov_x = scene_x + scene_w + 10
    ov_y = scene_y + 50
    lbl(draw, (ov_x - 80, ov_y), "Overlay oscuro", GRAY, f_small)
    lbl(draw, (ov_x - 80, ov_y + 12), "(fade out al soplar)", GRAY, f_small)
    sketch_rect(draw, (scene_x + scene_w - 60, scene_y + 10, scene_x + scene_w - 10, scene_y + 60), fill=(20, 20, 20, 180), outline=INK, width=1)
    # Arrow from overlay to scene
    arrow(draw, (scene_x + scene_w - 35, scene_y + 60), (scene_x + scene_w - 35, scene_y + scene_h - 50), INK, 1, 0.5)

    # ---- SCENE LABELS (right side of scene) ----
    label_data = [
        (scene_x + scene_w + 8, scene_y + 100, "Confeti fondo (z:0)", BLUE),
        (scene_x + scene_w + 8, scene_y + 120, "Confeti frente (z:2)", BLUE),
    ]
    for lx_, ly_, lt, lc in label_data:
        draw.ellipse(jit([(lx_ + 2, ly_), (lx_ + 6, ly_ + 4)], 0.3), fill=lc)
        lbl(draw, (lx_ + 12, ly_ + 2), lt, lc, f_small, align="left")

    # ===================================================================
    # SCENE LEGEND (below scene)
    # ===================================================================
    leg_x = lx + 18
    leg_y = scene_y + scene_h + 15
    sketch_rrect(draw, (leg_x, leg_y, leg_x + scene_w, leg_y + 275), fill=(252, 249, 242), outline=GRAY, width=1, r=5)

    lbl(draw, (leg_x + scene_w // 2, leg_y + 12), "ELEMENTOS DE LA ESCENA", GRAY, f_small)
    sketch_line(draw, [(leg_x + scene_w // 2 - 70, leg_y + 22), (leg_x + scene_w // 2 + 70, leg_y + 22)], GRAY, 1, 0.3)

    elems = [
        ("1", "Fondo rosa pastel", "con confeti animado en 2 capas (parallax)"),
        ("2", "Marco de madera", "con video de Mar.mp4 en loop infinito"),
        ("3", "Torta de 3 pisos", "con frosting de chocolate y vela con llama parpadeante"),
        ("4", "Caja de regalo", "que rebota con 5 estrellas giratorias alrededor"),
        ("5", "Texto 'Happy Birthday'", "flotando con animacion de brillo"),
        ("6", "Mesa / soporte", "dibujada con CSS, textura de madera"),
        ("7", "Overlay oscuro", "se desvanece al soplar la vela (fade out)"),
        ("8", "Modal carta de amor", "aparece al clickear el regalo, mensaje personalizado"),
    ]
    for i, (num, titl, desc) in enumerate(elems):
        col = i % 2
        row_y = leg_y + 32 + i * 28
        # Number circle
        draw.ellipse(jit([(leg_x + 12, row_y), (leg_x + 22, row_y + 10)], 0.3), fill=INK)
        lbl(draw, (leg_x + 17, row_y + 5), num, (255, 255, 255), f_tiny)
        # Title
        lbl(draw, (leg_x + 30, row_y + 1), titl, INK, f_bold or f_normal, align="left")
        # Description
        lbl(draw, (leg_x + 30, row_y + 14), desc, GRAY, f_small, align="left")
        if i < len(elems) - 1:
            sketch_line(draw, [(leg_x + 12, row_y + 24), (leg_x + scene_w - 12, row_y + 24)], (230, 225, 218), 1, 0.2)

    # ===================================================================
    # RIGHT PANEL: ARCHITECTURE
    # ===================================================================
    rx0 = lx + lw + 18
    ry0 = ly
    rw = W - rx0 - 25
    rh = lh
    sketch_rrect(draw, (rx0, ry0, rx0 + rw, ry0 + rh), fill=(255, 250, 242), outline=GRAY, width=1, r=10)

    lbl(draw, (rx0 + rw // 2, ry0 + 10), "ARQUITECTURA DEL PROYECTO", GRAY, f_small)
    sketch_line(draw, [(rx0 + 15, ry0 + 22), (rx0 + rw - 15, ry0 + 22)], GRAY, 1, 0.3)

    # ---- Box drawing helper ----
    def arch_box(x, y, w, h, title, items, color=BLUE, title_bg=None):
        sketch_rrect(draw, (x, y, x + w, y + h), fill=(255, 255, 255, 200), outline=INK, width=1, r=5)
        if title_bg:
            draw.rectangle([x + 1, y + 1, x + w - 1, y + 22], fill=title_bg)
        lbl(draw, (x + w // 2, y + 13), title, color, f_sub)
        sketch_line(draw, [(x + 8, y + 24), (x + w - 8, y + 24)], GRAY, 1, 0.2)
        for i, item in enumerate(items):
            lbl(draw, (x + 10, y + 30 + i * 14), item, INK, f_normal, align="left")

    # ---- HTML BOX ----
    arch_box(rx0 + 12, ry0 + 28, rw - 24, 175, "index.html", [
        "Meta tags, viewport, favicon",
        "Google Fonts (Pacifico)",
        "Canvas x2 para confeti (z-index 0 y 2)",
        "Video Mar.mp4 dentro del portarretrato",
        "Torta + vela + llama con animacion CSS",
        "Caja de regalo con estrellas giratorias",
        "Mensaje 'Happy Birthday' flotante",
        "Modal con carta de amor personalizada",
        "Audio: soplar1.mp3 (soplido), cancion.mp3",
        "Overlay oscuro + footer 'Hecho con amor'",
    ], BLUE, (235, 245, 255))

    # ---- CSS BOX ----
    arch_box(rx0 + 12, ry0 + 212, rw - 24, 140, "CSS — Estilos y animaciones", [
        "styles.css  (660 lineas)",
        "  Layout de escena con flexbox",
        "  @keyframes: flama (0.15s), apagar,",
        "    flotar, brillo, aparecer, latir",
        "    cinta, base, techo, sombra, estrella",
        "  clip-path, radial-gradient, box-shadow",
        "mobile.css  (36 lineas)",
        "  Escala responsive con calc(100vw/650)",
        "  Deshabilitar tap highlight en touch",
    ], GREEN, (235, 250, 235))

    # ---- JS BOX ----
    arch_box(rx0 + 12, ry0 + 360, rw - 24, 170, "JavaScript — Logica e interaccion", [
        "Confeti.js  (z-index: 0, detras de todo)",
        "  Canvas 2D, 100 particulas circulares",
        "  Caida infinita con requestAnimationFrame",
        "  Fondo rosa pastel (rgba 255,182,193,1)",
        "",
        "Confeti2.js  (z-index: 2, frente a todo)",
        "  Misma logica con clearRect (transparente)",
        "  Efecto parallax de 2 capas",
        "",
        "Sorpresa.js  (interactividad)",
        "  Click en llama -> apagar vela + sonido",
        "  Click en regalo -> abrir modal carta",
        "  Overlay fade out al soplar la vela",
    ], (100, 50, 130), (245, 235, 255))

    # ---- ASSETS BOX ----
    arch_box(rx0 + 12, ry0 + 540, rw - 24, 90, "Assets (recursos/)", [
        "Mar.mp4 — Video en loop dentro del marco",
        "cancion.mp3 — Cancion de cumpleanos",
        "soplar1.mp3 — Efecto de soplido",
        "soplar2.mp3 — (sin usar en el codigo actual)",
        "cumpleanos.png — Icono favicon de la pagina",
    ], RED, (255, 240, 240))

    # ---- INTERACTION FLOW ----
    arch_box(rx0 + 12, ry0 + 640, rw - 24, 145, "Flujo de interaccion del usuario", [
        "1. Pagina carga → overlay oscuro visible + confeti empieza (1.5s)",
        "2. Usuario clickea la LLAMA de la vela:",
        "     a) Suena soplar1.mp3 (efecto de soplido)",
        "     b) Animacion 'apagar' escala la llama a 0",
        "     c) 1 segundo despues: overlay fade out",
        "     d) Suena cancion.mp3 (cumpleanos)",
        "3. Usuario clickea la CAJA DE REGALO:",
        "     a) Modal carta aparece con animacion 'aparecer'",
        "     b) Muestra mensaje romantico para Mar, firmado por Alex",
        "     c) Click en el fondo del modal lo cierra",
        "4. Confeti continua cayendo infinitamente en 2 capas",
    ], ORANGE, (255, 248, 235))

    # ---- DEPLOY / DEPS / GIT ----
    arch_box(rx0 + 12, ry0 + 795, (rw - 24) // 2 - 6, 70, "Deploy", [
        "Statico — sin build tools ni dependencias",
        "Netlify / Netlify Drop — solo arrastrar carpeta",
    ], GREEN, (240, 250, 240))

    arch_box(rx0 + (rw - 24) // 2 + 18, ry0 + 795, (rw - 24) // 2 - 6, 70, "Dependencias", [
        "CERO dependencias externas",
        "Solo HTML + CSS + JavaScript vanilla",
        "Google Fonts (Pacifico) via CDN",
    ], (100, 50, 150), (245, 240, 255))

    arch_box(rx0 + 12, ry0 + 875, rw - 24, 55, "Git / Version control", [
        "github.com/alexperezalvarez/FelizCumple.git",
        "6 commits | Autor: Alex | Rama: main",
    ], BLUE, (235, 242, 255))

    # ---- ARROWS linking sections ----
    arrow(draw, (rx0 + rw // 2, ry0 + 203), (rx0 + rw // 2, ry0 + 212), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 352), (rx0 + rw // 2, ry0 + 360), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 530), (rx0 + rw // 2, ry0 + 540), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 630), (rx0 + rw // 2, ry0 + 640), INK, 1, 0.5)

    # ---- Divider line between panels ----
    sketch_line(draw, [(lx + lw + 5, ly + 20), (lx + lw + 5, ly + lh - 15)], GRAY, 1, 0.3, 2)

    # ---- Bottom footer ----
    lbl(draw, (W // 2, H - 12), "Boceto generado digitalmente con estilo dibujado a mano · Arial 11 · Julio 2026", GRAY, f_small)

    # ---- Save ----
    out_png = "D:/Feliz Cumpleaños/boceto_proyecto.png"
    img.save(out_png, "PNG")
    print(f"PNG: {out_png}")

    out_pdf = "D:/Feliz Cumpleaños/boceto_proyecto.pdf"
    img.save(out_pdf, "PDF", resolution=150)
    print(f"PDF: {out_pdf}")

if __name__ == "__main__":
    main()
