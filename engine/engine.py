import math, random, wave, os, sys, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = "/tmp/fonts/Roboto_v3.010/web/static/"
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + f"Roboto-{w}.ttf", s)
    return _fc[k]

# brand (from aileadfinders.com computed styles)
NAVY = (0, 7, 35); NAVY2 = (3, 17, 38); GOLD = (252, 191, 73); ORANGE = (247, 127, 0)
SKY = (66, 153, 225); TEAL = (0, 48, 73); WHITE = (255, 255, 255); GRAY = (150, 162, 180); GREEN = (52, 199, 89)
PHONE = "908-332-9330"; URL = "aileadfinders.com"
VOICE = "/tmp/voices/en-us-libritts-high.onnx"; SPK = {"M": 7, "F": 30}

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def fade(c, a): return tuple(int(v * a + NAVY[i] * (1 - a)) for i, v in enumerate(c))

random.seed(7)
PARTS = [(random.random() * W, random.random() * H, random.uniform(0.3, 1.2), random.uniform(1, 2.6)) for _ in range(80)]

def base(t):
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    # soft radial glow
    g = Image.new("L", (W // 4, H // 4), 0); gd = ImageDraw.Draw(g)
    cx, cy = W // 8 + int(40 * math.sin(t * 0.5)), H // 8 - 40
    gd.ellipse([cx - 160, cy - 160, cx + 160, cy + 160], fill=70)
    g = g.filter(ImageFilter.GaussianBlur(60)).resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), (10, 30, 80)), im, g); d = ImageDraw.Draw(im)
    off = (t * 30) % 120
    for x in range(-120, W + 120, 120): d.line([(x + off, 0), (x + off, H)], fill=(8, 18, 48), width=1)
    for y in range(-120, H + 120, 120): d.line([(0, y + off), (W, y + off)], fill=(8, 18, 48), width=1)
    for (px, py, sp, r) in PARTS:
        y = (py - t * 50 * sp) % H; a = 0.35 + 0.35 * math.sin(t * 2 + px)
        d.ellipse([px - r, y - r, px + r, y + r], fill=fade(GOLD if px % 3 < 1 else SKY, a))
    return im

def layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def glow(im, L, blur=26, k=1.0):
    g = L.filter(ImageFilter.GaussianBlur(blur))
    if k != 1: g.putalpha(g.split()[3].point(lambda v: int(min(255, v * k))))
    im.paste(g, (0, 0), g); im.paste(L, (0, 0), L); return im

