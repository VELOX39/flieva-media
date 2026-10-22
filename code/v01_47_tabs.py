"""Video 1: "POV: You tried to japa without a plan" (about 52 s)."""
import random

from socialkit import *

random.seed(4)
OUT = '/home/claude/flieva-social/out/'
DARK_TOP, DARK_BOT = (12, 18, 58), (4, 6, 22)
bg_dark = gradient_bg((58, 84, 255), (24, 36, 150))
bg_blue = gradient_bg((58, 84, 255), (24, 36, 150))
bg_night = gradient_bg((40, 58, 200), (16, 24, 110))

TAB_TITLES = ['canada visa requirements', 'is japa still possible 2026', 'uk visa fee naira', 'proof of funds how much',
              'visa agent near me', 'germany job no ielts', 'how to apply study visa', 'is this agent legit??',
              'visa sponsorship jobs', 'which form do i need', 'embassy appointment', 'japa without money',
              'canada express entry points', 'uk care job sponsor', 'visa refused why', 'cheapest country to japa']


def caption_top(img, text, t, size=64, y=150, highlight=None):
    rounded(img, (60, y - 30, W - 60, y + size * 2.6), 40, (0, 0, 0), alpha=110)
    text_block(img, text, y, size=size, weight='Black', appear=t * 4, highlight=highlight)


def s1(t):  # hook
    img = bg_dark.copy()
    y = text_block(img, 'POV:', 560, size=90, weight='Bold', color=(220, 225, 255), appear=t * 5)
    y = text_block(img, 'You tried to JAPA', y + 20, size=124, appear=(t - 0.25) * 4, highlight={'japa'})
    text_block(img, 'without a plan', y + 10, size=124, appear=(t - 0.7) * 4, color=YELLOW)
    text_block(img, 'watch till the end...', 1500, size=48, weight='Medium', color=(220, 225, 255), appear=(t - 2.0) * 3)
    return img


def s2(t):  # tabs piling up
    img = bg_dark.copy()
    caption_top(img, 'Kevin opens ONE tab to "quickly check"...', t, highlight={'one'})
    n = min(len(TAB_TITLES), int(1 + (t ** 1.6) * 2.2))
    for i in range(n):
        y = 520 + i * 78
        x = 70 + (i % 3) * 14
        rounded(img, (x, y, W - 70 + (i % 2) * 10, y + 66), 18, WHITE)
        d = ImageDraw.Draw(img)
        d.ellipse((x + 22, y + 22, x + 44, y + 44), fill=BLUE)
        d.text((x + 64, y + 13), TAB_TITLES[i], font=font(36, 'Medium'), fill=NAVY)
    count = min(47, int(1 + t ** 2 * 1.05))
    rounded(img, (300, 1720, W - 300, 1840), 60, YELLOW)
    text_block(img, f'TAB {count}', 1736, size=72, color=NAVY, appear=1)
    return img


def site_card(img, y, title, body, color, appear, flag=False):
    if appear <= 0:
        return
    a = ease_back(appear)
    yy = y + (1 - a) * 120
    rounded(img, (80, yy, W - 80, yy + 300), 36, (255, 255, 255), alpha=int(245 * min(1, appear * 2)))
    d = ImageDraw.Draw(img)
    d.text((130, yy + 40), title, font=font(42, 'SemiBold'), fill=(90, 96, 120))
    d.text((130, yy + 110), body, font=font(66, 'Black'), fill=color)
    if flag:
        flag_icon(img, W - 210, yy + 70, 120, appear)


def s3(t):  # three websites disagree
    img = bg_dark.copy()
    caption_top(img, 'Every website says something different', t, highlight={'different'})
    site_card(img, 480, 'Website 1', 'Fee is $155', NAVY, (t - 0.3) * 3)
    site_card(img, 840, 'Website 2', '"It depends"', NAVY, (t - 2.6) * 3)
    site_card(img, 1200, 'Website 3', 'GUARANTEED VISA', RED, (t - 5.0) * 3, flag=True)
    if t > 5.6:
        text_block(img, 'just pay $2,000 today', 1540, size=58, weight='Black', color=YELLOW, appear=(t - 5.6) * 3)
    return img


def s4(t):  # 3 months later
    img = bg_night.copy()
    text_block(img, '3 months later...', 700, size=110, color=(220, 225, 255), appear=t * 2)
    text_block(img, 'Kevin still doesn\'t know which form he needs.', 980, size=70, weight='Bold', appear=(t - 1.6) * 2)
    return img


