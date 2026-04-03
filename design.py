"""
design.py — SheValue AI v2
ONE JOB: Generate a professional Instagram post image (1080x1080).
Uses only Pillow — free. No external design services.
"""

import json, os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

THEMES = {
    "minimal_bold":   {"bg": "#1a1a1a", "text": "#FFFFFF", "accent": "#FFD700", "card": "#2a2a2a"},
    "warm_editorial": {"bg": "#FFF8F0", "text": "#1a1a1a", "accent": "#C9562B", "card": "#FFFFFF"},
    "data_card":      {"bg": "#FFFFFF", "text": "#1a1a1a", "accent": "#FFD700", "card": "#F5F5F5"},
    "diwali_gold":    {"bg": "#1a0a00", "text": "#FFD700", "accent": "#FF8C00", "card": "#2a1200"},
    "green_gold":     {"bg": "#003300", "text": "#FFD700", "accent": "#FFFFFF", "card": "#004400"},
    "navratri":       {"bg": "#8B0000", "text": "#FFD700", "accent": "#FFFFFF", "card": "#6B0000"},
    "vibrant":        {"bg": "#FFFFFF", "text": "#1a1a1a", "accent": "#FF6B6B", "card": "#FFF5F5"},
    "warm_saffron":   {"bg": "#FF8C00", "text": "#FFFFFF", "accent": "#1a1a1a", "card": "#FF7000"},
    "kerala_green":   {"bg": "#1a3a1a", "text": "#FFD700", "accent": "#FFFFFF", "card": "#2a4a2a"},
    "bridal_red":     {"bg": "#5a0000", "text": "#FFD700", "accent": "#FFFFFF", "card": "#6a0000"},
    "christmas":      {"bg": "#003300", "text": "#FFFFFF", "accent": "#FF0000", "card": "#004400"},
    "glitter":        {"bg": "#1a1a1a", "text": "#FFD700", "accent": "#C0C0C0", "card": "#2a2a2a"},
    "pastel":         {"bg": "#FFF0F5", "text": "#1a1a1a", "accent": "#FF69B4", "card": "#FFFFFF"},
    "mustard":        {"bg": "#FFF3C4", "text": "#1a1a1a", "accent": "#FF8C00", "card": "#FFFFFF"},
    "red_gold":       {"bg": "#4a0000", "text": "#FFD700", "accent": "#FFFFFF", "card": "#5a0000"},
    "orange":         {"bg": "#FF6B00", "text": "#FFFFFF", "accent": "#FFD700", "card": "#E05C00"},
}


def h2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def font(size, bold=False):
    paths = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{'Bold' if bold else 'Regular'}.ttf",
        "C:/Windows/Fonts/{'arialbd' if bold else 'arial'}.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def wrap_text(draw, text, x, y, max_w, fnt, fill, spacing=6):
    """Word-wrap text and return final y."""
    words = text.split()
    line = ""
    lines = []
    for w in words:
        test = (line + " " + w).strip()
        if fnt.getbbox(test)[2] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    cy = y
    for l in lines:
        draw.text((x, cy), l, font=fnt, fill=fill)
        h = fnt.getbbox(l)[3]
        cy += h + spacing
    return cy


