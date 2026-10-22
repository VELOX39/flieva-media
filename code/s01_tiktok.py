"""Slideshow 1, TikTok photo-mode version: 6 slides, 1080x1920, content centred (clear of TikTok's UI)."""
import numpy as np
from PIL import Image, ImageDraw
import s01_move_abroad as m
from socialkit import font

TOTAL = 6


def footer6(img, n, dark):
    d = ImageDraw.Draw(img)
    col = (200, 205, 240) if dark else (110, 116, 140)
    d.text((70, m.SH - 90), 'flieva.com', font=font(34, 'Bold'), fill=col)
    txt = f'{n}/{TOTAL}'
    d.text((m.SW - 70 - d.textlength(txt, font=font(34, 'Bold')), m.SH - 90), txt, font=font(34, 'Bold'), fill=col)


m.footer = lambda img, n, total, dark=True: None  # page numbers added below with the right total


def agent_slide():
    img = m.bg((40, 10, 20), (10, 4, 8))
    y = m.centered(img, 'And please...', 300, 70, color=(220, 225, 255), weight='Bold')
    y = m.centered(img, "Don't pay any agent who \"guarantees\" your visa", y + 30, 100, highlight={'guarantees"', 'visa'})
    m.centered(img, 'Only the government decides. Check the official website first.', y + 60, 54, color=(220, 225, 255), weight='Medium', gap=1.3)
    return img


def to_tall(img):
    """Pad a 1080x1350 slide to 1080x1920 by continuing its top and bottom edge colours."""
    a = np.array(img.convert('RGB'))
    top = np.repeat(a[:1], 285, axis=0)
    bot = np.repeat(a[-1:], 285, axis=0)
    return Image.fromarray(np.vstack([top, a, bot]))


slides = [(m.slide1(), True)] + [(m.step_slide(i), True) for i in range(3)] + [(agent_slide(), True), (m.slide5(), True)]
sheet = Image.new('RGB', (6 * 190, 340), 'white')
for i, (s, dark) in enumerate(slides, 1):
    footer6(s, i, dark)
    tall = to_tall(s)
    tall.save(f'out/s01tt_{i}.jpg', quality=92)
    sheet.paste(tall.resize((180, 320)), ((i - 1) * 190, 0))
sheet.save('out/s01tt_sheet.png')
