"""Small engine for Flieva's vertical social videos (1080x1920, 30 fps) and slideshow images.

Scenes draw onto a PIL image at a local time t (seconds). Sound effects and music are synthesized with
numpy (no samples, no licences needed) and mixed onto a timeline. Rendering pipes raw frames to ffmpeg.
"""
import math
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 44100
FONT_DIR = '/usr/share/fonts/opentype/inter/'
BLUE = (48, 73, 241)
NAVY = (10, 16, 54)
CREAM = (247, 244, 238)
WHITE = (255, 255, 255)
YELLOW = (255, 210, 63)
RED = (255, 77, 77)
GREEN = (43, 214, 123)
GREY = (150, 156, 180)

_fonts = {}


def font(size, weight='Black'):
    key = (size, weight)
    if key not in _fonts:
        name = {'Black': 'InterDisplay-Black.otf', 'Bold': 'InterDisplay-Bold.otf', 'Medium': 'Inter-Medium.otf',
                'Regular': 'Inter-Regular.otf', 'SemiBold': 'Inter-SemiBold.otf'}[weight]
        _fonts[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _fonts[key]


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = max(0.0, min(1.0, x))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split('\n'):
        words, cur = para.split(' '), ''
        for w_ in words:
            test = (cur + ' ' + w_).strip()
            if draw.textlength(test, font=fnt) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w_
        lines.append(cur)
    return lines


def text_block(img, text, y, size=96, weight='Black', color=WHITE, appear=1.0, max_w=940, stroke=0,
               stroke_color=(0, 0, 0), highlight=None, align='center', line_gap=1.12, x=None):
    """Draw wrapped text; `appear` 0..1 slides it up and fades it in. `highlight` = words drawn in yellow."""
    fnt = font(size, weight)
    lines = wrap(ImageDraw.Draw(img), text, fnt, max_w)
    if appear <= 0:
        return y + len(lines) * size * line_gap
    a = ease_back(appear)
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    yy = y + (1 - a) * 60
    for line in lines:
        lw = d.textlength(line, font=fnt)
        xx = (W - lw) / 2 if align == 'center' else (x if x is not None else 70)
        if highlight:
            # draw word by word so highlighted words get a different colour
            for word in line.split(' '):
                ww = d.textlength(word + ' ', font=fnt)
                col = YELLOW if word.strip('.,!?:"\'').lower() in highlight else color
                d.text((xx, yy), word, font=fnt, fill=col, stroke_width=stroke, stroke_fill=stroke_color)
                xx += ww
        else:
            d.text((xx, yy), line, font=fnt, fill=color, stroke_width=stroke, stroke_fill=stroke_color)
        yy += size * line_gap
    end = y + len(lines) * size * line_gap
    alpha = int(255 * min(1.0, appear * 2))
    if alpha < 255:
        layer.putalpha(layer.getchannel('A').point(lambda p: p * alpha // 255))
    img.alpha_composite(layer)
    return end


def rounded(img, box, radius, fill, outline=None, width=0, alpha=255):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=fill + (alpha,) if len(fill) == 3 else fill,
                        outline=outline, width=width)
    img.alpha_composite(layer)


def check_icon(img, cx, cy, r, color=GREEN, appear=1.0):
    if appear <= 0:
        return
    s = ease_back(appear)
    d = ImageDraw.Draw(img)
    rr = r * s
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=color)
    pts = [(cx - rr * 0.45, cy + rr * 0.02), (cx - rr * 0.1, cy + rr * 0.38), (cx + rr * 0.5, cy - rr * 0.35)]
    d.line(pts, fill=WHITE, width=max(3, int(rr * 0.22)), joint='curve')


def flag_icon(img, x, y, size, appear=1.0):
    if appear <= 0:
        return
    s = ease_back(appear)
    d = ImageDraw.Draw(img)
    h = size * s
    d.line([(x, y), (x, y + h)], fill=WHITE, width=max(3, int(size * 0.08)))
    d.polygon([(x, y), (x + h * 0.75, y + h * 0.18), (x, y + h * 0.4)], fill=RED)


def logo(img, cx, cy, size, appear=1.0):
    """The Flieva mark: blue rounded square with the cream F (drawn, so it is crisp at any size)."""
    if appear <= 0:
        return
    s = size * ease_back(appear)
    x0, y0 = cx - s / 2, cy - s / 2
    rounded(img, (x0, y0, x0 + s, y0 + s), int(s * 0.18), BLUE)
    d = ImageDraw.Draw(img)
    u = s / 1024
    # stem
    d.rounded_rectangle((x0 + 236 * u, y0 + 300 * u, x0 + 392 * u, y0 + 844 * u), radius=int(48 * u), fill=CREAM)
    # top bar with the wing
    d.rounded_rectangle((x0 + 236 * u, y0 + 260 * u, x0 + 700 * u, y0 + 392 * u), radius=int(60 * u), fill=CREAM)
    d.polygon([(x0 + 660 * u, y0 + 260 * u), (x0 + 820 * u, y0 + 185 * u), (x0 + 878 * u, y0 + 205 * u),
               (x0 + 790 * u, y0 + 340 * u), (x0 + 680 * u, y0 + 392 * u)], fill=CREAM)
    # middle bar
    d.rounded_rectangle((x0 + 236 * u, y0 + 483 * u, x0 + 700 * u, y0 + 611 * u), radius=int(40 * u), fill=CREAM)


def gradient_bg(top, bottom):
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    for i in range(3):
        arr[:, :, i] = np.linspace(top[i], bottom[i], H, dtype=np.float32)[:, None]
    arr[:, :, 3] = 255
    return Image.fromarray(arr, 'RGBA')


# ---------------------------------------------------------------- sound
def _env(n, attack=0.005, decay=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / max(decay, 1e-4))
    return e


def sfx(kind, dur=None):
    rng = np.random.default_rng(len(kind))
    if kind == 'boom':
        n = int(SR * 1.4); t = np.arange(n) / SR
        f = 40 + 90 * np.exp(-t * 6)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.5) + rng.normal(0, 1, n) * _env(n, 0.001, 0.05) * 0.4
        return y * 0.9
    if kind == 'click':
        n = int(SR * 0.02)
        return rng.normal(0, 1, n) * _env(n, 0.0005, 0.004) * 0.5
    if kind == 'pop':
        n = int(SR * 0.12); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (500 + 900 * t / 0.12) * t) * _env(n, 0.002, 0.04) * 0.45
    if kind == 'ding':
        n = int(SR * 1.2); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t)) * _env(n, 0.001, 0.35) * 0.35
    if kind == 'whoosh':
        n = int(SR * 0.7); t = np.arange(n) / SR
        noise = rng.normal(0, 1, n)
        kernel = np.ones(30) / 30
        y = np.convolve(noise, kernel, 'same') * np.sin(np.pi * t / 0.7) ** 2
        return y * 1.6
    if kind == 'scratch':
        n = int(SR * 0.45); t = np.arange(n) / SR
        f = 300 + 900 * np.abs(np.sin(2 * np.pi * 3 * t))
        saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
        return (saw * 0.5 + rng.normal(0, 0.3, n)) * _env(n, 0.002, 0.2) * 0.6
    if kind == 'buzzer':
        n = int(SR * 0.7); t = np.arange(n) / SR
        return np.sign(np.sin(2 * np.pi * 110 * t)) * 0.25 * _env(n, 0.005, 0.4)
    if kind == 'sad':  # descending "wah wah wah wahhh"
        out = []
        for f0, d in ((392, 0.45), (370, 0.45), (349, 0.45), (330, 1.4)):
            n = int(SR * d); t = np.arange(n) / SR
            vib = 1 + 0.02 * np.sin(2 * np.pi * 6 * t) * (t > 0.3)
            ph = 2 * np.pi * np.cumsum(f0 * vib) / SR
            y = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)) * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08)
            out.append(y * 0.22)
        return np.concatenate(out)
    raise ValueError(kind)


