from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

W, H = 2000, 1400
BG = (252, 249, 242)
INK = (30, 28, 25)
GRAY = (130, 125, 118)
LIGHT_GRAY = (200, 195, 188)
BLUE = (22, 50, 105)
RED = (155, 30, 30)
GREEN = (30, 90, 50)
BROWN = (110, 68, 38)
GOLD = (195, 155, 25)
PINK = (200, 70, 110)
ORANGE = (200, 110, 25)
SOFT_PINK = (255, 225, 230)
PURPLE = (90, 45, 130)
TEAL = (25, 120, 110)

random.seed(42)

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_PATH_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_PATH_ITALIC = "C:/Windows/Fonts/ariali.ttf"

f_normal = f_small = f_tiny = f_title = f_sub = f_bold = f_header = f_big = None
if os.path.exists(FONT_PATH):
    f_normal = ImageFont.truetype(FONT_PATH, 12)
    f_small = ImageFont.truetype(FONT_PATH, 10)
    f_tiny = ImageFont.truetype(FONT_PATH, 8)
    f_title = ImageFont.truetype(FONT_PATH, 20)
    f_sub = ImageFont.truetype(FONT_PATH, 14)
    f_header = ImageFont.truetype(FONT_PATH, 16)
    f_big = ImageFont.truetype(FONT_PATH, 24)
if os.path.exists(FONT_PATH_BOLD):
    f_bold = ImageFont.truetype(FONT_PATH_BOLD, 12)
    f_bold_title = ImageFont.truetype(FONT_PATH_BOLD, 16)
if os.path.exists(FONT_PATH_ITALIC):
    f_italic = ImageFont.truetype(FONT_PATH_ITALIC, 11)


def jit(pts, amp=1.0):
    return [(x + random.uniform(-amp, amp), y + random.uniform(-amp, amp)) for x, y in pts]


def sketch_line(draw, pts, fill=INK, width=1, rough=0.8, passes=1):
    if len(pts) < 2:
        return
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
    if outline:
        sketch_line(draw, t, outline, width, rough)
        sketch_line(draw, r, outline, width, rough)
        sketch_line(draw, b, outline, width, rough)
        sketch_line(draw, l, outline, width, rough)


def sketch_rrect(draw, xy, fill=None, outline=INK, width=1, rough=0.8, r=6):
    x1, y1, x2, y2 = xy
    pts = [
        (x1 + r, y1), (x2 - r, y1),
        (x2, y1 + r), (x2, y2 - r),
        (x2 - r, y2), (x1 + r, y2),
        (x1, y2 - r), (x1, y1 + r),
    ]
    if fill:
        draw.polygon(jit(pts, rough), fill=fill)
    if outline:
        sketch_line(draw, [(x1 + r, y1), (x2 - r, y1)], outline, width, rough)
        sketch_line(draw, [(x2, y1 + r), (x2, y2 - r)], outline, width, rough)
        sketch_line(draw, [(x2 - r, y2), (x1 + r, y2)], outline, width, rough)
        sketch_line(draw, [(x1, y2 - r), (x1, y1 + r)], outline, width, rough)


def arrow(draw, start, end, fill=INK, width=1, rough=0.8, head_size=8):
    sx, sy = start
    ex, ey = end
    a = math.atan2(ey - sy, ex - sx)
    hl = head_size
    sketch_line(draw, jit([(sx, sy), (ex, ey)], rough), fill, width, rough)
    sketch_line(draw, jit([(ex, ey), (ex - hl * math.cos(a - 0.45), ey - hl * math.sin(a - 0.45))], rough), fill, width, rough)
    sketch_line(draw, jit([(ex, ey), (ex - hl * math.cos(a + 0.45), ey - hl * math.sin(a + 0.45))], rough), fill, width, rough)


def dashed_line(draw, start, end, fill=INK, width=1, dash_len=8, gap_len=5, rough=0.5):
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    pos = 0
    while pos < length:
        seg_end = min(pos + dash_len, length)
        p1 = (sx + ux * pos + random.uniform(-rough, rough), sy + uy * pos + random.uniform(-rough, rough))
        p2 = (sx + ux * seg_end + random.uniform(-rough, rough), sy + uy * seg_end + random.uniform(-rough, rough))
        draw.line([p1, p2], fill=fill, width=width)
        pos += dash_len + gap_len


