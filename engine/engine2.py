import math, os, shutil, subprocess, wave, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine as E
from engine import (W, H, FPS, F, NAVY, NAVY2, GOLD, ORANGE, SKY, TEAL, WHITE, GRAY, GREEN, PHONE, URL,
                    ease, back, fade, layer, glow, ctext, fit, phone_icon, check, base, chrome)

# ---------------- natural voice (Kokoro) ----------------
_K = None
VOICES = {"F": "af_heart", "M": "am_michael"}
def tts(text, spk, out, speed=1.04):
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro("/tmp/kokoro/kokoro-v1.0.onnx", "/tmp/kokoro/voices-v1.0.bin")
    a, sr = _K.create(text, voice=VOICES[spk], speed=speed, lang="en-us")
    a = np.asarray(a, dtype=np.float32)
    # trim leading/trailing silence
    nz = np.where(np.abs(a) > 0.01)[0]
    if len(nz): a = a[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
    return a, sr

def envelope(a, sr, n):
    hop = sr / FPS; env = np.zeros(n)
    for i in range(n):
        s = a[int(i * hop): int((i + 1) * hop)]
        env[i] = np.sqrt((s ** 2).mean()) if len(s) else 0
    m = env.max() or 1; env = np.clip(env / (0.6 * m), 0, 1)
    sm = np.convolve(env, [0.25, 0.5, 0.25], "same")
    return sm

# ---------------- people (flat illustrated, brand palette) ----------------
SKIN = {"maya": (214, 160, 120), "daniel": (176, 120, 86), "c1": (236, 196, 160), "c2": (120, 82, 58)}
def person(L, cx, cy, s, who, mouth=0.0, blink=False, look=0, outfit=None):
    """chest-up frontal person drawn on RGBA layer L. cy = center of head."""
    d = ImageDraw.Draw(L); sk = SKIN.get(who, (210, 160, 120)) + (255,)
    dk = tuple(int(c * 0.82) for c in sk[:3]) + (255,)
    hair = {"maya": (58, 34, 22), "daniel": (24, 18, 16), "c1": (150, 100, 50), "c2": (20, 16, 14)}.get(who, (40, 30, 20)) + (255,)
    coat = (outfit or {"maya": (12, 30, 78), "daniel": (14, 34, 70), "c1": (130, 60, 70), "c2": (60, 80, 70)}.get(who, (40, 40, 60))) + (255,)
    hw, hh = 112 * s, 142 * s
    # hair back (maya)
    if who in ("maya", "c1"):
        d.rounded_rectangle([cx - hw * 1.22, cy - hh * 1.02, cx + hw * 1.22, cy + hh * 1.55], int(hw), fill=hair)
    # torso
    ty = cy + hh * 1.05
    d.rounded_rectangle([cx - hw * 2.6, ty + hh * 0.35, cx + hw * 2.6, ty + hh * 3.2], int(hw * 0.9), fill=coat)
    # shirt V
    shirt = ((244, 236, 222) if who != "daniel" else (245, 245, 245)) + (255,)
    d.polygon([(cx - hw * 0.62, ty + hh * 0.3), (cx + hw * 0.62, ty + hh * 0.3), (cx, ty + hh * 1.55)], fill=shirt)
    # lapels
    d.polygon([(cx - hw * 0.62, ty + hh * 0.3), (cx - hw * 1.2, ty + hh * 0.55), (cx - hw * 0.15, ty + hh * 1.75)], fill=tuple(int(c * 0.78) for c in coat[:3]) + (255,))
    d.polygon([(cx + hw * 0.62, ty + hh * 0.3), (cx + hw * 1.2, ty + hh * 0.55), (cx + hw * 0.15, ty + hh * 1.75)], fill=tuple(int(c * 0.78) for c in coat[:3]) + (255,))
    # neck
    d.rounded_rectangle([cx - hw * 0.38, cy + hh * 0.55, cx + hw * 0.38, ty + hh * 0.5], int(hw * 0.2), fill=dk)
    # ears
    for sx in (-1, 1):
        d.ellipse([cx + sx * hw * 0.98 - 18 * s, cy - 10 * s, cx + sx * hw * 0.98 + 18 * s, cy + 46 * s], fill=sk)
    # head
    d.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill=sk)
    # beard
    if who == "daniel":
        d.chord([cx - hw * 0.98, cy - hh * 0.25, cx + hw * 0.98, cy + hh * 1.02], 20, 160, fill=(36, 26, 22, 255))
        d.ellipse([cx - hw * 0.5, cy + hh * 0.28, cx + hw * 0.5, cy + hh * 0.62], fill=sk)
    # hair top
    if who in ("maya", "c1"):
        d.chord([cx - hw * 1.08, cy - hh * 1.08, cx + hw * 1.08, cy + hh * 0.35], 180, 360, fill=hair)
        d.pieslice([cx - hw * 1.3, cy - hh * 1.05, cx + hw * 0.4, cy + hh * 0.2], 200, 330, fill=hair)
    else:
        d.chord([cx - hw * 1.02, cy - hh * 1.12, cx + hw * 1.02, cy - hh * 0.05], 180, 360, fill=hair)
        d.rectangle([cx - hw * 1.0, cy - hh * 0.62, cx - hw * 0.86, cy - hh * 0.05], fill=hair)
        d.rectangle([cx + hw * 0.86, cy - hh * 0.62, cx + hw * 1.0, cy - hh * 0.05], fill=hair)
    # eyes
    ey = cy - hh * 0.08; ex = hw * 0.4
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.line([(x - 22 * s, ey), (x + 22 * s, ey)], fill=(40, 26, 20, 255), width=max(2, int(5 * s)))
        else:
            d.ellipse([x - 24 * s, ey - 15 * s, x + 24 * s, ey + 15 * s], fill=(255, 255, 255, 255))
            ix = x + look * 8 * s
            d.ellipse([ix - 12 * s, ey - 12 * s, ix + 12 * s, ey + 12 * s], fill=(52, 34, 24, 255))
            d.ellipse([ix - 5 * s, ey - 5 * s, ix + 5 * s, ey + 5 * s], fill=(10, 8, 8, 255))
            d.ellipse([ix + 2 * s, ey - 8 * s, ix + 7 * s, ey - 3 * s], fill=(255, 255, 255, 255))
        # brows (raise a little while speaking)
        by = ey - 38 * s - mouth * 6 * s
        d.line([(x - 26 * s, by + 4 * s), (x + 24 * s, by - 2 * s * sx * 0 - 2 * s)], fill=hair, width=max(3, int(8 * s)))
    # nose
    d.arc([cx - 16 * s, cy + hh * 0.05, cx + 16 * s, cy + hh * 0.32], 20, 160, fill=dk, width=max(2, int(5 * s)))
    # cheeks
    if who in ("maya", "c1"):
        for sx in (-1, 1):
            d.ellipse([cx + sx * hw * 0.55 - 22 * s, cy + hh * 0.18, cx + sx * hw * 0.55 + 22 * s, cy + hh * 0.36], fill=tuple(int(sk[i] * 0.72 + (235, 130, 120)[i] * 0.28) for i in range(3)) + (255,))
    # mouth (lip sync)
    my = cy + hh * 0.5; mw = 34 * s; mo = mouth
    lip = (170, 70, 70, 255) if who in ("maya", "c1") else (120, 60, 50, 255)
    if mo < 0.12:
        d.arc([cx - mw, my - 14 * s, cx + mw, my + 14 * s], 15, 165, fill=lip, width=max(3, int(6 * s)))
    else:
        oh = (8 + 30 * mo) * s; ow = mw * (0.75 + 0.25 * (1 - mo))
        d.ellipse([cx - ow, my - oh * 0.35, cx + ow, my + oh], fill=(70, 20, 24, 255), outline=lip, width=max(2, int(5 * s)))
        d.rectangle([cx - ow * 0.7, my - oh * 0.3, cx + ow * 0.7, my - oh * 0.3 + 7 * s], fill=(250, 250, 250, 255))
    # earrings (maya)
    if who == "maya":
        for sx in (-1, 1): d.ellipse([cx + sx * hw * 0.98 - 7 * s, cy + 50 * s, cx + sx * hw * 0.98 + 7 * s, cy + 64 * s], fill=GOLD + (255,))
    return d

