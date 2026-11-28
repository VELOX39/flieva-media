"""Flieva daily carousel 2026-11-28: Netherlands highly skilled migrant permit (jobs that mention visa sponsorship)."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "d/2026-11-28"
os.makedirs(OUT, exist_ok=True)
NAVY = (11, 10, 30); VIOLET = (99, 102, 255); WHITE = (255, 255, 255); MUTED = (190, 192, 230)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
AV = "d/flieva-avatar.png"
SRC = "Source: ind.nl (Dutch immigration service)"

SLIDES = [
    ("WORK IN THE NETHERLANDS", "Dutch job offer? Read this before you pay anyone", "The highly skilled migrant permit: who applies, the 2026 salary rules and the fee. All from the official IND site.", None),
    ("RULE 1", "Only a recognised sponsor can apply", "Your employer must be recognised by the IND, the Dutch immigration service. The employer applies for your permit, not an agent.", SRC),
    ("CHECK IT", "Search the public register", "The IND publishes a public register of recognised sponsors. Look up the company name before you send any documents.", SRC),
    ("THE SALARY (2026)", "Gross per month, without holiday pay", "30 or older: €5,942\nUnder 30: €4,357\nReduced criterion (e.g. within 3 years of graduating): €3,122", "Amounts change every 1 January. Source: ind.nl"),
    ("THE FEE", "€423 in 2026", "The IND fee for a first highly skilled migrant application. It is paid to the IND as part of your employer's application.", SRC),
    ("SPEED", "Often decided within 2 weeks", "The IND tries to decide within 2 weeks for recognised sponsors. That is a target, not a promise.", SRC),
    ("RED FLAG", "'Pay us and we'll get you the permit'?", "Nobody can sell you this permit. Check the employer on the IND register and the job on the company's own careers page.", "Never send money to WhatsApp-only 'agents'"),
    ("FLIEVA", "Find jobs in the Netherlands that mention visa sponsorship", "Search jobs, get document checklists and practise your interview. Scam check included in Flieva plans.", "App Store · Google Play · flieva.com"),
]

def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        words, line = para.split(" "), ""
        for w in words:
            t = (line + " " + w) if line else w
            if d.textlength(t, font=font) <= width: line = t
            else: out.append(line); line = w
        out.append(line)
    return out

def render(W, H, i, s, n, pin=False):
    tag, head, body, foot = s
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    pad = 90; tw = W - 2 * pad
    d.ellipse((W - 420, -260, W + 260, 420), fill=(24, 22, 64))
    if os.path.exists(AV):
        a = Image.open(AV).convert("RGBA").resize((72, 72)); im.paste(a, (pad, pad), a)
    d.text((pad + 90, pad + 14), "Flieva", font=ImageFont.truetype(B, 38), fill=WHITE)
    if not pin: d.text((W - pad, pad + 18), f"{i+1}/{n}", font=ImageFont.truetype(B, 32), fill=MUTED, anchor="ra")
    hs = 88 if i == 0 else 76
    bsz = 42
    hf = ImageFont.truetype(B, hs); bf = ImageFont.truetype(R, bsz); tf = ImageFont.truetype(B, 34)
    hl = wrap(d, head, hf, tw); bl = wrap(d, body, bf, tw)
    lh = int(bsz * 1.42)
    total = 60 + 40 + len(hl) * int(hs * 1.18) + 80 + len(bl) * lh
    y = max(pad + 160, (H - total) // 2)
    pw = d.textlength(tag, font=tf) + 48
    d.rounded_rectangle((pad, y, pad + pw, y + 60), 30, fill=VIOLET)
    d.text((pad + 24, y + 30), tag, font=tf, fill=WHITE, anchor="lm"); y += 100
    for l in hl:
        d.text((pad, y), l, font=hf, fill=WHITE); y += int(hs * 1.18)
    y += 30
    d.rectangle((pad, y, pad + 120, y + 8), fill=VIOLET); y += 50
    for l in bl:
        d.text((pad, y), l, font=bf, fill=MUTED if i else WHITE); y += lh
    last = (i == n - 1)
    if foot:
        ff = ImageFont.truetype(B if last else R, 40 if last else 30)
        d.text((pad, H - pad - 40), foot, font=ff, fill=VIOLET if last else MUTED)
    if i == 0 and not pin:
        d.text((W - pad, H - pad - 40), "Swipe  >>", font=ImageFont.truetype(B, 40), fill=VIOLET, anchor="ra")
    return im

n = len(SLIDES)
for i, s in enumerate(SLIDES):
    render(1080, 1350, i, s, n).save(f"{OUT}/ig_{i+1}.jpg", quality=92)
    render(1080, 1920, i, s, n).save(f"{OUT}/tt_{i+1}.jpg", quality=92)

pin = ("WORK IN THE NETHERLANDS", "Dutch highly skilled migrant permit, explained", "Only an IND-recognised sponsor can apply. 2026 salary: €5,942/month (30+), €4,357 (under 30), gross without holiday pay. IND fee €423. Never pay an agent.", "flieva.com")
render(1000, 1500, n - 1, pin, n, pin=True).save(f"{OUT}/pinterest_card.jpg", quality=92)
print("ok")