def music(kind, dur, bpm=120):
    n = int(SR * dur); t = np.arange(n) / SR
    beat = 60 / bpm
    y = np.zeros(n)
    rng = np.random.default_rng(7)
    if kind == 'tension':  # low drone + ticking clock
        y += 0.10 * np.sin(2 * np.pi * 55 * t) + 0.05 * np.sin(2 * np.pi * 82.4 * t + 0.5 * np.sin(2 * np.pi * 0.3 * t))
        for k in np.arange(0, dur, beat / 2):
            i = int(k * SR); m = min(n - i, int(0.03 * SR))
            y[i:i + m] += rng.normal(0, 1, m) * _env(m, 0.0005, 0.006) * 0.25
        return y
    if kind == 'sadpad':
        for f in (220, 261.6, 329.6):
            y += 0.05 * np.sin(2 * np.pi * f * t)
        return y * np.minimum(1, t / 1.0)
    if kind == 'upbeat':
        bass_notes = [55, 55, 65.4, 73.4]
        for b, k in enumerate(np.arange(0, dur, beat)):
            i = int(k * SR)
            m = min(n - i, int(0.35 * SR)); tt = np.arange(m) / SR
            y[i:i + m] += np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.55  # kick
            if b % 2 == 1:
                m2 = min(n - i, int(0.12 * SR))
                y[i:i + m2] += rng.normal(0, 1, m2) * _env(m2, 0.001, 0.04) * 0.25  # clap
            f = bass_notes[(b // 2) % 4]
            m3 = min(n - i, int(beat * SR)); t3 = np.arange(m3) / SR
            y[i:i + m3] += 0.12 * np.sign(np.sin(2 * np.pi * f * 2 * t3)) * np.exp(-t3 * 3)
            for h in (0.5,):
                j = int((k + beat * h) * SR); m4 = min(max(0, n - j), int(0.03 * SR))
                if m4:
                    y[j:j + m4] += rng.normal(0, 1, m4) * _env(m4, 0.0005, 0.01) * 0.18  # hat
        chords = [(220, 261.6, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7), (196, 246.9, 293.7)]
        bar = beat * 4
        for c, k in enumerate(np.arange(0, dur, bar)):
            i = int(k * SR); m = min(n - i, int(bar * SR)); tt = np.arange(m) / SR
            for f in chords[c % 4]:
                y[i:i + m] += 0.03 * np.sign(np.sin(2 * np.pi * f * 2 * tt)) * np.exp(-tt * 1.2)
        return y
    raise ValueError(kind)


class Timeline:
    def __init__(self, dur):
        self.audio = np.zeros(int(SR * dur) + SR)

    def add(self, at, samples, gain=1.0):
        i = int(at * SR)
        m = min(len(samples), len(self.audio) - i)
        if m > 0:
            self.audio[i:i + m] += samples[:m] * gain

    def write(self, path):
        a = self.audio / max(1.0, np.max(np.abs(self.audio)) / 0.95)
        pcm = (a * 32767).astype(np.int16)
        with wave.open(path, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(pcm.tobytes())


def render(scenes, out_path, audio_path, shake=None):
    """scenes: list of (duration, draw(img, t)). shake(t_global) -> pixels of screen shake."""
    total = sum(d for d, _ in scenes)
    proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', audio_path,
                             '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                             '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out_path],
                            stdin=subprocess.PIPE)
    start = 0.0
    for dur, draw in scenes:
        for f in range(int(round(dur * FPS))):
            t = f / FPS
            img = draw(t)
            if shake:
                s = shake(start + t)
                if s:
                    dx, dy = int(s * math.sin((start + t) * 91)), int(s * math.cos((start + t) * 73))
                    img = img.transform(img.size, Image.AFFINE, (1, 0, dx, 0, 1, dy))
            proc.stdin.write(img.convert('RGB').tobytes())
        start += dur
    proc.stdin.close()
    proc.wait()
    return total
