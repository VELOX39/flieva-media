"""Flieva daily carousel 2026-11-25: Germany Opportunity Card (Chancenkarte)."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "d/2026-11-25"
os.makedirs(OUT, exist_ok=True)
NAVY = (11, 10, 30); VIOLET = (99, 102, 255); WHITE = (255, 255, 255); MUTED = (190, 192, 230)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Medium.otf" if os.path.exists("/usr/share/fonts/opentype/inter/Inter-Medium.otf") else B
AV = "d/flieva-avatar.png"

SLIDES = [
    ("GERMANY", "Job-hunt in Germany without a job offer?", "The Opportunity Card (Chancenkarte) is real. Here is what it actually asks for.", None),
    ("WHAT IT IS", "Up to 1 year in Germany to look for work", "A residence permit for job search. Find qualified work and it can be extended as a Follow-up Opportunity Card.", "Source: arbeitsagentur.de"),
    ("ROUTE 1", "Qualification fully recognised in Germany?", "Then you qualify directly, no points needed. That covers German or recognised foreign degrees and vocational training.", "Source: arbeitsagentur.de, diplo.de"),
    ("ROUTE 2", "Otherwise: score at least 6 points", "Minimum first: a degree or 2+ years of vocational training recognised in your country, plus German A1 or English B2.", "Source: arbeitsagentur.de"),
    ("POINTS", "What earns points", "• Partial recognition in Germany: 4\n• German B2: 3  (B1: 2, A2: 1)\n• 5+ years' experience: 3  (2+ years: 2)\n• Under 35: 2  (under 40: 1)\n• 1 each: shortage occupation, English C1, 6+ months in Germany before, partner applying too", "Source: arbeitsagentur.de"),
    ("MONEY", "Show €1,091 a month (2026)", "That is €13,092 for 12 months: blocked account, bank statements, a Verpflichtungserklärung (formal letter of commitment) or a part-time job contract.", "Source: make-it-in-germany.com, diplo.de"),
    ("WHILE YOU SEARCH", "Work up to 20 hours a week", "Plus trial work of up to 2 weeks per employer. Apply yourself via the German mission and digital.diplo.de/visa. No agent needed.", "Check your German embassy's page: rules can change"),
    ("FLIEVA", "Find jobs in Germany that mention visa sponsorship", "Official checklists and language practice. Scam check included in Flieva plans.", "App Store · Google Play · flieva.com"),
]

def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        words, line = para.split(" "), ""
        for w in words:
            t = (line + " " + w) if line else w
            if d.textlength(t, font=font) <= width: line = t
            else: out.append(line); line = "   " + w if para.startswith("•") else w
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
    hs = 96 if i == 0 else 78
    bsz = 40 if body.count("\n") >= 3 else 44
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

pin = ("GERMANY", "Job-hunt in Germany without a job offer? Read this.", "Opportunity Card: up to 1 year to look for work. 6 points or a recognised qualification, German A1 or English B2, and €1,091 a month in funds (2026).", "flieva.com")
render(1000, 1500, n - 1, pin, n, pin=True).save(f"{OUT}/pinterest_card.jpg", quality=92)
print("ok")
