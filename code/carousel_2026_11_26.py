"""Flieva daily carousel 2026-11-26: Erasmus Mundus Joint Masters (scholarships / funded study)."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "d/2026-11-26"
os.makedirs(OUT, exist_ok=True)
NAVY = (11, 10, 30); VIOLET = (99, 102, 255); WHITE = (255, 255, 255); MUTED = (190, 192, 230)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Medium.otf" if os.path.exists("/usr/share/fonts/opentype/inter/Inter-Medium.otf") else B
AV = "d/flieva-avatar.png"
SRC = "Source: erasmus-plus.ec.europa.eu"

SLIDES = [
    ("STUDY IN EUROPE", "A funded master's in Europe. No agent needed.", "Erasmus Mundus scholarship applications mostly run October to January. That window is open now.", None),
    ("WHAT IT IS", "Erasmus Mundus Joint Masters", "Master's programmes run together by universities in different countries, funded by the EU. You can study in more than one country.", SRC),
    ("WHO CAN APPLY", "Students from all over the world", "You need a bachelor's degree, or be in your final year and graduate before the master's starts. An equivalent level of learning can also count.", SRC),
    ("WHAT IT PAYS", "Scholarships cover your participation costs", "They also contribute to travel, visa and a living allowance. Full scholarships go to the best applicants.", SRC),
    ("HOW TO APPLY", "Apply directly to the programme", "Find your course in the official Erasmus Mundus catalogue (eacea.ec.europa.eu), then apply on that programme's own website.", SRC),
    ("DEADLINES", "Most close between October and January", "That is for courses starting next academic year. Each programme sets its own date and documents, so check its page today.", SRC),
    ("RED FLAG", "Paying someone to 'secure' your scholarship?", "Students apply directly to the university running the programme. Nobody can sell you a place. Check every offer on the official site.", "Never send money to WhatsApp-only 'agents'"),
    ("FLIEVA", "Plan your study abroad in one app", "Document checklists, language-test practice and visa-interview practice. Scam check included in Flieva plans.", "App Store · Google Play · flieva.com"),
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

pin = ("STUDY IN EUROPE", "Funded master's in Europe? Apply direct, no agent.", "Erasmus Mundus Joint Masters: open to students worldwide, most deadlines October to January. Find your course in the official catalogue and apply on the programme's site.", "flieva.com")
render(1000, 1500, n - 1, pin, n, pin=True).save(f"{OUT}/pinterest_card.jpg", quality=92)
print("ok")