def lbl(draw, xy, txt, fill=INK, font=None, align="center"):
    x, y = xy
    f = font or f_normal
    b = draw.textbbox((0, 0), txt, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    if align == "center":
        px = x - tw / 2
    elif align == "left":
        px = x
    else:
        px = x - tw
    dr = random.uniform(-0.3, 0.3)
    draw.text((px, y - th / 2 + dr), txt, fill=fill, font=f)


def crosshatch(draw, xy, color=(200, 195, 185), spacing=6, angle=45):
    x1, y1, x2, y2 = xy
    for i in range(int(x1), int(x2) + spacing, spacing):
        offset = random.uniform(-0.5, 0.5)
        draw.line(
            [(i + offset, y1), (i + spacing * 0.3 + offset, y2)],
            fill=color, width=1
        )


def draw_circle(draw, cx, cy, r, fill=None, outline=None, width=1):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def draw_star(draw, cx, cy, r_outer, r_inner=0.4, fill=GOLD, points=5):
    pts = []
    for i in range(points * 2):
        angle = math.pi / 2 + i * math.pi / points
        r = r_outer if i % 2 == 0 else r_outer * r_inner
        pts.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    draw.polygon(jit(pts, 0.5), fill=fill)


def draw_heart(draw, cx, cy, size, fill=(200, 70, 110)):
    pts = []
    for t_deg in range(0, 360):
        t = math.radians(t_deg)
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * size / 16, cy + y * size / 16))
    draw.polygon(pts, fill=fill)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # --- Paper border ---
    for i in range(4):
        o = i * 2 + 1
        c = 210 + i * 5
        draw.rectangle([o, o, W - o - 1, H - o - 1], outline=(c, c - 3, c - 8), width=1)

    # Corner decorations
    for cx, cy in [(8, 8), (W - 8, 8), (8, H - 8), (W - 8, H - 8)]:
        sketch_line(draw, [(cx - 6, cy + 20), (cx - 6, cy - 6), (cx + 20, cy - 6)], GRAY, 1, 0.5)

    # Small dots at corners
    for cx, cy in [(12, 12), (W - 12, 12), (12, H - 12), (W - 12, H - 12)]:
        draw_circle(draw, cx, cy, 2, fill=GRAY)

    # --- TITLE ---
    lbl(draw, (W // 2, 25), "BOCETO DEL PROYECTO  —  FELIZ CUMPLEA\u00d1OS", INK, f_big)
    sketch_line(draw, [(350, 48), (W - 350, 48)], INK, 1, 0.5, 2)
    lbl(draw, (W // 2, 62), "Vista previa visual (izq.)  ·  Arquitectura t\u00e9cnica (centro)  ·  Flujo de datos (der.)", GRAY, f_sub)

    # Decorative small hearts near title
    draw_heart(draw, 330, 25, 4, PINK)
    draw_heart(draw, W - 330, 25, 4, PINK)

    # ===================================================================
    # LEFT PANEL: VISUAL MOCKUP
    # ===================================================================
    lx, ly = 25, 80
    lw, lh = 680, 1260
    sketch_rrect(draw, (lx, ly, lx + lw, ly + lh), fill=(255, 252, 246), outline=GRAY, width=1, r=10)

    lbl(draw, (lx + lw // 2, ly + 14), "VISTA PREVIA \u2014 C\u00d3MO SE VE LA P\u00c1GINA", GRAY, f_bold_title)
    sketch_line(draw, [(lx + 20, ly + 28), (lx + lw - 20, ly + 28)], GRAY, 1, 0.3)

    # Browser chrome mockup
    chrome_x = lx + 15
    chrome_y = ly + 35
    chrome_w = lw - 30
    sketch_rrect(draw, (chrome_x, chrome_y, chrome_x + chrome_w, chrome_y + 30), fill=(240, 238, 232), outline=GRAY, width=1, r=4)
    # Address bar
    sketch_rrect(draw, (chrome_x + 60, chrome_y + 6, chrome_x + chrome_w - 10, chrome_y + 24), fill=(255, 255, 255), outline=LIGHT_GRAY, width=1, r=3)
    lbl(draw, (chrome_x + 60, chrome_y + 15), "felizcumplea\u00f1os.alex.com", GRAY, f_tiny, align="left")
    # Browser dots
    for i in range(3):
        col = [(255, 95, 86), (255, 189, 46), (39, 201, 63)][i]
        draw_circle(draw, chrome_x + 18 + i * 14, chrome_y + 15, 4, fill=col)

    # --- Pink scene background ---
    scene_x = chrome_x
    scene_y = chrome_y + 32
    scene_w = chrome_w
    scene_h = 600
    draw.rectangle([scene_x, scene_y, scene_x + scene_w, scene_y + scene_h], fill=(255, 182, 193))
    sketch_rect(draw, (scene_x, scene_y, scene_x + scene_w, scene_y + scene_h), outline=None)

    # Confetti in background
    for _ in range(60):
        cx = scene_x + random.randint(8, scene_w - 8)
        cy = scene_y + random.randint(8, scene_h - 8)
        r = random.randint(2, 5)
        col = random.choice([
            (255, 160, 160), (255, 200, 170), (200, 170, 255),
            (170, 220, 255), (255, 255, 170), (170, 255, 200)
        ])
        if random.random() > 0.5:
            draw_circle(draw, cx, cy, r, fill=col)
        else:
            rect_pts = jit([(cx - r, cy - r // 2), (cx + r, cy - r // 2),
                            (cx + r, cy + r // 2), (cx - r, cy + r // 2)], 0.5)
            draw.polygon(rect_pts, fill=col)

    # --- Picture Frame ---
    fr_x = scene_x + (scene_w - 240) // 2
    fr_y = scene_y + 25
    fr_w, fr_h = 240, 185

    # Frame shadow
    sketch_rect(draw, (fr_x - 8, fr_y - 8, fr_x + fr_w + 12, fr_y + fr_h + 12), fill=(180, 170, 160), outline=None)
    # Frame outer
    sketch_rect(draw, (fr_x - 12, fr_y - 12, fr_x + fr_w + 12, fr_y + fr_h + 12), fill=(170, 120, 70), outline=(130, 85, 45), width=2)
    sketch_rect(draw, (fr_x - 9, fr_y - 9, fr_x + fr_w + 9, fr_y + fr_h + 9), fill=(160, 110, 60), outline=None)
    # Wood grain on frame
    for g in range(5):
        gy = fr_y - 10 + g * 75
        sketch_line(draw, [(fr_x - 11, gy), (fr_x + fr_w + 11, gy)], (145, 100, 55), 1, 0.5)
    for g in range(4):
        gx = fr_x - 8 + g * 80
        sketch_line(draw, [(gx, fr_y - 10), (gx, fr_y + fr_h + 10)], (145, 100, 55), 1, 0.5)
    # Inner frame
    sketch_rect(draw, (fr_x, fr_y, fr_x + fr_w, fr_y + fr_h), fill=(195, 205, 215), outline=INK, width=1)
    # Video content
    draw.rectangle([fr_x + 4, fr_y + 4, fr_x + fr_w - 4, fr_y + fr_h - 4], fill=(175, 190, 210))
    # Mountain scene sketch
    sketch_line(draw, [
        (fr_x + 15, fr_y + fr_h - 35),
        (fr_x + 55, fr_y + fr_h - 75),
        (fr_x + 90, fr_y + fr_h - 50),
        (fr_x + 130, fr_y + fr_h - 85),
        (fr_x + 175, fr_y + fr_h - 55),
        (fr_x + 215, fr_y + fr_h - 35)
    ], (100, 130, 160), 1, 0.8, 2)
    # Water
    for wy in range(3):
        sketch_line(draw, [
            (fr_x + 15, fr_y + fr_h - 20 + wy * 8),
            (fr_x + fr_w - 15, fr_y + fr_h - 20 + wy * 8)
        ], (150, 165, 180), 1, 0.5)
    # Play button
    cx_play = fr_x + fr_w // 2 + 15
    cy_play = fr_y + fr_h // 2
    draw.polygon(jit([(cx_play - 8, cy_play - 12), (cx_play - 8, cy_play + 12), (cx_play + 12, cy_play)], 0.5), fill=(80, 100, 130))
    lbl(draw, (fr_x + fr_w // 2, fr_y + fr_h // 2 + 20), "Mar.mp4", (120, 130, 140), f_small)

    # Frame label
    lbl(draw, (fr_x + fr_w // 2, fr_y - 22), "Portarretrato con video", BROWN, f_small)
    sketch_line(draw, [(fr_x + fr_w // 2 - 35, fr_y - 15), (fr_x + fr_w // 2 + 35, fr_y - 15)], BROWN, 1, 0.3)

    # --- Happy Birthday Text ---
    hb_x = scene_x + scene_w // 2
    hb_y = fr_y + fr_h + 25
    lbl(draw, (hb_x, hb_y), "Happy Birthday!", PINK, f_big)
    lbl(draw, (hb_x, hb_y + 24), "~ animaci\u00f3n flotar + brillo infinito ~", GRAY, f_small)

    # Decorative line
    sketch_line(draw, [(hb_x - 120, hb_y + 38), (hb_x + 120, hb_y + 38)], PINK, 1, 0.3)

    # Small hearts around text
    draw_heart(draw, hb_x - 130, hb_y + 2, 3, PINK)
    draw_heart(draw, hb_x + 130, hb_y + 2, 3, PINK)

    # --- Cake ---
    c_x = scene_x + (scene_w // 2) - 115
    c_y = hb_y + 60
    c_w, c_h = 165, 140

    # Cake plate
    sketch_rrect(draw, (c_x - 30, c_y + c_h + 5, c_x + c_w + 30, c_y + c_h + 20), fill=(220, 215, 208), outline=GRAY, width=1, r=6)

    # Cake layers (3 tiers)
    colors = [(245, 205, 185), (235, 195, 175), (225, 185, 165)]
    for i in range(3):
        off = i * 12
        layer_h = 34
        ly2 = c_y + i * layer_h
        sketch_rrect(draw, (c_x - off + i * 10, ly2, c_x + c_w + off - i * 10, ly2 + layer_h), fill=colors[i], outline=BROWN, width=1, r=4)
        # Frosting drips
        for d in range(6):
            dx = c_x - off + i * 10 + 15 + d * 24
            if dx > c_x + c_w + off - i * 10 - 12:
                continue
            dy = ly2 + layer_h
            drip_h = random.randint(6, 14)
            draw.ellipse([dx - 5, dy - 3, dx + 5, dy + drip_h], fill=(200, 170, 155))

    # Chocolate frosting top
    frosting_y = c_y - 10
    sketch_rrect(draw, (c_x - 14, frosting_y, c_x + c_w + 14, frosting_y + 16), fill=(90, 55, 35), outline=BROWN, width=1, r=4)

    # Candle
    v_x = c_x + c_w // 2 - 5
    v_y = c_y - 60
    sketch_rect(draw, (v_x, v_y, v_x + 10, c_y - 11), fill=(255, 252, 240), outline=INK, width=1)
    # Candle stripes
    for s in range(3):
        sketch_line(draw, [(v_x + 1, v_y + 10 + s * 14), (v_x + 9, v_y + 10 + s * 14)], (200, 180, 220), 1, 0.2)
    # Flame
    f_top = (v_x + 5, v_y - 6)
    f_l = (v_x - 7, v_y + 12)
    f_r = (v_x + 17, v_y + 12)
    draw.polygon(jit([f_top, f_l, f_r], 1.5), fill=(255, 200, 60))
    draw.polygon(jit([(v_x + 5, v_y + 2), (v_x, v_y + 10), (v_x + 10, v_y + 10)], 0.8), fill=(255, 255, 220))
    # Glow
    draw.ellipse(jit([(v_x - 12, v_y - 10), (v_x + 22, v_y + 22)], 1), fill=(255, 220, 100, 30))

    lbl(draw, (c_x + c_w // 2, c_y + c_h + 30), "Torta 3 pisos + vela + llama parpadeante", BROWN, f_small)

    # --- Gift Box ---
    g_x = c_x + c_w + 55
    g_y = c_y + 35
    g_s = 70
    # Shadow
    sketch_rrect(draw, (g_x + 5, g_y + g_s + 5, g_x + g_s + 5, g_y + g_s + 12), fill=(200, 195, 188), outline=None)
    # Box body
    sketch_rrect(draw, (g_x, g_y, g_x + g_s, g_y + g_s), fill=(255, 210, 210), outline=RED, width=2, r=3)
    # Ribbon vertical
    sketch_line(draw, [(g_x + g_s // 2, g_y), (g_x + g_s // 2, g_y + g_s)], RED, 3, 0.5, 2)
    # Ribbon horizontal
    sketch_line(draw, [(g_x, g_y + g_s // 2), (g_x + g_s, g_y + g_s // 2)], RED, 3, 0.5, 2)
    # Bow loops
    draw.polygon(jit([(g_x + g_s // 2, g_y - 4), (g_x + g_s // 2 - 14, g_y - 18), (g_x + g_s // 2 + 14, g_y - 18)], 0.5), fill=(220, 50, 50))
    draw.polygon(jit([(g_x + g_s // 2, g_y - 4), (g_x + g_s // 2 - 9, g_y - 14), (g_x + g_s // 2 + 9, g_y - 14)], 0.5), fill=(240, 80, 80))
    # Bow knot
    draw_circle(draw, g_x + g_s // 2, g_y - 4, 3, fill=(200, 40, 40))
    # Lid
    sketch_rrect(draw, (g_x - 5, g_y - 10, g_x + g_s + 5, g_y + 2), fill=(255, 220, 220), outline=RED, width=1, r=3)
    # Stars around gift
    for s in range(7):
        angle = s * (2 * math.pi / 7)
        sx_ = g_x + g_s // 2 + int(45 * math.cos(angle))
        sy_ = g_y + g_s // 2 + int(45 * math.sin(angle))
        draw_star(draw, sx_, sy_, 7, fill=GOLD)

    lbl(draw, (g_x + g_s // 2, g_y + g_s + 16), "Regalo (rebote + 7 estrellas giratorias)", RED, f_small)

    # --- Love Letter Modal (small preview) ---
    mod_x = g_x + 95
    mod_y = g_y + 5
    mod_w, mod_h = 120, 85
    # Modal overlay hint
    sketch_rrect(draw, (mod_x, mod_y, mod_x + mod_w, mod_y + mod_h), fill=(255, 245, 245), outline=RED, width=1, r=5)
    # Speech bubble tail
    sketch_line(draw, [(mod_x + 18, mod_y + mod_h), (mod_x + 12, mod_y + mod_h + 10), (mod_x + 28, mod_y + mod_h)], RED, 1, 0.3)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 12), "Carta de amor", PINK, f_small)
    sketch_line(draw, [(mod_x + 8, mod_y + 22), (mod_x + mod_w - 8, mod_y + 22)], (PINK[0], PINK[1], PINK[2], 80), 1, 0.3)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 32), "Mi Querida Mar...", INK, f_tiny)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 46), "Hoy el mundo est\u00e1", GRAY, f_tiny)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 57), "m\u00e1s bonito...", GRAY, f_tiny)
    lbl(draw, (mod_x + mod_w // 2, mod_y + 72), "~ Alex ~", PINK, f_tiny)

    # Arrow from gift to modal
    arrow(draw, (g_x + g_s, g_y + 30), (mod_x, mod_y + 40), RED, 1, 0.5)

    # --- Table ---
    tab_x = scene_x + 25
    tab_y = scene_y + scene_h - 80
    tab_w = scene_w - 50
    tab_h = 35
    # Table shadow
    sketch_rect(draw, (tab_x + 8, tab_y + tab_h + 5, tab_x + tab_w + 8, tab_y + tab_h + 55), fill=(200, 195, 188), outline=None)
    # Table top
    sketch_rect(draw, (tab_x, tab_y, tab_x + tab_w, tab_y + tab_h), fill=(185, 155, 120), outline=BROWN, width=2)
    # Wood grain
    for g in range(4):
        gy = tab_y + 7 + g * 7
        sketch_line(draw, [(tab_x + 10, gy), (tab_x + tab_w - 10, gy)], (165, 135, 105), 1, 0.5)
    # Table legs
    sketch_line(draw, [(tab_x + 35, tab_y + tab_h), (tab_x + 20, tab_y + tab_h + 50)], BROWN, 3, 0.8, 2)
    sketch_line(draw, [(tab_x + tab_w - 35, tab_y + tab_h), (tab_x + tab_w - 20, tab_y + tab_h + 50)], BROWN, 3, 0.8, 2)
    # Crossbar
    sketch_line(draw, [(tab_x + 20, tab_y + tab_h + 35), (tab_x + tab_w - 20, tab_y + tab_h + 35)], BROWN, 1, 0.5)

    lbl(draw, (tab_x + tab_w // 2, tab_y + tab_h // 2), "Mesa de madera (CSS + box-shadow)", BROWN, f_small)

    # --- Overlay indicator ---
    ov_x = scene_x + scene_w - 70
    ov_y = scene_y + 10
    sketch_rrect(draw, (ov_x, ov_y, ov_x + 55, ov_y + 50), fill=(30, 30, 30), outline=INK, width=1, r=3)
    lbl(draw, (ov_x + 27, ov_y + 18), "Overlay", (180, 180, 180), f_tiny)
    lbl(draw, (ov_x + 27, oy := ov_y + 32), "oscuro", (150, 150, 150), f_tiny)
    lbl(draw, (ov_x + 27, oy + 14), "(fade out)", (120, 120, 120), f_tiny)
    dashed_line(draw, (ov_x + 27, ov_y + 50), (ov_x + 27, scene_y + scene_h - 10), fill=INK, rough=0.5)

    # --- Layer indicators ---
    layer_data = [
        (scene_x + scene_w + 12, scene_y + 15, "z-index: 9999", "Overlay oscuro", INK),
        (scene_x + scene_w + 12, scene_y + 45, "z-index: 10000", "Llama (click)", ORANGE),
        (scene_x + scene_w + 12, scene_y + 75, "z-index: 2", "Confeti frente", BLUE),
        (scene_x + scene_w + 12, scene_y + 105, "z-index: 0", "Confeti fondo", BLUE),
    ]
    for lx_, ly_, idx, name, col in layer_data:
        sketch_rrect(draw, (lx_ - 4, ly_ - 3, lx_ + 120, ly_ + 14), fill=None, outline=col, width=1, r=3)
        lbl(draw, (lx_ + 4, ly_ + 1), idx, col, f_tiny, align="left")
        lbl(draw, (lx_ + 4, ly_ + 11), name, GRAY, f_tiny, align="left")

    # ===================================================================
    # SCENE LEGEND (below scene)
    # ===================================================================
    leg_x = lx + 18
    leg_y = scene_y + scene_h + 10
    leg_w = scene_w + 40
    sketch_rrect(draw, (leg_x, leg_y, leg_x + leg_w, leg_y + 390), fill=(252, 249, 242), outline=GRAY, width=1, r=5)

    lbl(draw, (leg_x + leg_w // 2, leg_y + 14), "ELEMENTOS DE LA ESCENA", INK, f_bold_title)
    sketch_line(draw, [(leg_x + leg_w // 2 - 80, leg_y + 26), (leg_x + leg_w // 2 + 80, leg_y + 26)], GRAY, 1, 0.3)

    elems = [
        ("1", "Fondo rosa pastel", "rgba(255, 182, 193) \u2014 canvas confeti", PINK),
        ("2", "Portarretrato de madera", "Mar.mp4 en loop \u2014 box-shadow + border", BROWN),
        ("3", "Texto 'Happy Birthday'", "Pacifico 40px \u2014 anim flotar + brillo", PINK),
        ("4", "Torta de 3 pisos", "CSS puro \u2014 frosting + chocolate drip", BROWN),
        ("5", "Vela con llama", "radial-gradient + keyframe flama 0.15s", ORANGE),
        ("6", "Caja de regalo", "rebote con cinta + techo + base + sombra", RED),
        ("7", "7 estrellas giratorias", "clip-path polygon + 2 keyframes", GOLD),
        ("8", "Carta de amor (modal)", "Georgia serif \u2014 click regalo \u2192 aparecer", PINK),
        ("9", "Overlay oscuro", "opacity 1\u21920 al clickear llama", INK),
        ("10", "Audio soplido + cancion", "soplar1.mp3 + cancion.mp3", BLUE),
        ("11", "Footer 'Hecho con amor'", "Pacifico 14px \u2014 fixed bottom-right", GRAY),
        ("12", "Confeti 2 capas (parallax)", "Canvas 2D \u2014 100 particulas c/u", TEAL),
    ]

    for i, (num, titl, desc, col) in enumerate(elems):
        col_idx = i % 2
        row = i // 2
        row_y = leg_y + 35 + row * 42
        row_x = leg_x + 15 + col_idx * (leg_w // 2)

        # Number badge
        draw_circle(draw, row_x, row_y + 5, 8, fill=col)
        lbl(draw, (row_x, row_y + 5), num, (255, 255, 255), f_tiny)
        # Title
        lbl(draw, (row_x + 14, row_y), titl, INK, f_bold or f_normal, align="left")
        # Description
        lbl(draw, (row_x + 14, row_y + 14), desc, GRAY, f_tiny, align="left")
        # Separator
        sketch_line(draw, [(row_x - 5, row_y + 28), (row_x + leg_w // 2 - 40, row_y + 28)], (235, 230, 222), 1, 0.2)

    # ===================================================================
    # CENTER PANEL: ARCHITECTURE
    # ===================================================================
    cx0 = lx + lw + 18
    cy0 = ly
    cw = 600
    ch = lh
    sketch_rrect(draw, (cx0, cy0, cx0 + cw, cy0 + ch), fill=(255, 252, 246), outline=GRAY, width=1, r=10)

    lbl(draw, (cx0 + cw // 2, cy0 + 14), "ARQUITECTURA T\u00c9CNICA", INK, f_bold_title)
    sketch_line(draw, [(cx0 + 15, cy0 + 28), (cx0 + cw - 15, cy0 + 28)], GRAY, 1, 0.3)

    def arch_box(x, y, w, h, title, items, color=BLUE, title_bg=None):
        sketch_rrect(draw, (x, y, x + w, y + h), fill=(255, 255, 255), outline=color, width=1, r=5)
        if title_bg:
            draw.rectangle([x + 2, y + 2, x + w - 2, y + 24], fill=title_bg)
        lbl(draw, (x + w // 2, y + 14), title, color, f_bold_title)
        sketch_line(draw, [(x + 10, y + 26), (x + w - 10, y + 26)], color, 1, 0.2)
        for i, item in enumerate(items):
            lbl(draw, (x + 12, y + 34 + i * 15), item, INK, f_small, align="left")

    # HTML
    arch_box(cx0 + 12, cy0 + 35, cw - 24, 195, "index.html", [
        "Meta viewport + favicon (cumplea\u00f1os.png)",
        "Google Fonts: Pacifico via CDN",
        "Canvas #canvas1 (z:0, confeti fondo)",
        "Canvas #canvas2 (z:2, confeti frente)",
        "Video Mar.mp4 autoplay muted loop",
        "Torta + vela + llama (CSS puro)",
        "Caja regalo: cinta + techo + base + sombra",
        "5 estrellas clip-path polygon",
        "Modal carta: Georgia serif, anim aparecer",
        "Audio: soplar1.mp3 + cancion.mp3 preload",
        "Overlay: opacity 1\u21920, transition 1.5s",
    ], BLUE, (235, 245, 255))

    # CSS
    arch_box(cx0 + 12, cy0 + 240, cw - 24, 160, "styles.css (660 l\u00edneas) + mobile.css (36 l\u00edneas)", [
        "Layout: flexbox centrado, overflow hidden",
        "@keyframes: flama, apagar, flotar, brillo",
        "  aparecer, latir, cinta, base, techo, sombra",
        "  estrella1, estrella2 (2 direcciones)",
        "Regalo: clip-path, box-shadow, transform",
        "Carta: gradient, border 3px, box-shadow glow",
        "Torta: border-radius, before/after pseudo",
        "Vela: radial-gradient + filter blur",
        "mobile: calc(100vw/650), tap-highlight: none",
    ], GREEN, (235, 250, 235))

    # JS
    arch_box(cx0 + 12, cy0 + 410, cw - 24, 195, "JavaScript (3 archivos)", [
        "Confeti.js (z:0) \u2014 Canvas 2D, 100 particulas",
        "  rgba(255,182,193,1) fondo, requestAF",
        "  Caida infinita, random x/speed/radio",
        "",
        "Confeti2.js (z:2) \u2014 mismsa l\u00f3gica",
        "  clearRect transparente, efecto parallax",
        "",
        "Sorpresa.js \u2014 interactividad:",
        "  click llama: play soplar1 \u2192 apagar",
        "    1s delay \u2192 overlay fade \u2192 cancion",
        "  click regalo: modal.classList.add('activo')",
        "  click overlay carta: quitar modal",
    ], PURPLE, (245, 235, 255))

    # Assets
    arch_box(cx0 + 12, cy0 + 615, cw - 24, 105, "recursos/ (Assets)", [
        "Mar.mp4 \u2014 Video de Mar en loop",
        "cancion.mp3 \u2014 Canci\u00f3n de cumplea\u00f1os",
        "soplar1.mp3 \u2014 Efecto de soplido",
        "soplar2.mp3 \u2014 (disponible, sin uso actual)",
        "cumpleanos.png \u2014 Favicon 32x32",
    ], RED, (255, 240, 240))

    # Interaction Flow
    arch_box(cx0 + 12, cy0 + 730, cw - 24, 180, "Flujo de interacci\u00f3n del usuario", [
        "1. Pagina carga \u2192 overlay negro visible",
        "   Confeti empieza a caer (Canvas 2D)",
        "2. Click LLAMA de la vela:",
        "   a) play soplar1.mp3 (soplido)",
        "   b) @keyframes apagar: scale(1)\u2192scale(0)",
        "   c) 1s delay \u2192 overlay.style.opacity=0",
        "   d) play cancion.mp3 (cumplea\u00f1os)",
        "3. Click CAJA DE REGALO:",
        "   a) modal.classList.add('activo')",
        "   b) Carta aparece con animaci\u00f3n",
        "   c) Click fondo modal \u2192 cierra",
        "4. Confeti sigue cayendo infinitamente",
    ], ORANGE, (255, 248, 235))

    # Deploy + Deps
    arch_box(cx0 + 12, cy0 + 920, (cw - 24) // 2 - 5, 80, "Deploy", [
        "Est\u00e1tico \u2014 sin build tools",
        "Netlify / Netlify Drop",
        "Solo arrastrar carpeta",
    ], GREEN, (240, 250, 240))

    arch_box(cx0 + (cw - 24) // 2 + 17, cy0 + 920, (cw - 24) // 2 - 5, 80, "Dependencias", [
        "CERO dependencias externas",
        "HTML + CSS + JS vanilla",
        "Google Fonts (Pacifico) CDN",
    ], PURPLE, (245, 240, 255))

    # Git
    arch_box(cx0 + 12, cy0 + 1010, cw - 24, 65, "Git / Repository", [
        "github.com/alexperezalvarez/FelizCumple.git",
        "Rama: main \u2014 Autor: Alex \u2014 Julio 2026",
    ], BLUE, (235, 242, 255))

    # Arrows between boxes
    arrow(draw, (cx0 + cw // 2, cy0 + 230), (cx0 + cw // 2, cy0 + 240), INK, 1, 0.5)
    arrow(draw, (cx0 + cw // 2, cy0 + 400), (cx0 + cw // 2, cy0 + 410), INK, 1, 0.5)
    arrow(draw, (cx0 + cw // 2, cy0 + 605), (cx0 + cw // 2, cy0 + 615), INK, 1, 0.5)
    arrow(draw, (cx0 + cw // 2, cy0 + 720), (cx0 + cw // 2, cy0 + 730), INK, 1, 0.5)
    arrow(draw, (cx0 + cw // 2, cy0 + 910), (cx0 + cw // 2, cy0 + 920), INK, 1, 0.5)
    arrow(draw, (cx0 + cw // 2, cy0 + 1000), (cx0 + cw // 2, cy0 + 1010), INK, 1, 0.5)

    # Divider
    sketch_line(draw, [(cx0 - 5, cy0 + 20), (cx0 - 5, cy0 + ch - 15)], GRAY, 1, 0.3, 2)

    # ===================================================================
    # RIGHT PANEL: DATA FLOW + TECHNICAL DETAILS
    # ===================================================================
    rx0 = cx0 + cw + 18
    ry0 = ly
    rw = W - rx0 - 25
    rh = lh
    sketch_rrect(draw, (rx0, ry0, rx0 + rw, ry0 + rh), fill=(255, 252, 246), outline=GRAY, width=1, r=10)

    lbl(draw, (rx0 + rw // 2, ry0 + 14), "FLUJO DE DATOS Y DETALLES", INK, f_bold_title)
    sketch_line(draw, [(rx0 + 15, ry0 + 28), (rx0 + rw - 15, ry0 + 28)], GRAY, 1, 0.3)

    def info_box(x, y, w, h, title, items, color=BLUE, title_bg=None):
        sketch_rrect(draw, (x, y, x + w, y + h), fill=(255, 255, 255), outline=color, width=1, r=5)
        if title_bg:
            draw.rectangle([x + 2, y + 2, x + w - 2, y + 24], fill=title_bg)
        lbl(draw, (x + w // 2, y + 14), title, color, f_bold_title)
        sketch_line(draw, [(x + 10, y + 26), (x + w - 10, y + 26)], color, 1, 0.2)
        for i, item in enumerate(items):
            lbl(draw, (x + 12, y + 34 + i * 15), item, INK, f_small, align="left")

    # CSS Animation details
    info_box(rx0 + 12, ry0 + 35, rw - 24, 170, "Animaciones CSS (@keyframes)", [
        "flama    0.15s  alternate  \u2192 llama titila",
        "apagar   0.5s   forwards   \u2192 llama desaparece",
        "flotar   2s     infinite   \u2192 texto sube/baja",
        "brillo   1.5s   infinite   \u2192 text-shadow pulse",
        "aparecer 0.8s   ease       \u2192 modal escala 0.9\u21921",
        "latir    1.2s   infinite   \u2192 corazon escala",
        "cinta    1.5s   infinite   \u2192 lazo rebota",
        "base     1.5s   infinite   \u2192 base comprime",
        "techo    1.5s   infinite   \u2192 tapa rebota",
        "sombra   1.5s   infinite   \u2192 sombra escala",
        "estrella 1.5s   infinite   \u2192 clip-path rotate",
    ], ORANGE, (255, 248, 235))

    # Responsive
    info_box(rx0 + 12, ry0 + 215, rw - 24, 100, "Responsive Design", [
        "mobile.css: transform scale(100vw/650)",
        "Solo para pantallas < 768px",
        "Deshabilitar -webkit-tap-highlight-color",
        "user-scalable=no en viewport meta",
        "overflow:hidden en html (sin scroll)",
    ], TEAL, (235, 248, 245))

    # Performance
    info_box(rx0 + 12, ry0 + 325, rw - 24, 100, "Performance y Optimizaci\u00f3n", [
        "Canvas 2D: requestAnimationFrame (60fps)",
        "Audio preload='auto' para respuesta r\u00e1pida",
        "CSS animations (GPU accelerated)",
        "Sin frameworks \u2014 peso m\u00ednimo",
        "Video muted autoplay (sin bloqueo)",
    ], GREEN, (235, 250, 235))

    # z-index map
    info_box(rx0 + 12, ry0 + 435, rw - 24, 130, "Mapa de z-index", [
        "  0  Canvas confeti fondo (Confeti.js)",
        "  1  .contenedor \u2014 escena visual",
        "  2  Canvas confeti frente (Confeti2.js)",
        " 999  Modal carta (.modal-carta)",
        "9999  Overlay oscuro (.overlay)",
        "10000 Llama (.llama) \u2014 click target",
        "10001 Footer (.footer-cumplea\u00f1os)",
    ], PURPLE, (245, 235, 255))

    # Key selectors
    info_box(rx0 + 12, ry0 + 575, rw - 24, 130, "Selectores CSS importantes", [
        ".torta:before \u2014 2 franjas rosas (box-shadow)",
        ".torta:after  \u2014 base roja de la torta",
        ".chocolate    \u2014 frosting drips (box-shadow)",
        ".soporte:before/after \u2014 patas de la mesa",
        ".cinta-de-regalo \u2014 lazo animado",
        ".regalo-sombra \u2014 sombra del regalo",
    ], BROWN, (250, 242, 235))

    # File sizes
    info_box(rx0 + 12, ry0 + 715, rw - 24, 100, "Tama\u00f1o de archivos", [
        "index.html  \u2014 ~3.5 KB (111 l\u00edneas)",
        "styles.css  \u2014 ~15 KB (660 l\u00edneas)",
        "mobile.css  \u2014 ~1 KB (36 l\u00edneas)",
        "Confeti.js  \u2014 ~2 KB",
        "Confeti2.js \u2014 ~2 KB",
        "Sorpresa.js \u2014 ~3 KB",
    ], INK, (245, 243, 240))

    # Browser compat
    info_box(rx0 + 12, ry0 + 825, rw - 24, 80, "Compatibilidad", [
        "Chrome / Edge / Firefox / Safari",
        "Mobile: iOS Safari, Chrome Android",
        "Requiere: soporte CSS clip-path",
    ], BLUE, (235, 242, 255))

    # Color palette
    info_box(rx0 + 12, ry0 + 915, rw - 24, 110, "Paleta de colores", [
        "Fondo:     rgba(255, 182, 193) \u2014 rosa pastel",
        "Torta:     #FDE8C8 (crema) + #ff5959 (rojo)",
        "Regalo:    #fe3f3f (cinta) + #e9e3e3 (base)",
        "Marco:     #bb7d4e (madera) + #8a5e3c (borde)",
        "Texto:     #ff4d6d (Happy Birthday)",
        "Mesa:      #4A4A4A (gris oscuro)",
    ], PINK, (255, 245, 248))

    # Summary stats
    info_box(rx0 + 12, ry0 + 1035, rw - 24, 80, "Resumen del Proyecto", [
        "6 archivos \u00b7 ~25 KB total \u00b7 0 dependencias",
        "HTML + CSS + JS vanilla \u00b7 Canvas 2D \u00b7 CSS animations",
        "Deploy: Netlify (arrastrar y soltar)",
    ], TEAL, (235, 248, 245))

    # Arrows between right panel boxes
    arrow(draw, (rx0 + rw // 2, ry0 + 205), (rx0 + rw // 2, ry0 + 215), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 315), (rx0 + rw // 2, ry0 + 325), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 425), (rx0 + rw // 2, ry0 + 435), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 565), (rx0 + rw // 2, ry0 + 575), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 705), (rx0 + rw // 2, ry0 + 715), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 815), (rx0 + rw // 2, ry0 + 825), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 905), (rx0 + rw // 2, ry0 + 915), INK, 1, 0.5)
    arrow(draw, (rx0 + rw // 2, ry0 + 1025), (rx0 + rw // 2, ry0 + 1035), INK, 1, 0.5)

    # Divider
    sketch_line(draw, [(rx0 - 5, ry0 + 20), (rx0 - 5, ry0 + ch - 15)], GRAY, 1, 0.3, 2)

    # --- Footer ---
    lbl(draw, (W // 2, H - 15), "Boceto generado digitalmente \u00b7 Estilo dibujado a mano \u00b7 Arial \u00b7 Julio 2026", GRAY, f_small)

    # --- Save ---
    out_png = "D:/Feliz Cumplea\u00f1os/boceto.png"
    img.save(out_png, "PNG")
    print(f"PNG guardado: {out_png}")

    out_pdf = "D:/Feliz Cumplea\u00f1os/boceto.pdf"
    img.save(out_pdf, "PDF", resolution=150)
    print(f"PDF guardado: {out_pdf}")


if __name__ == "__main__":
    main()
