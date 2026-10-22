"""Slideshow 1: "Wanna move abroad?" (5 slides, 1080x1350)."""
from PIL import Image, ImageDraw
import socialkit as sk
from socialkit import font, logo, rounded, check_icon, BLUE, NAVY, CREAM, WHITE, YELLOW, RED, GREEN

SW, SH = 1080, 1350
OUT = '/home/claude/flieva-social/out/s01_'


BRAND_TOP, BRAND_BOTTOM = (58, 84, 255), (24, 36, 150)  # the only slide background (Flieva blue)


def bg(top=None, bottom=None):
    top, bottom = BRAND_TOP, BRAND_BOTTOM
    import numpy as np
    arr = np.zeros((SH, SW, 4), dtype=np.uint8)
    for i in range(3):
        arr[:, :, i] = np.linspace(top[i], bottom[i], SH)[:, None]
    arr[:, :, 3] = 255
    return Image.fromarray(arr, 'RGBA')


def centered(img, text, y, size, color=WHITE, weight='Black', max_w=920, gap=1.12, highlight=None):
    d = ImageDraw.Draw(img)
    f = font(size, weight)
    for line in sk.wrap(d, text, f, max_w):
        if highlight:
            words = line.split(' ')
            total = d.textlength(line, font=f)
            x = (SW - total) / 2
            for w in words:
                col = YELLOW if w.strip('?.,!').lower() in highlight else color
                d.text((x, y), w, font=f, fill=col)
                x += d.textlength(w + ' ', font=f)
        else:
            d.text(((SW - d.textlength(line, font=f)) / 2, y), line, font=f, fill=color)
        y += size * gap
    return y


def footer(img, n, total, dark=True):
    d = ImageDraw.Draw(img)
    col = (200, 205, 240) if dark else (110, 116, 140)
    d.text((70, SH - 90), 'flieva.com', font=font(34, 'Bold'), fill=col)
    txt = f'{n}/{total}'
    d.text((SW - 70 - d.textlength(txt, font=font(34, 'Bold')), SH - 90), txt, font=font(34, 'Bold'), fill=col)


STEPS = [
    ('1', 'A valid passport', 'Check it won\'t expire before or during your trip. Many countries want months of validity left.'),
    ('2', 'The right visa route', 'Work, study, visit or family: each has its own form, fee and rules. Pick the wrong one and you start again.'),
    ('3', 'The documents for THAT route', 'Offer letters, bank statements, test results... the list changes by country and route.'),
]


def slide1():
    img = bg((58, 84, 255), (24, 36, 150))
    logo(img, SW // 2, 260, 150)
    y = centered(img, 'Wanna move abroad?', 470, 120, highlight={'abroad'})
    centered(img, 'Here\'s what you actually need (and what most people miss)', y + 50, 52, weight='Bold', color=(220, 225, 255))
    d = ImageDraw.Draw(img)
    d.text((SW // 2 - 150, SH - 180), 'swipe  ->', font=font(56, 'Black'), fill=YELLOW)
    footer(img, 1, 5)
    return img


def step_slide(i):
    num, title, body = STEPS[i]
    img = bg((247, 244, 238), (226, 230, 255))
    d = ImageDraw.Draw(img)
    d.ellipse((SW // 2 - 110, 190, SW // 2 + 110, 410), fill=WHITE)
    f = font(150, 'Black')
    d.text((SW // 2 - d.textlength(num, font=f) / 2, 205), num, font=f, fill=BLUE)
    y = centered(img, title, 500, 92, color=WHITE)
    centered(img, body, y + 50, 50, color=(220, 225, 255), weight='Medium', gap=1.3)
    footer(img, i + 2, 5, dark=True)
    return img


def slide5():
    img = bg((14, 20, 64), (5, 8, 28))
    logo(img, SW // 2, 220, 150)
    y = centered(img, 'Flieva does the hard part', 360, 84, highlight={'flieva'})
    items = ['Pick your country + why you\'re going', 'Get the official government links and fees',
             'Your document checklist, ready to tick', 'A reminder of your next step every day']
    y += 40
    for it in items:
        rounded(img, (80, y, SW - 80, y + 115), 30, WHITE)
        check_icon(img, 150, y + 57, 34)
        ImageDraw.Draw(img).text((210, y + 35), it, font=font(40, 'Bold'), fill=NAVY)
        y += 135
    centered(img, 'Free at flieva.com', y + 20, 72, color=YELLOW)
    footer(img, 5, 5)
    return img


if __name__ == '__main__':
    slides = [slide1()] + [step_slide(i) for i in range(3)] + [slide5()]
    for i, s in enumerate(slides, 1):
        s.convert('RGB').save(f'{OUT}{i}.jpg', quality=92)
    sheet = Image.new('RGB', (5 * 280, 350), 'white')
    for i, s in enumerate(slides):
        sheet.paste(s.convert('RGB').resize((270, 338)), (i * 280, 0))
    sheet.save(OUT + 'sheet.png')