def ctext(d, y, s, f, fill, x=None): d.text((W // 2 if x is None else x, y), s, font=f, fill=fill, anchor="mm")

def fit(d, s, w, maxsize, weight="Black"):
    size = maxsize
    while size > 30 and d.textlength(s, font=F(weight, size)) > w: size -= 4
    return F(weight, size)

def phone_icon(d, x, y, s, col, bg=None):
    # classic telephone handset: thick arc + ear/mouth pieces
    w = max(3, int(s * 0.22))
    d.arc([x, y, x + s, y + s], 100, 260, fill=col, width=w)
    r = s * 0.2
    for ang in (100, 260):
        a = math.radians(ang); cx = x + s / 2 + (s / 2 - w / 2) * math.cos(a); cy = y + s / 2 + (s / 2 - w / 2) * math.sin(a)
        d.rounded_rectangle([cx - r * 0.2, cy - r * 0.75, cx + r * 1.35, cy + r * 0.75], int(r * 0.5), fill=col)

def check(d, cx, cy, s, col):
    d.line([(cx - s * 0.45, cy), (cx - s * 0.12, cy + s * 0.33), (cx + s * 0.48, cy - s * 0.38)], fill=col, width=max(3, int(s * 0.18)), joint="curve")

def chrome(im, caption, lt):
    d = ImageDraw.Draw(im)
    d.text((64, 104), "AI LEAD FINDERS", font=F("Bold", 34), fill=WHITE)
    d.rounded_rectangle([64, 150, 64 + 120, 156], 3, fill=GOLD)
    # footer bar (always on)
    d.rectangle([0, H - 150, W, H], fill=NAVY2); d.line([(0, H - 150), (W, H - 150)], fill=GOLD, width=3)
    d.text((64, H - 75), URL, font=F("Bold", 44), fill=WHITE, anchor="lm")
    pw = d.textlength(PHONE, font=F("Bold", 44))
    phone_icon(d, W - 64 - pw - 46, H - 98, 46, GOLD)
    d.text((W - 64, H - 75), PHONE, font=F("Bold", 44), fill=GOLD, anchor="rm")
    if caption:
        a = ease(lt / 0.25); f = fit(d, caption, W - 140, 56, "Bold")
        tw = d.textlength(caption, font=f)
        d.rounded_rectangle([W // 2 - tw / 2 - 30, H - 300, W // 2 + tw / 2 + 30, H - 205], 22, fill=fade((6, 20, 55), a))
        ctext(d, H - 252, caption, f, fade(WHITE, a))

# ---------------- scenes ----------------
def sc_slam(im, t, lt, p):
    L = layer(); d = ImageDraw.Draw(L); lines = p["lines"]; cols = p.get("colors", [WHITE] * len(lines))
    y0 = p.get("y", 860) - (len(lines) - 1) * p.get("gap", 170) / 2
    for i, (s, c) in enumerate(zip(lines, cols)):
        k = (lt - i * p.get("stagger", 0.18)) / 0.3
        if k <= 0: continue
        sc = 0.6 + 0.4 * back(k); f = fit(d, s, W - 120, int(p.get("size", 150) * sc))
        d.text((W // 2, y0 + i * p.get("gap", 170)), s, font=f, fill=c + (255,), anchor="mm")
    if p.get("badge"):
        k = back((lt - 0.4) / 0.3)
        if k > 0:
            bw = 280 * k; by = y0 + len(lines) * p.get("gap", 170) + 30
            d.rounded_rectangle([W // 2 - bw / 2, by - 55, W // 2 + bw / 2, by + 55], 55, fill=GOLD + (255,))
            d.text((W // 2, by), p["badge"], font=F("Black", int(64 * k) + 1), fill=TEAL + (255,), anchor="mm")
    return glow(im, L, 34, 0.7)

def phone_frame(d, px=240, py=330, pw=600, ph=1080):
    d.rounded_rectangle([px, py, px + pw, py + ph], 80, fill=(4, 12, 30), outline=(60, 75, 105), width=6)
    d.rounded_rectangle([px + pw // 2 - 70, py + 30, px + pw // 2 + 70, py + 62], 16, fill=(20, 28, 48))
    return px, py, pw, ph

def sc_call(im, t, lt, p):
    d = ImageDraw.Draw(im); px, py, pw, ph = phone_frame(d); cx = px + pw // 2
    state = p["state"]
    col = {"ring": GOLD, "missed": ORANGE, "answered": GOLD}[state]
    if state == "ring":
        for k in range(3):
            r = 120 + ((lt * 1.2 + k / 3) % 1) * 220; a = 1 - ((lt * 1.2 + k / 3) % 1)
            d.ellipse([cx - r, 760 - r, cx + r, 760 + r], outline=fade(GOLD, a * 0.8), width=4)
    L = layer(); g = ImageDraw.Draw(L)
    g.ellipse([cx - 110, 650, cx + 110, 870], fill=col + (255,)); im = glow(im, L, 30, 0.8); d = ImageDraw.Draw(im)
    phone_icon(d, cx - 52, 708, 104, NAVY)
    ctext(d, 450, p.get("who", "Seller"), F("Bold", 64), WHITE)
    ctext(d, 525, p.get("sub", "Incoming call · 9:04 PM"), F("Regular", 38), GRAY)
    if state == "missed":
        k = back(lt / 0.3)
        if k > 0:
            bw = 420 * k
            d.rounded_rectangle([cx - bw / 2, 960, cx + bw / 2, 1060], 50, fill=ORANGE)
            ctext(d, 1010, "MISSED CALL", F("Black", int(52 * k) + 1), WHITE)
    if state == "answered":
        ctext(d, 960, "AI Voice Agent", F("Bold", 48), GOLD)
        ctext(d, 1020, "Answered in 3 seconds", F("Regular", 38), WHITE)
        for i in range(28):
            x = px + 80 + i * 16; amp = 20 + 60 * abs(math.sin(lt * 8 + i * 0.7)) * (0.5 + 0.5 * math.sin(i * 0.4))
            d.rounded_rectangle([x, 1150 - amp, x + 8, 1150 + amp], 4, fill=GOLD)
    return im

def sc_qualify_cal(im, t, lt, p):
    d = ImageDraw.Draw(im); items = p["items"]
    for i, s in enumerate(items):
        k = ease((lt - i * 0.35) / 0.3)
        if k <= 0: continue
        y = 420 + i * 120; d.rounded_rectangle([140, y, 940, y + 92], 46, fill=fade(NAVY2, 1), outline=fade(GOLD, k), width=3)
        d.ellipse([170, y + 18, 226, y + 74], fill=fade(GOLD, k)); check(d, 198, y + 46, 30, TEAL)
        d.text((256, y + 46), s, font=F("Medium", 42), fill=fade(WHITE, k), anchor="lm")
    k = back((lt - len(items) * 0.35 - 0.1) / 0.35)
    if k > 0:
        y0 = 420 + len(items) * 120 + 60
        d.rounded_rectangle([140, y0, 940, y0 + 330], 34, fill=(8, 22, 52), outline=(50, 70, 110), width=2)
        d.text((180, y0 + 50), p.get("day", "THURSDAY"), font=F("Bold", 34), fill=GRAY, anchor="lm")
        for j, hr in enumerate(["9 AM", "10 AM", "11 AM"]):
            d.text((180, y0 + 120 + j * 75), hr, font=F("Regular", 32), fill=GRAY, anchor="lm")
            d.line([(300, y0 + 120 + j * 75), (900, y0 + 120 + j * 75)], fill=(30, 45, 80), width=2)
        L = layer(); g = ImageDraw.Draw(L); slot = p.get("slot", 1); sy = y0 + 92 + slot * 75
        g.rounded_rectangle([310, sy, 310 + 580 * min(1, k), sy + 62], 14, fill=GOLD + (255,))
        im = glow(im, L, 18, 0.8); d = ImageDraw.Draw(im)
        if k > 0.6: d.text((335, sy + 31), p.get("appt", "Listing appt · Booked by AI"), font=F("Bold", 34), fill=TEAL, anchor="lm")
    return im

PINS = [(random.uniform(150, 930), random.uniform(560, 1300), random.uniform(0, 1.0)) for _ in range(22)]
def sc_map(im, t, lt, p):
    d = ImageDraw.Draw(im)
    for i in range(13):
        y = 520 + i * 64; d.line([(80, y), (1000, y)], fill=(18, 36, 80), width=2)
    for i in range(12):
        x = 100 + i * 80; d.line([(x, 520), (x + (x - 540) * 0.15, 1330)], fill=(18, 36, 80), width=2)
    L = layer(); g = ImageDraw.Draw(L)
    for (px, py, dl) in PINS:
        k = ease((lt - dl) / 0.3)
        if k <= 0: continue
        r = 15 * back((lt - dl) / 0.3); yy = py - 28 * k
        g.ellipse([px - r, yy - r, px + r, yy + r], fill=GOLD + (255,))
        g.polygon([(px - r * 0.6, yy + r * 0.5), (px + r * 0.6, yy + r * 0.5), (px, py)], fill=GOLD + (255,))
    im = glow(im, L, 16, 1.1); d = ImageDraw.Draw(im)
    tags = p.get("tags", [])
    for i, s in enumerate(tags):
        k = back((lt - 0.3 - i * 0.3) / 0.3)
        if k <= 0: continue
        x, y = [(260, 640), (760, 820), (300, 1020), (740, 1200)][i % 4]
        tw = d.textlength(s, font=F("Bold", 36)) + 50
        d.rounded_rectangle([x - tw / 2 * k, y - 34, x + tw / 2 * k, y + 34], 34, fill=ORANGE if i % 2 else SKY)
        if k > 0.7: ctext(d, y, s, F("Bold", 36), WHITE, x)
    if p.get("title"): ctext(d, 420, p["title"], F("Black", 72), WHITE)
    return im

def sc_sms(im, t, lt, p):
    d = ImageDraw.Draw(im); px, py, pw, ph = phone_frame(d, 160, 330, 760, 1100)
    ctext(d, py + 120, p.get("who", "Maria · Seller"), F("Bold", 42), WHITE)
    d.line([(px + 40, py + 170), (px + pw - 40, py + 170)], fill=(40, 55, 85), width=2)
    y = py + 210
    for i, (side, s) in enumerate(p["msgs"]):
        k = ease((lt - i * p.get("step", 0.75)) / 0.25)
        if k <= 0: continue
        f = F("Regular", 36); words = s.split(); lines = []; cur = ""
        for w_ in words:
            if d.textlength(cur + " " + w_, font=f) > 470: lines.append(cur.strip()); cur = w_
            else: cur += " " + w_
        lines.append(cur.strip()); bh = 30 + 46 * len(lines); bw = max(d.textlength(l, font=f) for l in lines) + 56
        x0 = px + 50 if side == "them" else px + pw - 50 - bw
        fill = (30, 44, 74) if side == "them" else GOLD; tc = WHITE if side == "them" else TEAL
        yy = y + int(20 * (1 - k))
        d.rounded_rectangle([x0, yy, x0 + bw, yy + bh], 30, fill=fade(fill, k))
        for j, l in enumerate(lines): d.text((x0 + 28, yy + 20 + j * 46), l, font=f, fill=fade(tc, k))
        y += bh + 24
    if p.get("stop"):
        ctext(d, py + ph - 70, "Opted-in contacts · Reply STOP to opt out", F("Regular", 28), GRAY)
    return im

def sc_pipeline(im, t, lt, p):
    d = ImageDraw.Draw(im); cols = p.get("cols", ["New", "Contacted", "Qualified", "Appointment"])
    cw = 230; gap = 20; x0 = (W - (cw * 4 + gap * 3)) // 2; y0 = 520
    for i, c in enumerate(cols):
        x = x0 + i * (cw + gap)
        d.rounded_rectangle([x, y0, x + cw, y0 + 760], 24, fill=(6, 18, 46), outline=(35, 55, 95), width=2)
        d.text((x + cw // 2, y0 + 50), c, font=F("Bold", 32 if len(c) < 11 else 28), fill=GOLD if i == 3 else WHITE, anchor="mm")
        for j in range(3 - (i == 3) * 2):
            d.rounded_rectangle([x + 18, y0 + 100 + j * 120, x + cw - 18, y0 + 200 + j * 120], 14, fill=(18, 34, 70))
    k = ease((lt - 0.2) / (p.get("dur", 1.8)))
    stage = k * 3; cx = x0 + stage * (cw + gap) + 18; cy = y0 + 100 + (360 if k > 0.98 else 0) * 0
    L = layer(); g = ImageDraw.Draw(L)
    g.rounded_rectangle([cx, cy, cx + cw - 36, cy + 100], 14, fill=(GOLD if k > 0.97 else SKY) + (255,))
    im = glow(im, L, 18, 0.9); d = ImageDraw.Draw(im)
    d.text((cx + 18, cy + 32), p.get("card", "Maria · Elm St"), font=F("Bold", 26), fill=TEAL if k > 0.97 else WHITE)
    d.text((cx + 18, cy + 66), "Thu 11 AM" if k > 0.97 else "in progress", font=F("Regular", 24), fill=TEAL if k > 0.97 else WHITE)
    if p.get("title"): ctext(d, 420, p["title"], F("Black", 66), WHITE)
    return im

def sc_channels(im, t, lt, p):
    L = layer(); g = ImageDraw.Draw(L); words = p["words"]; cols = [GOLD, SKY, ORANGE, WHITE]
    for i, w_ in enumerate(words):
        k = (lt - i * p.get("step", 0.5)) / 0.25
        if k <= 0: continue
        s = back(k); y = 640 + i * 230
        g.text((W // 2, y), w_, font=F("Black", int(140 * (0.7 + 0.3 * s))), fill=WHITE + (255,), anchor="mm")
        g.rounded_rectangle([W // 2 - 260, y + 85, W // 2 + 260, y + 97], 6, fill=cols[i % 4] + (255,))
    return glow(im, L, 30, 0.6)

def sc_form(im, t, lt, p):
    d = ImageDraw.Draw(im); x0, y0 = 140, 470
    d.rounded_rectangle([x0, y0, x0 + 800, y0 + 760], 34, fill=(8, 22, 52), outline=(50, 70, 110), width=2)
    d.text((x0 + 50, y0 + 70), "Find your next home", font=F("Bold", 46), fill=WHITE, anchor="lm")
    fields = [("Name", "Jordan Smith"), ("Phone", "(908) 555-0142"), ("Looking in", "Union County, NJ")]
    total = sum(len(v) for _, v in fields); shown = lt / 1.6 * total
    for i, (lab, v) in enumerate(fields):
        y = y0 + 150 + i * 160; d.text((x0 + 50, y), lab, font=F("Medium", 30), fill=GRAY)
        d.rounded_rectangle([x0 + 50, y + 44, x0 + 750, y + 124], 16, fill=(16, 32, 66))
        n = int(max(0, min(len(v), shown))); shown -= len(v)
        d.text((x0 + 74, y + 84), v[:n], font=F("Regular", 38), fill=WHITE, anchor="lm")
    k = 1 + 0.08 * math.sin(lt * 10) if lt > 1.7 else 1
    bw = 300 * k; by = y0 + 660
    d.rounded_rectangle([x0 + 400 - bw / 2, by - 45, x0 + 400 + bw / 2, by + 45], 45, fill=GOLD)
    ctext(d, by, "Submit", F("Bold", 40), TEAL, x0 + 400)
    return im

def sc_chips(im, t, lt, p):
    d = ImageDraw.Draw(im); items = p["items"]
    if p.get("title"): ctext(d, 520, p["title"], F("Black", 70), WHITE)
    for i, (a, b) in enumerate(items):
        k = back((lt - 0.2 - i * 0.4) / 0.3)
        if k <= 0: continue
        y = 700 + i * 190; d.rounded_rectangle([140, y, 940, y + 140], 70, fill=(8, 24, 56), outline=GOLD, width=3)
        d.ellipse([170, y + 30, 250, y + 110], fill=GOLD); check(d, 210, y + 70, 42, TEAL)
        d.text((280, y + 48), a, font=F("Bold", 40), fill=WHITE, anchor="lm")
        d.text((280, y + 96), b, font=F("Regular", 32), fill=GRAY, anchor="lm")
    return im

def sc_week(im, t, lt, p):
    d = ImageDraw.Draw(im); days = ["MON", "TUE", "WED", "THU", "FRI"]; x0, y0, cw = 110, 460, 172
    if p.get("title"): ctext(d, 380, p["title"], F("Black", 62), WHITE)
    for i, dname in enumerate(days):
        x = x0 + i * cw; d.rounded_rectangle([x, y0, x + cw - 14, y0 + 860], 18, fill=(6, 18, 46))
        d.text((x + (cw - 14) // 2, y0 + 40), dname, font=F("Bold", 30), fill=GRAY, anchor="mm")
    L = layer(); g = ImageDraw.Draw(L); random.seed(3)
    slots = [(i, j) for i in range(5) for j in range(6) if random.random() < 0.55]
    filled = int(len(slots) * ease(lt / p.get("dur", 1.8))) if not p.get("empty") else 0
    for (i, j) in slots[:filled]:
        x = x0 + i * cw; y = y0 + 90 + j * 125
        g.rounded_rectangle([x + 10, y, x + cw - 24, y + 100], 12, fill=GOLD + (255,))
    im = glow(im, L, 14, 0.8); d = ImageDraw.Draw(im)
    for (i, j) in slots[:filled]:
        x = x0 + i * cw; y = y0 + 90 + j * 125
        d.text((x + 22, y + 30), "Appt", font=F("Bold", 26), fill=TEAL); d.text((x + 22, y + 64), "Booked", font=F("Regular", 22), fill=TEAL)
    if p.get("empty"):
        k = back((lt - 0.3) / 0.3)
        if k > 0: ctext(d, y0 + 430, "?", F("Black", int(260 * k) + 1), ORANGE)
    return im

def sc_book(im, t, lt, p):
    d = ImageDraw.Draw(im); ctext(d, 620, "30-minute", F("Bold", 64), WHITE); ctext(d, 710, "strategy call", F("Bold", 64), WHITE)
    tap = 0.9; k = 1 - 0.08 * math.exp(-((lt - tap) * 8) ** 2)
    bw, bh = 640 * k, 170 * k; by = 960
    L = layer(); g = ImageDraw.Draw(L)
    g.rounded_rectangle([W // 2 - bw / 2, by - bh / 2, W // 2 + bw / 2, by + bh / 2], 85, fill=GOLD + (255,))
    im = glow(im, L, 30, 1.0); d = ImageDraw.Draw(im)
    ctext(d, by, "Book a Call", F("Black", int(78 * k)), TEAL)
    if lt > tap:
        r = (lt - tap) * 700; a = max(0, 1 - (lt - tap) / 0.7)
        d.ellipse([W // 2 - r, by - r, W // 2 + r, by + r], outline=fade(GOLD, a), width=5)
    if lt > tap + 0.5:
        k2 = back((lt - tap - 0.5) / 0.3); ctext(d, 1170, "Booked", F("Bold", int(60 * k2) + 1), GREEN); check(d, W // 2 - 150, 1170, 50 * k2 + 1, GREEN)
    return im

def sc_end(im, t, lt, p):
    L = layer(); g = ImageDraw.Draw(L)
    a1, a2, a3, a4 = (ease((lt - s) / 0.3) for s in (0, 0.35, 0.8, 1.2))
    head = p.get("head", ["Book your", "strategy call"])
    for i, s in enumerate(head):
        g.text((W // 2, 520 + i * 120), s, font=F("Black", 104), fill=(WHITE if i == 0 else GOLD) + (int(255 * a1),), anchor="mm")
    if a2 > 0:
        s = 0.85 + 0.15 * back((lt - 0.35) / 0.3)
        g.rounded_rectangle([110, 860, 970, 1040], 90, fill=GOLD + (int(255 * a2),))
        g.text((W // 2, 950), PHONE, font=F("Black", int(96 * s)), fill=TEAL + (int(255 * a2),), anchor="mm")
    if a3 > 0:
        g.text((W // 2, 1150), URL, font=F("Bold", 76), fill=(255, 255, 255, int(255 * a3)), anchor="mm")
    im = glow(im, L, 30, 0.6); d = ImageDraw.Draw(im)
    if a4 > 0:
        ctext(d, 1280, p.get("sub", "Realtors · Investors · Wholesalers"), F("Medium", 42), fade(GRAY, a4))
        ctext(d, 1345, "New Jersey", F("Medium", 38), fade(GRAY, a4))
    return im

def sc_timer_wrap(fn):
    def w(im, t, lt, p):
        im = fn(im, t, lt, p)
        if "timer" in p:
            d = ImageDraw.Draw(im); a, b = p["timer"]; v = a + (b - a) * min(1, lt / max(0.01, p.get("tdur", 1.0)))
            s = f"{int(v // 60):02d}:{int(v % 60):02d}"; stop = p.get("stopped")
            d.rounded_rectangle([W - 330, 80, W - 64, 176], 48, fill=GOLD if stop else (10, 30, 70), outline=GOLD, width=3)
            d.text((W - 197, 128), ("Done " if stop else "") + s, font=F("Bold", 50), fill=TEAL if stop else GOLD, anchor="mm")
        return im
    return w

SCENES = {k: sc_timer_wrap(v) for k, v in dict(slam=sc_slam, call=sc_call, qualify=sc_qualify_cal, map=sc_map, sms=sc_sms,
          pipeline=sc_pipeline, channels=sc_channels, form=sc_form, chips=sc_chips, week=sc_week, book=sc_book, end=sc_end).items()}

def tts(text, spk, out):
    subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-s", str(SPK[spk]), "--length_scale", "0.93", "-f", out],
                   input=text.encode(), check=True, stderr=subprocess.DEVNULL)
    w = wave.open(out); return w.getnframes() / w.getframerate()

def render(name, beats, outdir="/tmp/ailf/out"):
    work = f"/tmp/ailf/work/{name}"; shutil.rmtree(work, ignore_errors=True); os.makedirs(work + "/f"); os.makedirs(outdir, exist_ok=True)
    durs = []
    for i, b in enumerate(beats):
        dd = tts(b["say"], b["spk"], f"{work}/v{i}.wav") if b.get("say") else 0
        durs.append(max(b.get("min", 0), dd + b.get("pad", 0.45)))
    starts = np.cumsum([0] + durs[:-1]); total = sum(durs); N = int(total * FPS)
    for fi in range(N):
        t = fi / FPS; bi = int(np.searchsorted(starts, t, side="right") - 1); lt = t - starts[bi]; b = beats[bi]
        im = SCENES[b["scene"]](base(t), t, lt, b.get("p", {}))
        if bi and lt < 0.08: im = Image.blend(im, Image.new("RGB", (W, H), (40, 50, 90)), 0.3 * (1 - lt / 0.08))
        chrome(im, b.get("cap"), lt)
        if fi > N - FPS * 0.35: im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), (fi - (N - FPS * 0.35)) / (FPS * 0.35))
        im.save(f"{work}/f/{fi:05d}.jpg", quality=90)
    SR = 22050; mix = np.zeros(int((total + 0.5) * SR))
    for i, b in enumerate(beats):
        if not b.get("say"): continue
        w = wave.open(f"{work}/v{i}.wav"); sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if sr != SR: x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * SR / sr)), np.arange(len(x)), x)
        st = int((starts[i] + 0.1) * SR); mix[st:st + len(x)] += x[:len(mix) - st] * 0.95
    tt = np.arange(int(0.25 * SR)) / SR; kick = np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14) * 0.35
    for s0 in starts: st = int(s0 * SR); mix[st:st + len(kick)] += kick[:len(mix) - st]
    ta = np.arange(len(mix)) / SR
    pad = (np.sin(2 * np.pi * 55 * ta) + 0.5 * np.sin(2 * np.pi * 82.4 * ta) + 0.3 * np.sin(2 * np.pi * 110 * ta)) * 0.045
    pad *= np.minimum(1, ta) * np.clip((total + 0.3 - ta) / 0.8, 0, 1)
    rng = np.random.default_rng(1); hat = np.zeros_like(mix)
    for k in range(int(total / 0.5)):
        st = int((k * 0.5 + 0.25) * SR); n = int(0.03 * SR); hat[st:st + n] += rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 120) * 0.035
    mix += pad + hat; mix /= max(1, np.abs(mix).max() / 0.95)
    with wave.open(f"{work}/a.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    out = f"{outdir}/{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{work}/f/%05d.jpg", "-i", f"{work}/a.wav",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    return out, total, starts