def blink_at(t, seed=0): return ((t + seed * 1.7) % 3.7) < 0.12
def mouth_at(p, lt):
    env = p.get("_env");
    if env is None: return 0
    i = int(lt * FPS) - 3  # voice starts 0.1s in
    return float(env[i]) if 0 <= i < len(env) else 0

# ---------------- new scenes ----------------
def sc_presenter(im, t, lt, p):
    who = p.get("who", "maya"); m = mouth_at(p, lt); bob = m * 10
    # backdrop: glowing arch + optional room hint
    L = layer(); d = ImageDraw.Draw(L)
    d.ellipse([W // 2 - 470, 560, W // 2 + 470, 1500], fill=(16, 40, 96, 255))
    im = glow(im, L, 80, 0.9)
    L = layer(); d = ImageDraw.Draw(L)
    d.ellipse([W // 2 - 440, 590, W // 2 + 440, 1470], outline=GOLD + (200,), width=4)
    im = glow(im, L, 12, 1.0)
    P = layer(); person(P, W // 2 + int(6 * math.sin(t * 1.3)), 900 + bob, 1.55, who, mouth=m, blink=blink_at(t, 1 if who == "maya" else 2), look=0)
    # crop person bottom at footer area
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle([0, 0, W, H - 330], fill=255)
    P.putalpha(Image.composite(P.split()[3], Image.new("L", (W, H), 0), mask))
    im.paste(P, (0, 0), P)
    d = ImageDraw.Draw(im)
    # name tag
    k = ease((lt - 0.2) / 0.3)
    if k > 0 and p.get("name"):
        nm, role = p["name"]; x = 80 - int(60 * (1 - k)); y = 1430
        d.rounded_rectangle([x, y, x + 470, y + 104], 18, fill=fade(NAVY2, k), outline=fade(GOLD, k), width=3)
        d.text((x + 28, y + 30), nm, font=F("Bold", 38), fill=fade(WHITE, k), anchor="lm")
        d.text((x + 28, y + 74), role, font=F("Regular", 28), fill=fade(GOLD, k), anchor="lm")
    # floating text card top
    if p.get("card"):
        k = back((lt - 0.15) / 0.3)
        if k > 0:
            f = fit(d, p["card"], W - 200, 64, "Black"); tw = d.textlength(p["card"], font=f)
            d.rounded_rectangle([W // 2 - tw / 2 - 40, 250, W // 2 + tw / 2 + 40, 370], 30, fill=GOLD)
            ctext(d, 310, p["card"], f, TEAL)
    return im

def table_scene_bg(im, t):
    d = ImageDraw.Draw(im)
    # window w/ city lights
    d.rounded_rectangle([60, 260, W - 60, 980], 24, fill=(6, 16, 44))
    random.seed(11)
    for _ in range(70):
        x = random.randint(80, W - 80); y = random.randint(600, 960); h = random.randint(60, 340)
        d.rectangle([x, y, x + random.randint(30, 70), 980], fill=(10, 24, 60))
    for _ in range(120):
        x = random.randint(80, W - 80); y = random.randint(620, 960)
        if math.sin(t * 2 + x) > -0.6: d.rectangle([x, y, x + 5, y + 7], fill=(252, 191, 73) if x % 4 else (120, 170, 230))
    return im

def sc_meeting(im, t, lt, p):
    im = table_scene_bg(im, t); state = p.get("state", "ring")
    P = layer()
    m = mouth_at(p, lt) if p.get("speaker") == "client" else 0
    # host (daniel) right, two clients left, all chest-up behind table
    person(P, 760, 930, 0.92, "daniel", mouth=0, blink=blink_at(t, 2), look=(-1 if state == "ring" and lt > 0.8 else 0) * 0 + (1 if lt > 0.9 else 0))
    person(P, 300, 960, 0.85, "c1", mouth=0.3 * abs(math.sin(t * 9)) if state == "ring" and lt < 0.9 else 0, blink=blink_at(t, 3), look=1)
    im.paste(P, (0, 0), P); d = ImageDraw.Draw(im)
    # table
    d.polygon([(0, 1180), (W, 1180), (W, 1560), (0, 1560)], fill=(20, 40, 80))
    d.line([(0, 1180), (W, 1180)], fill=(90, 140, 210), width=4)
    # papers + laptop
    d.polygon([(150, 1260), (420, 1240), (450, 1340), (170, 1365)], fill=(235, 238, 245))
    d.rounded_rectangle([520, 1230, 640, 1290], 6, fill=(200, 205, 215))
    # phone on table
    shake = (6 * math.sin(lt * 60)) if state == "ring" else 0
    px, py = 700 + shake, 1300
    L = layer(); g = ImageDraw.Draw(L)
    if state == "ring":
        r = 60 + (lt * 1.5 % 1) * 120; a = int(220 * (1 - (lt * 1.5 % 1)))
        g.ellipse([px + 70 - r, py + 30 - r * 0.5, px + 70 + r, py + 30 + r * 0.5], outline=GOLD + (a,), width=5)
    col = GOLD if state == "ring" else ORANGE
    g.rounded_rectangle([px, py, px + 180, py + 70], 14, fill=col + (255,))
    im = glow(im, L, 22, 1.0); d = ImageDraw.Draw(im)
    phone_icon(d, px + 20, py + 14, 42, NAVY)
    d.text((px + 78, py + 35), "Seller" if state == "ring" else "Missed", font=F("Bold", 24), fill=NAVY, anchor="lm")
    # call card popup
    k = back((lt - 0.4) / 0.3)
    if k > 0:
        cw = 600 * k; cy0 = 320
        d.rounded_rectangle([W // 2 - cw / 2, cy0, W // 2 + cw / 2, cy0 + 150], 30, fill=NAVY2, outline=col, width=4)
        if k > 0.8:
            ctext(d, cy0 + 52, p.get("title", "Incoming call · Seller"), F("Bold", 44), WHITE)
            ctext(d, cy0 + 106, p.get("sub", "9:04 PM · Cranford, NJ"), F("Regular", 32), col)
    return im

def sc_couch(im, t, lt, p):
    d = ImageDraw.Draw(im)
    # night window + lamp
    d.rounded_rectangle([80, 260, 560, 820], 18, fill=(6, 18, 50)); d.line([(320, 260), (320, 820)], fill=(30, 50, 90), width=6)
    for i in range(40): x = 100 + (i * 37) % 440; y = 300 + (i * 53) % 480; d.ellipse([x, y, x + 3, y + 3], fill=(200, 210, 240))
    L = layer(); g = ImageDraw.Draw(L); g.ellipse([760, 380, 1000, 560], fill=(252, 191, 73, 200)); im = glow(im, L, 60, 1.0); d = ImageDraw.Draw(im)
    d.polygon([(800, 420), (960, 420), (920, 330), (840, 330)], fill=(240, 220, 170)); d.rectangle([872, 420, 888, 900], fill=(90, 80, 70))
    P = layer(); m = mouth_at(p, lt) * 0
    person(P, 390, 980, 0.95, "c1", blink=blink_at(t, 4), look=1, outfit=(160, 70, 80))
    person(P, 690, 960, 0.98, "c2", blink=blink_at(t, 5), look=-1, outfit=(50, 90, 80))
    im.paste(P, (0, 0), P); d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 1230, W - 40, 1580], 60, fill=(70, 60, 95)); d.rounded_rectangle([40, 1150, W - 40, 1290], 50, fill=(85, 72, 112))
    # phone glow in hands
    L = layer(); g = ImageDraw.Draw(L); g.rounded_rectangle([480, 1180, 580, 1360], 16, fill=(180, 220, 255, 255)); im = glow(im, L, 40, 1.4)
    d = ImageDraw.Draw(im); d.rounded_rectangle([488, 1190, 572, 1350], 12, fill=(235, 245, 255))
    d.rectangle([500, 1210, 560, 1250], fill=(150, 180, 220)); d.rectangle([500, 1262, 560, 1270], fill=(180, 190, 205))
    if p.get("clock"):
        k = back((lt - 0.2) / 0.3)
        if k > 0:
            d.rounded_rectangle([W // 2 - 220 * k, 880 - 520, W // 2 + 220 * k, 880 - 410], 50, fill=NAVY2, outline=GOLD, width=4)
            if k > 0.8: ctext(d, 415, p["clock"], F("Black", 64), GOLD)
    return im

def sc_contact(im, t, lt, p):
    # mid-roll contact card: phone + url slide in
    L = layer(); g = ImageDraw.Draw(L)
    a = ease(lt / 0.3); b = ease((lt - 0.35) / 0.3)
    head = p.get("head", "Call us today")
    g.text((W // 2, 560), head, font=F("Black", 90), fill=(255, 255, 255, int(255 * a)), anchor="mm")
    y = 820 + int(80 * (1 - a))
    g.rounded_rectangle([90, y - 110, 990, y + 110], 110, fill=GOLD + (int(255 * a),))
    g.text((W // 2 + 50, y), PHONE, font=F("Black", 100), fill=TEAL + (int(255 * a),), anchor="mm")
    im = glow(im, L, 34, 0.7); d = ImageDraw.Draw(im)
    if a > 0.5: phone_icon(d, 140, y - 40, 80, TEAL)
    if b > 0:
        ctext(d, 1060, URL, F("Bold", 80), fade(WHITE, b))
        ctext(d, 1160, p.get("sub", "Book your strategy call"), F("Medium", 46), fade(GOLD, b))
    return im

E.SCENES.update({k: E.sc_timer_wrap(v) for k, v in dict(presenter=sc_presenter, meeting=sc_meeting, couch=sc_couch, contact=sc_contact).items()})

def render(name, beats, outdir="/tmp/ailf/out3"):
    work = f"/tmp/ailf/work3/{name}"; shutil.rmtree(work, ignore_errors=True); os.makedirs(work + "/f"); os.makedirs(outdir, exist_ok=True)
    clips = []; durs = []
    for i, b in enumerate(beats):
        if b.get("say"):
            a, sr = tts(b["say"], b["spk"], None, b.get("speed", 1.04)); clips.append((a, sr)); dd = len(a) / sr
        else:
            clips.append(None); dd = 0
        durs.append(max(b.get("min", 0), dd + b.get("pad", 0.35)))
        b.setdefault("p", {})
        if clips[-1] is not None: b["p"]["_env"] = envelope(a, sr, int(durs[-1] * FPS) + 5)
    starts = np.cumsum([0] + durs[:-1]); total = sum(durs); N = int(total * FPS)
    for fi in range(N):
        t = fi / FPS; bi = int(np.searchsorted(starts, t, side="right") - 1); lt = t - starts[bi]; b = beats[bi]
        im = E.SCENES[b["scene"]](base(t), t, lt, b["p"])
        if bi and lt < 0.07: im = Image.blend(im, Image.new("RGB", (W, H), (40, 50, 90)), 0.25 * (1 - lt / 0.07))
        chrome(im, b.get("cap"), lt)
        if fi > N - FPS * 0.35: im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), (fi - (N - FPS * 0.35)) / (FPS * 0.35))
        im.save(f"{work}/f/{fi:05d}.jpg", quality=90)
    SR = 24000; mix = np.zeros(int((total + 0.5) * SR))
    for i, c in enumerate(clips):
        if c is None: continue
        a, sr = c
        if sr != SR: a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a)
        st = int((starts[i] + 0.1) * SR); mix[st:st + len(a)] += a[:len(mix) - st] * 0.9
    # music bed: soft chords + gentle kick on 2 & 4 feel, ducked under voice
    ta = np.arange(len(mix)) / SR; bpm = 96; beat = 60 / bpm
    chords = [(55, 82.4, 110, 138.6), (49, 73.4, 98, 123.5), (43.7, 65.4, 87.3, 110), (49, 73.4, 98, 123.5)]
    bed = np.zeros_like(mix)
    for ci in range(int(total / (beat * 4)) + 1):
        s0 = int(ci * beat * 4 * SR); s1 = min(len(mix), int((ci + 1) * beat * 4 * SR)); tt = np.arange(s1 - s0) / SR
        for f in chords[ci % 4]: bed[s0:s1] += np.sin(2 * np.pi * f * tt) * 0.018 * np.minimum(1, tt * 4)
    kick_t = np.arange(int(0.2 * SR)) / SR; kick = np.sin(2 * np.pi * (50 + 70 * np.exp(-kick_t * 30)) * kick_t) * np.exp(-kick_t * 16) * 0.22
    for k in range(int(total / beat)):
        st = int(k * beat * SR); mix_seg = bed[st:st + len(kick)]; bed[st:st + len(kick)] += kick[:len(mix_seg)]
    venv = np.convolve(np.abs(mix), np.ones(int(0.2 * SR)) / int(0.2 * SR), "same"); duck = 1 - np.clip(venv * 6, 0, 0.6)
    bed *= duck * np.minimum(1, ta) * np.clip((total + 0.3 - ta) / 0.8, 0, 1)
    mix += bed; mix /= max(1, np.abs(mix).max() / 0.95)
    with wave.open(f"{work}/a.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    out = f"{outdir}/{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{work}/f/%05d.jpg", "-i", f"{work}/a.wav",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    return out, total

# ---------------- drone / inventory / checks ----------------
_HOOD = None
def hood():
    global _HOOD
    if _HOOD is not None: return _HOOD
    S = 2600; im = Image.new("RGB", (S, S), (16, 40, 36)); d = ImageDraw.Draw(im); rnd = random.Random(21)
    road = (38, 46, 62); bs = 300
    for i in range(0, S, bs):
        d.rectangle([i - 26, 0, i + 26, S], fill=road); d.rectangle([0, i - 26, S, i + 26], fill=road)
        for j in range(0, S, 40): d.rectangle([i - 2, j, i + 2, j + 18], fill=(120, 120, 90)); d.rectangle([j, i - 2, j + 18, i + 2], fill=(120, 120, 90))
    houses = []
    roofs = [(120, 70, 60), (70, 76, 90), (150, 120, 90), (60, 60, 70), (110, 90, 80), (140, 140, 150)]
    for bx in range(0, S, bs):
        for by in range(0, S, bs):
            for (ox, oy) in [(40, 40), (160, 40), (40, 160), (160, 160)]:
                x, y = bx + ox, by + oy
                d.rectangle([x, y, x + 100, y + 100], fill=(30, 66, 52))
                w_, h_ = rnd.randint(54, 72), rnd.randint(44, 60); hx, hy = x + rnd.randint(8, 100 - w_ - 6), y + rnd.randint(8, 100 - h_ - 6)
                rc = roofs[rnd.randrange(len(roofs))]
                d.rectangle([hx + 6, hy + 6, hx + w_ + 6, hy + h_ + 6], fill=(10, 24, 22))
                d.rectangle([hx, hy, hx + w_, hy + h_], fill=rc)
                d.line([(hx, hy + h_ // 2), (hx + w_, hy + h_ // 2)], fill=tuple(int(c * 0.7) for c in rc), width=3)
                d.rectangle([hx, hy, hx + w_ // 2, hy + h_], fill=tuple(int(c * 0.88) for c in rc))
                if rnd.random() < 0.35: d.rounded_rectangle([x + 70, y + 64, x + 96, y + 94], 6, fill=(60, 140, 200))
                for _ in range(rnd.randint(1, 3)):
                    tx, ty = x + rnd.randint(0, 95), y + rnd.randint(0, 95); r = rnd.randint(9, 16)
                    d.ellipse([tx - r + 4, ty - r + 4, tx + r + 4, ty + r + 4], fill=(10, 28, 24)); d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(40, 96, 60))
                houses.append((hx + w_ // 2, hy + h_ // 2))
    _HOOD = (im, houses); return _HOOD

def sc_drone(im, t, lt, p):
    src, houses = hood(); S = src.size[0]
    dur = p.get("dur", 4.0); k = min(1, lt / dur)
    zoom = 1.35 - 0.35 * k if p.get("push", True) else 1.0 + 0.25 * k
    ang = p.get("rot", 8) * k
    cx = S / 2 + p.get("dx", 220) * k; cy = S / 2 + p.get("dy", -160) * k
    vw, vh = W / zoom, H / zoom; R = int(math.hypot(vw, vh) / 2) + 4
    crop = src.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R))).rotate(ang, resample=Image.BICUBIC)
    c2 = crop.crop((int(R - vw / 2), int(R - vh / 2), int(R + vw / 2), int(R + vh / 2))).resize((W, H), Image.BILINEAR)
    # golden-hour tint + vignette toward brand navy
    tint = Image.new("RGB", (W, H), (40, 30, 10)); c2 = Image.blend(c2, tint, 0.12)
    vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse([-300, -200, W + 300, H + 200], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220)); im = Image.composite(c2, Image.new("RGB", (W, H), NAVY), vig)
    d = ImageDraw.Draw(im)
    # pins on chosen houses (screen-space positions)
    tags = p.get("tags", [])
    pts = [(310, 720), (760, 900), (420, 1150), (720, 560), (560, 1300)]
    L = layer(); g = ImageDraw.Draw(L)
    for i, s in enumerate(tags):
        kk = back((lt - 0.5 - i * 0.45) / 0.3)
        if kk <= 0: continue
        x, y = pts[i % len(pts)]; r = 70 + 10 * math.sin(lt * 4 + i)
        g.ellipse([x - r, y - r, x + r, y + r], outline=GOLD + (230,), width=5)
        g.ellipse([x - 12, y - 12, x + 12, y + 12], fill=GOLD + (255,))
    im = glow(im, L, 14, 1.1); d = ImageDraw.Draw(im)
    for i, s in enumerate(tags):
        kk = back((lt - 0.5 - i * 0.45) / 0.3)
        if kk <= 0: continue
        x, y = pts[i % len(pts)]; tw = d.textlength(s, font=F("Bold", 34)) + 44
        col = [GOLD, ORANGE, SKY, GREEN][i % 4]; tc = TEAL if col in (GOLD,) else WHITE
        d.rounded_rectangle([x - tw / 2, y - 140, x + tw / 2, y - 84], 28, fill=col)
        if kk > 0.6: ctext(d, y - 112, s, F("Bold", 34), tc, x)
        d.line([(x, y - 84), (x, y - 14)], fill=col, width=4)
    # drone HUD
    hud = (255, 255, 255)
    for (x, y, sx, sy) in [(60, 230, 1, 1), (W - 60, 230, -1, 1), (60, H - 360, 1, -1), (W - 60, H - 360, -1, -1)]:
        d.line([(x, y), (x + 70 * sx, y)], fill=hud, width=4); d.line([(x, y), (x, y + 70 * sy)], fill=hud, width=4)
    if int(t * 2) % 2 == 0: d.ellipse([W - 220, 192, W - 196, 216], fill=(230, 50, 50))
    d.text((W - 186, 204), "REC", font=F("Bold", 30), fill=WHITE, anchor="lm")
    d.text((90, H - 400), f"ALT {int(380 - 120 * k)} FT", font=F("Medium", 28), fill=WHITE)
    d.text((W - 90, H - 400), p.get("place", "UNION COUNTY, NJ"), font=F("Medium", 28), fill=WHITE, anchor="ra")
    if p.get("title"):
        f = fit(d, p["title"], W - 160, 74, "Black"); tw = d.textlength(p["title"], font=f)
        d.rounded_rectangle([W // 2 - tw / 2 - 36, 280, W // 2 + tw / 2 + 36, 390], 28, fill=NAVY2)
        ctext(d, 335, p["title"], f, WHITE)
    return im

def house_thumb(d, x, y, w, h, col):
    d.rounded_rectangle([x, y, x + w, y + h], 14, fill=col)
    d.polygon([(x + w * 0.2, y + h * 0.55), (x + w * 0.5, y + h * 0.22), (x + w * 0.8, y + h * 0.55)], fill=(250, 245, 235))
    d.rectangle([x + w * 0.27, y + h * 0.55, x + w * 0.73, y + h * 0.85], fill=(250, 245, 235))
    d.rectangle([x + w * 0.45, y + h * 0.65, x + w * 0.55, y + h * 0.85], fill=col)

def sc_inventory(im, t, lt, p):
    d = ImageDraw.Draw(im); items = p.get("items")
    if not items:
        items = [("12 Elm St", "Under contract"), ("48 Oak Ave", "New seller"), ("7 Birch Ln", "Appointment"), ("230 Maple Dr", "Assigned"),
                 ("15 Cedar Ct", "New seller"), ("91 Park Pl", "Under contract"), ("4 Hill Rd", "Appointment"), ("66 River St", "New seller")]
    chip = {"Under contract": SKY, "New seller": ORANGE, "Appointment": GOLD, "Assigned": GREEN, "Listing": GOLD, "Sold": GREEN, "Showing": SKY}
    shown = int(min(len(items), lt / p.get("step", 0.32)) + 0.999)
    ctext(d, 300, p.get("title", "Your deal pipeline"), F("Black", 70), WHITE)
    cnt = shown
    d.rounded_rectangle([W // 2 - 190, 360, W // 2 + 190, 440], 40, fill=NAVY2, outline=GOLD, width=3)
    ctext(d, 400, f"{cnt} active {'deals' if p.get('deals', True) else 'listings'}", F("Bold", 40), GOLD)
    for i in range(shown):
        k = back((lt - i * p.get("step", 0.32)) / 0.25); col, row = i % 2, i // 2
        x = 90 + col * 460; y = 480 + row * 270 + int(40 * (1 - min(1, k)))
        if y > H - 560: continue
        d.rounded_rectangle([x, y, x + 440, y + 240], 26, fill=(8, 22, 54), outline=(40, 60, 100), width=2)
        house_thumb(d, x + 20, y + 20, 150, 200, [(40, 80, 140), (120, 60, 50), (60, 100, 80), (90, 70, 120)][i % 4])
        a, s = items[i]
        d.text((x + 190, y + 60), a, font=F("Bold", 34), fill=WHITE)
        c = chip.get(s, SKY); tw = d.textlength(s, font=F("Bold", 26)) + 30
        d.rounded_rectangle([x + 190, y + 130, x + 190 + tw, y + 176], 23, fill=c)
        d.text((x + 205, y + 153), s, font=F("Bold", 26), fill=TEAL if c == GOLD else WHITE, anchor="lm")
    if p.get("note", True): ctext(d, H - 360, "Example pipeline · for illustration", F("Regular", 26), GRAY)
    return im

def sc_checks(im, t, lt, p):
    memos = p.get("memos", ["Assignment fee · 12 Elm St", "Commission · 48 Oak Ave", "Assignment fee · 230 Maple Dr", "Commission · 91 Park Pl"])
    d = ImageDraw.Draw(im)
    if p.get("title"): ctext(d, 330, p["title"], F("Black", 76), WHITE)
    for i, memo in enumerate(memos):
        k = ease((lt - 0.2 - i * p.get("step", 0.55)) / 0.35)
        if k <= 0: continue
        cw, ch = 860, 380; ck = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); g = ImageDraw.Draw(ck)
        g.rounded_rectangle([0, 0, cw - 1, ch - 1], 22, fill=(246, 240, 222, 255), outline=(200, 185, 150, 255), width=3)
        for yy in range(0, ch, 14): g.line([(0, yy), (cw, yy)], fill=(238, 230, 208, 255), width=1)
        g.rectangle([0, 0, cw, 70], fill=(18, 52, 90, 255)); g.text((28, 35), p.get("payer", "TITLE & ESCROW CO."), font=F("Bold", 30), fill=(255, 255, 255, 255), anchor="lm")
        g.text((cw - 28, 35), f"No. {1040 + i}", font=F("Medium", 26), fill=(252, 191, 73, 255), anchor="rm")
        g.text((30, 110), "PAY TO THE", font=F("Medium", 22), fill=(90, 90, 90, 255)); g.text((30, 136), "ORDER OF", font=F("Medium", 22), fill=(90, 90, 90, 255))
        g.text((170, 128), p.get("payee", "YOU"), font=F("Black", 46), fill=(20, 30, 60, 255), anchor="lm")
        g.line([(160, 160), (600, 160)], fill=(120, 120, 120, 255), width=2)
        g.rounded_rectangle([620, 96, cw - 30, 160], 10, outline=(120, 120, 120, 255), width=2, fill=(255, 255, 255, 255))
        g.text(((620 + cw - 30) // 2, 128), "$ XX,XXX.00", font=F("Bold", 36), fill=(20, 30, 60, 255), anchor="mm")
        g.text((30, 236), "MEMO", font=F("Medium", 22), fill=(90, 90, 90, 255)); g.text((110, 238), memo, font=F("Medium", 32), fill=(20, 30, 60, 255), anchor="lm")
        g.line([(100, 262), (560, 262)], fill=(120, 120, 120, 255), width=2)
        g.line([(600, 300), (cw - 40, 300)], fill=(120, 120, 120, 255), width=2)
        for j in range(9): g.line([(620 + j * 22, 290 + 8 * math.sin(j)), (640 + j * 22, 280 - 6 * math.cos(j))], fill=(30, 40, 110, 255), width=3)
        g.text((30, 330), "⑆ 021000021 ⑈ 0001234567", font=F("Regular", 24), fill=(90, 90, 90, 255))
        ang = [-6, 4, -2, 7][i % 4] * (1 - 0.2 * k)
        ck = ck.rotate(ang, expand=True, resample=Image.BICUBIC)
        x = (W - ck.size[0]) // 2 + int((1 - k) * (900 if i % 2 else -900)); y = 520 + i * 95 - int(30 * k)
        sh = Image.new("RGBA", ck.size, (0, 0, 0, 120)); sh.putalpha(ck.split()[3].point(lambda v: v // 2))
        im.paste(sh, (x + 16, y + 20), sh); im.paste(ck, (x, y), ck)
    d = ImageDraw.Draw(im)
    ctext(d, H - 360, "Illustration only · results vary", F("Regular", 26), GRAY)
    return im

E.SCENES.update({k: E.sc_timer_wrap(v) for k, v in dict(drone=sc_drone, inventory=sc_inventory, checks=sc_checks).items()})
