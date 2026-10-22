"""Slideshow 2: "Wanna work abroad? Were you asked to pay $10,000 for a visa? It's a lie."
6 slides. Writes a 4:5 set (Instagram/Facebook/LinkedIn) and a 9:16 set (TikTok)."""
import numpy as np
from PIL import Image, ImageDraw
import s01_move_abroad as m
from socialkit import font, logo, rounded, check_icon, flag_icon, BLUE, NAVY, WHITE, YELLOW, RED

TOTAL = 6
m.footer = lambda *a, **k: None


def footer(img, n, dark=True):
    d = ImageDraw.Draw(img)
    col = (200, 205, 240) if dark else (110, 116, 140)
    f = font(34, 'Bold')
    d.text((70, m.SH - 90), 'flieva.com', font=f, fill=col)
    d.text((m.SW - 70 - d.textlength(f'{n}/{TOTAL}', font=f), m.SH - 90), f'{n}/{TOTAL}', font=f, fill=col)


def s1():
    img = m.bg((58, 84, 255), (24, 36, 150))
    logo(img, m.SW // 2, 250, 140)
    y = m.centered(img, 'Wanna work abroad?', 430, 120, highlight={'abroad'})
    m.centered(img, 'Read this before you pay ANYONE', y + 50, 60, weight='Bold', color=(220, 225, 255))
    ImageDraw.Draw(img).text((m.SW // 2 - 150, m.SH - 200), 'swipe  ->', font=font(56, 'Black'), fill=YELLOW)
    footer(img, 1)
    return img


def s2():
    img = m.bg((40, 10, 20), (12, 4, 8))
    y = m.centered(img, 'Were you asked to pay', 330, 84, color=(220, 225, 255), weight='Bold')
    y = m.centered(img, '$10,000', y + 20, 230, color=YELLOW)
    y = m.centered(img, 'to an agent for a "visa" or a "job + visa package"?', y + 30, 76)
    footer(img, 2)
    return img


def s3():
    img = m.bg((14, 20, 64), (5, 8, 28))
    y = m.centered(img, "IT'S A LIE.", 240, 170, color=YELLOW)
    body = ('Visa fees are set by the government and published on its official website. '
            'You pay them to the government or its official visa centre.')
    y = m.centered(img, body, y + 60, 54, weight='Medium', color=(225, 228, 245), gap=1.32)
    rounded(img, (90, y + 40, m.SW - 90, y + 220), 36, WHITE)
    m.centered(img, "Never to an agent's personal account.", y + 75, 58, color=NAVY, max_w=820)
    footer(img, 3)
    return img


def s4():
    img = m.bg((247, 244, 238), (226, 230, 255))
    y = m.centered(img, "Real employers don't sell jobs.", 220, 96, color=WHITE, highlight={"don't"})
    points = [
        'International labour standards say workers should not pay recruitment fees.',
        "In the UK, a licensed sponsor must not make you pay its sponsorship costs.",
        'A genuine offer comes from a real company you can look up yourself.',
    ]
    y += 50
    for p in points:
        check_icon(img, 135, y + 34, 32)
        d = ImageDraw.Draw(img)
        yy = y
        for line in m.sk.wrap(d, p, font(46, 'SemiBold'), 760):
            d.text((195, yy), line, font=font(46, 'SemiBold'), fill=WHITE)
            yy += 60
        y = yy + 45
    footer(img, 4)
    return img


def s5():
    img = m.bg((40, 10, 20), (12, 4, 8))
    y = m.centered(img, 'Red flags', 200, 120, color=YELLOW)
    flags = ['"Guaranteed" visa or job', 'Pay today, it\'s urgent', 'Personal account, crypto or gift cards',
             'One "package" fee for job + visa + flight', 'No official government link anywhere']
    y += 40
    for f_ in flags:
        rounded(img, (80, y, m.SW - 80, y + 120), 30, WHITE)
        flag_icon(img, 130, y + 28, 64)
        ImageDraw.Draw(img).text((210, y + 36), f_, font=font(42, 'Bold'), fill=NAVY)
        y += 140
    footer(img, 5)
    return img


def s6():
    img = m.bg((14, 20, 64), (5, 8, 28))
    logo(img, m.SW // 2, 200, 140)
    y = m.centered(img, 'Check before you pay. Free on Flieva.', 320, 80, highlight={'flieva.'})
    items = ['See the official fee and link for your route', 'Check if a UK or Dutch employer is on the official sponsor register',
             'Paste any job offer into the scam check', 'Find jobs that say they sponsor visas']
    y += 40
    for it in items:
        d = ImageDraw.Draw(img)
        lines = m.sk.wrap(d, it, font(40, 'Bold'), 760)
        h = 50 * len(lines) + 60
        rounded(img, (80, y, m.SW - 80, y + h), 30, WHITE)
        check_icon(img, 150, y + h // 2, 34)
        yy = y + 32
        for line in lines:
            d.text((210, yy), line, font=font(40, 'Bold'), fill=NAVY)
            yy += 50
        y += h + 20
    m.centered(img, 'flieva.com', y + 20, 80, color=YELLOW)
    footer(img, 6)
    return img


SLIDES = [(s1, True), (s2, True), (s3, True), (s4, True), (s5, True), (s6, True)]


def to_tall(img):
    a = np.array(img.convert('RGB'))
    return Image.fromarray(np.vstack([np.repeat(a[:1], 285, axis=0), a, np.repeat(a[-1:], 285, axis=0)]))


if __name__ == '__main__':
    sheet = Image.new('RGB', (6 * 190, 340 + 250), 'white')
    for i, (fn, _) in enumerate(SLIDES, 1):
        img = fn().convert('RGB')
        img.save(f'out/s02_{i}.jpg', quality=92)
        tall = to_tall(img)
        tall.save(f'out/s02tt_{i}.jpg', quality=92)
        sheet.paste(tall.resize((180, 320)), ((i - 1) * 190, 0))
        sheet.paste(img.resize((180, 225)), ((i - 1) * 190, 345))
    sheet.save('out/s02_sheet.png')