def rrect(draw, xy, r, fill):
    """Draw rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    for cx, cy in [(x1, y1), (x2-2*r, y1), (x1, y2-2*r), (x2-2*r, y2-2*r)]:
        draw.ellipse([cx, cy, cx+2*r, cy+2*r], fill=fill)


def load_brain():
    with open("brain.json") as f:
        return json.load(f)


def get_theme(brain):
    festival = brain["today"].get("festival_name", "")
    if festival:
        for f in brain["festivals"]["calendar"]:
            if f["name"] == festival:
                return f.get("theme", "minimal_bold")
    idx = brain["strategy"]["design_index"]
    return brain["strategy"]["design_rotation"][idx]


def generate_image(content):
    """
    content = {
      headline, category, problem, products: [{title, price, rating, reviews}]
    }
    Returns output path.
    """
    brain = load_brain()
    theme_key = get_theme(brain)
    t = THEMES.get(theme_key, THEMES["minimal_bold"])

    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), h2rgb(t["bg"]))
    draw = ImageDraw.Draw(img)

    top = content["products"][0] if content["products"] else {}
    headline = content.get("headline", "Honest Product Review")
    category = content.get("category", "skincare").replace("_", " ").title()
    today = datetime.now().strftime("%d %B %Y")

    # ── TOP BAR ──────────────────────────
    draw.rectangle([0, 0, W, 88], fill=h2rgb(t["accent"]))
    draw.text((44, 24), "⭐ SheValue AI", font=font(30, True), fill=h2rgb(t["bg"]))
    draw.text((W-200, 32), today, font=font(20), fill=h2rgb(t["bg"]))

    # ── CATEGORY BADGE ───────────────────
    bf = font(20, True)
    btext = f"  {category}  "
    bw = bf.getbbox(btext)[2] + 16
    rrect(draw, [44, 112, 44+bw, 150], 14, h2rgb(t["accent"]))
    draw.text((52, 118), btext, font=bf, fill=h2rgb("#1a1a1a"))

    # ── HEADLINE ─────────────────────────
    hf = font(48, True)
    short_hl = headline if len(headline) <= 52 else headline[:49] + "..."
    hy = wrap_text(draw, short_hl, 44, 170, W-88, hf, h2rgb(t["text"]), spacing=8)

    # ── DIVIDER ──────────────────────────
    draw.rectangle([44, hy+10, W-44, hy+13], fill=h2rgb(t["accent"]))

    # ── PRODUCT CARD ─────────────────────
    cy = hy + 30
    card_h = 300
    rrect(draw, [44, cy, W-44, cy+card_h], 18, h2rgb(t["card"]))

    draw.text((74, cy+18), "  #1 HONEST PICK  ", font=font(19, True), fill=h2rgb(t["accent"]))

    pname = top.get("title", "Top Product")
    pname = pname if len(pname) <= 42 else pname[:39] + "..."
    wrap_text(draw, pname, 74, cy+56, W-148, font(34, True), h2rgb(t["text"]))

    draw.text((74, cy+155), f"₹{top.get('price','?')}", font=font(52, True), fill=h2rgb(t["accent"]))

    rating = top.get("rating", 0)
    stars = "★" * int(rating) + "☆" * (5-int(rating))
    draw.text((74, cy+222), f"{stars}  {rating}/5", font=font(30), fill=h2rgb(t["accent"]))

    reviews = top.get("reviews", 0)
    if reviews:
        draw.text((74, cy+265), f"{reviews:,} verified reviews · Amazon India",
                  font=font(22), fill=h2rgb("#888888" if t["bg"] == "#FFFFFF" else "#aaaaaa"))

    # ── TRUST SIGNALS ────────────────────
    ty = cy + card_h + 22
    tf = font(24, True)
    sigs = ["✓ No paid promotions", "✓ Honest cons included", "✓ Real data only"]
    tx = 44
    for sig in sigs:
        sw = tf.getbbox(sig)[2]
        if tx + sw > W - 44:
            ty += 36
            tx = 44
        draw.text((tx, ty), sig, font=tf, fill=h2rgb(t["accent"]))
        tx += sw + 28

    # ── BOTTOM CTA ───────────────────────
    draw.rectangle([0, H-92, W, H], fill=h2rgb(t["accent"]))
    cta = "Full Review + 3 Products → Link in Bio"
    cf = font(28, True)
    cx = (W - cf.getbbox(cta)[2]) // 2
    draw.text((cx, H-64), cta, font=cf, fill=h2rgb("#1a1a1a"))

    # ── WATERMARK ────────────────────────
    draw.text((44, H-126), "@shevalueai", font=font(20),
              fill=h2rgb("#666666" if t["bg"] in ["#FFFFFF", "#FFF8F0", "#FFF0F5"] else "#555555"))

    # ── SAVE ─────────────────────────────
    slug = content.get("slug", datetime.now().strftime("%Y-%m-%d"))
    os.makedirs("output/posts", exist_ok=True)
    path = f"output/posts/{slug}.png"
    img.save(path, "PNG", quality=95)
    print(f"[Design] Image saved: {path}")

    # Rotate design style for tomorrow
    brain["strategy"]["design_index"] = \
        (brain["strategy"]["design_index"] + 1) % len(brain["strategy"]["design_rotation"])
    with open("brain.json", "w") as f:
        json.dump(brain, f, indent=2)

    return path


if __name__ == "__main__":
    sample = {
        "headline": "3 Honest Vitamin C Serums Under ₹500 That Actually Work",
        "category": "skincare",
        "slug": "test-post",
        "products": [{"title": "Minimalist 10% Vitamin C Serum", "price": 349, "rating": 4.4, "reviews": 15200}],
    }
    print(generate_image(sample))
      