def s5(t):  # the link
    img = bg_blue.copy()
    y = text_block(img, 'Then his friend sent him', 700, size=84, appear=t * 4)
    text_block(img, 'ONE link.', y + 30, size=150, color=YELLOW, appear=(t - 0.6) * 4)
    return img


FEATURES = [('Official government link', 'straight from the source'),
            ('The official fee', 'and where it comes from'),
            ('A document checklist', 'tick it off as you go'),
            ('Your next step every day', 'on WhatsApp or email'),
            ('Scam check', 'before you pay ANYONE')]


def s6(t):  # Flieva features
    img = gradient_bg((58, 84, 255), (24, 36, 150))
    logo(img, W // 2, 300, 230, appear=t * 3)
    text_block(img, 'Flieva', 450, size=90, color=WHITE, appear=(t - 0.2) * 3)
    for i, (a, b) in enumerate(FEATURES):
        ap = (t - 1.0 - i * 2.4) * 3
        if ap <= 0:
            continue
        y = 640 + i * 230
        rounded(img, (80, y, W - 80, y + 190), 36, WHITE, alpha=int(255 * min(1, ap * 2)))
        check_icon(img, 175, y + 95, 48, appear=ap)
        d = ImageDraw.Draw(img)
        d.text((260, y + 40), a, font=font(52, 'Black'), fill=NAVY)
        d.text((260, y + 110), b, font=font(40, 'Medium'), fill=(90, 96, 120))
    return img


def s7(t):  # payoff
    img = bg_blue.copy()
    text_block(img, '47 tabs', 520, size=130, color=(200, 205, 255), appear=t * 4)
    if t > 0.6:
        d = ImageDraw.Draw(img)
        w = min(1, (t - 0.6) * 4)
        tw = d.textlength('47 tabs', font=font(130, 'Black'))
        x0 = (W - tw) / 2 - 20
        d.line([(x0, 600), (x0 + (tw + 40) * w, 600)], fill=RED, width=16)
    text_block(img, '1 plan.', 700, size=170, color=YELLOW, appear=(t - 1.0) * 4)
    text_block(img, 'Don\'t be Kevin.', 1000, size=92, appear=(t - 2.0) * 4)
    logo(img, W // 2, 1340, 200, appear=(t - 2.8) * 3)
    text_block(img, 'flieva.com', 1480, size=84, appear=(t - 3.0) * 3)
    text_block(img, 'link in bio', 1590, size=48, weight='Medium', color=(220, 225, 255), appear=(t - 3.3) * 3)
    return img


SCENES = [(3.6, s1), (8.6, s2), (8.2, s3), (5.2, s4), (2.6, s5), (14.0, s6), (6.8, s7)]
starts, acc = [], 0
for d, _ in SCENES:
    starts.append(acc); acc += d
TOTAL = acc

tl = Timeline(TOTAL)
tl.add(0, music('tension', starts[3]), 0.9)
tl.add(0.25, sfx('boom'))
tl.add(0.7, sfx('pop'))
# tab clicks speed up
s = starts[1]
for k in range(48):
    tt = ((k / 1.05) ** 0.5)
    if tt < 8.4:
        tl.add(s + tt, sfx('click'), 1.2)
tl.add(starts[2] + 0.3, sfx('pop')); tl.add(starts[2] + 2.6, sfx('pop'))
tl.add(starts[2] + 5.0, sfx('scratch'), 1.2); tl.add(starts[2] + 5.0, sfx('boom'), 0.7)
tl.add(starts[3] + 0.2, sfx('sad'), 1.1)
tl.add(starts[3], music('sadpad', 5.2), 0.8)
tl.add(starts[4], sfx('whoosh'), 1.0); tl.add(starts[4] + 0.6, sfx('ding'))
tl.add(starts[5], music('upbeat', TOTAL - starts[5], bpm=118), 0.85)
for i in range(len(FEATURES)):
    tl.add(starts[5] + 1.0 + i * 2.4, sfx('pop'))
tl.add(starts[6] + 0.6, sfx('scratch'), 0.6)
tl.add(starts[6] + 1.0, sfx('ding'))


def shake(tg):
    for hit, strength in ((0.25, 26), (starts[2] + 5.0, 30)):
        if 0 <= tg - hit < 0.35:
            return strength * (1 - (tg - hit) / 0.35)
    return 0


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    tl.write(OUT + 'v01.wav')
    render(SCENES, OUT + 'v01_47_tabs.mp4', OUT + 'v01.wav', shake=shake)
    print('duration', TOTAL)
