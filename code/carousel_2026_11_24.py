"""Flieva daily carousel 2026-11-24: UK sponsorship fees scam check."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "d/2026-11-24"
os.makedirs(OUT, exist_ok=True)
NAVY = (11, 10, 30); VIOLET = (99, 102, 255); WHITE = (255, 255, 255); MUTED = (190, 192, 230)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Medium.otf" if os.path.exists("/usr/share/fonts/opentype/inter/Inter-Medium.otf") else B
AV = "d/flieva-avatar.png"

SLIDES = [
    ("WARNING", "Asked to pay for your UK certificate of sponsorship?", "Read this before you send a single naira, cedi or rupee.", None),
    ("WHAT IT IS", "A CoS is a reference number from a licensed UK employer", "You need it to apply for a Skilled Worker visa. It comes from the employer that hires you.", None),
    ("WHO PAYS", "The employer pays the CoS fee. Not you.", "GOV.UK lists £525 per Worker certificate and says Skilled Worker sponsors must pay it themselves.", "Source: gov.uk/uk-visa-sponsorship-employers"),
    ("ALSO THE EMPLOYER", "The immigration skills charge is theirs too", "GOV.UK: a sponsor's licence may be revoked if they ask the worker to pay the fee or any costs linked to their application.", "Source: gov.uk/uk-visa-sponsorship-employers"),
    ("RED FLAGS", "\"Pay first, job later\"", "• An \"agent\" selling a CoS\n• Fee before any interview\n• WhatsApp-only contact, no company email\n• Pressure to pay today", None),
    ("CHECK IT", "Look the employer up yourself", "Search the GOV.UK \"Register of licensed sponsors: workers\" and apply through the company's own careers page.", None),
    ("WHAT YOU DO PAY", "Your own visa application", "You pay your visa fee and the health surcharge to the Home Office on GOV.UK, never to an agent.", "Check current amounts: gov.uk/skilled-worker-visa"),
    ("FLIEVA", "Find UK jobs that mention visa sponsorship", "Scam check included in Flieva plans. Official checklists, no agents.", "App Store · Google Play · flieva.com"),
]

def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= width: line = t
            else: out.append(line); line = w
        out.append(line)
    return out

def render(W, H, i, s, pin=False):
    tag, head, body, foot = s
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    pad = 90; tw = W - 2 * pad
    # glow
    d.ellipse((W - 420, -260, W + 260, 420), fill=(24, 22, 64))
    # top bar: logo + page
    if os.path.exists(AV):
        a = Image.open(AV).convert("RGBA").resize((72, 72)); im.paste(a, (pad, pad), a)
    d.text((pad + 90, pad + 14), "Flieva", font=ImageFont.truetype(B, 38), fill=WHITE)
    if not pin: d.text((W - pad, pad + 18), f"{i+1}/{len(SLIDES)}", font=ImageFont.truetype(B, 32), fill=MUTED, anchor="ra")
    hs = 96 if i == 0 else 78
    hf = ImageFont.truetype(B, hs); bf = ImageFont.truetype(R, 44); tf = ImageFont.truetype(B, 34)
    hl = wrap(d, head, hf, tw); bl = wrap(d, body, bf, tw)
    total = 60 + 40 + len(hl) * int(hs * 1.18) + 40 + len(bl) * 62
    y = max(pad + 160, (H - total) // 2)
    # tag pill
    pw = d.textlength(tag, font=tf) + 48
    d.rounded_rectangle((pad, y, pad + pw, y + 60), 30, fill=VIOLET)
    d.text((pad + 24, y + 30), tag, font=tf, fill=WHITE, anchor="lm"); y += 100
    for l in hl:
        d.text((pad, y), l, font=hf, fill=WHITE); y += int(hs * 1.18)
    y += 30
    d.rectangle((pad, y, pad + 120, y + 8), fill=VIOLET); y += 50
    for l in bl:
        d.text((pad, y), l, font=bf, fill=MUTED if i else WHITE); y += 62
    if foot:
        ff = ImageFont.truetype(B if i == len(SLIDES) - 1 else R, 40 if i == len(SLIDES) - 1 else 32)
        d.text((pad, H - pad - 40), foot, font=ff, fill=VIOLET if i == len(SLIDES) - 1 else MUTED)
    if i == 0:
        d.text((W - pad, H - pad - 40), "Swipe  >>", font=ImageFont.truetype(B, 40), fill=VIOLET, anchor="ra")
    return im

for i, s in enumerate(SLIDES):
    render(1080, 1350, i, s).save(f"{OUT}/ig_{i+1}.jpg", quality=92)
    render(1080, 1920, i, s).save(f"{OUT}/tt_{i+1}.jpg", quality=92)

# Pinterest text card
pin = ("SCAM CHECK", "UK job asking you to pay for your sponsorship? Read this.", "The employer pays the CoS fee and the immigration skills charge (GOV.UK). Check the Register of licensed sponsors.", "flieva.com")
im = render(1000, 1500, len(SLIDES) - 1, pin, pin=True)
im.save(f"{OUT}/pinterest_card.jpg", quality=92)
print("ok")
