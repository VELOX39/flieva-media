"""Flieva daily carousel 2026-11-27: Ireland Critical Skills Employment Permit (jobs that mention visa sponsorship)."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "d/2026-11-27"
os.makedirs(OUT, exist_ok=True)
NAVY = (11, 10, 30); VIOLET = (99, 102, 255); WHITE = (255, 255, 255); MUTED = (190, 192, 230)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
AV = "d/flieva-avatar.png"
SRC = "Source: enterprise.gov.ie"

SLIDES = [
    ("WORK IN IRELAND", "Ireland's Critical Skills permit: read this before you pay anyone", "What it needs, what it costs, and who actually applies. All from the official Irish government page.", None),
    ("WHAT IT IS", "Critical Skills Employment Permit", "Ireland's work permit for in-demand jobs. You need a job offer of at least 2 years from an Irish employer.", SRC),
    ("THE SALARY", "€40,904 a year or more", "For jobs on the Critical Skills Occupations List (with a relevant degree).\nOther eligible jobs: over €68,911.\nBasic salary counts. Bonuses don't.", SRC),
    ("WHO APPLIES", "You or your employer", "Applications go in online on Employment Permits Online (EPOS), at least 12 weeks before your start date.", SRC),
    ("THE FEE", "€1,000, paid in the official system", "If the application is refused, 90% is refunded. Pay only through the government system, never to a 'visa agent'.", SRC),
    ("FAMILY & LATER", "Family can join you", "Immediate family apply through Irish Immigration Service Delivery. When the permit ends, holders can apply to the Department of Justice for Stamp 4.", SRC),
    ("RED FLAG", "'Pay us for the permit and the job'?", "Real employers apply on EPOS or support your own application. Check the job on the company's own careers page first.", "Never send money to WhatsApp-only 'agents'"),
    ("FLIEVA", "Find jobs in Ireland that mention visa sponsorship", "Search jobs, get document checklists and practise your interview. Scam check included in Flieva plans.", "App Store · Google Play · flieva.com"),
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

pin = ("WORK IN IRELAND", "Ireland's Critical Skills permit, explained", "2-year job offer, €40,904+ for listed jobs, €1,000 fee paid in the official system. You or your employer apply on EPOS. Never pay an agent.", "flieva.com")
render(1000, 1500, n - 1, pin, n, pin=True).save(f"{OUT}/pinterest_card.jpg", quality=92)
print("ok")
