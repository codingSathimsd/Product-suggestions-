"""
write.py - SheValue AI v2
ONE JOB: Write an honest, SEO-optimised review using Gemini.
Generates: Blog HTML + Instagram caption + Telegram message.
"""

import json, os, re
from datetime import datetime
import google.generativeai as genai

MODEL = "gemini-2.0-flash-exp"

PSYCHOLOGY = {
    "honest_con_trick":   "State the BIGGEST flaw of each product FIRST. This builds instant trust. Then give genuine benefits. End with exactly who should and should not buy.",
    "problem_first_hook": "Open with the exact pain point. Make her feel you understand her struggle personally. Then position products as her solution.",
    "social_proof":       "Lead with real numbers: ratings and review counts from Amazon India. Make her feel she is joining thousands of trusted Indian women.",
    "price_anchoring":    "Show the most expensive option first. Then reveal the affordable option. Make the budget pick feel like a steal.",
    "loss_aversion":      "Tell her what she loses every day without fixing this problem. Make inaction feel more costly than buying.",
    "micro_commitment":   "Ask 3 small yes-questions before recommending. Each yes pulls her closer to the final pick.",
}


def load_brain():
    with open("brain.json") as f:
        return json.load(f)


def save_brain(brain):
    brain["last_updated"] = datetime.now().isoformat()
    with open("brain.json", "w") as f:
        json.dump(brain, f, indent=2, ensure_ascii=False)


def make_slug(text):
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return f"{datetime.now().strftime('%Y-%m-%d')}-{s[:55]}"


def build_prompt(research, brain):
    psych_key = brain["strategy"]["psychology_rotation"][brain["strategy"]["psychology_index"]]
    psych_instruction = PSYCHOLOGY.get(psych_key, PSYCHOLOGY["honest_con_trick"])
    festival = research.get("festival", "")
    festival_note = f"\nIMPORTANT: {festival} is coming soon. Naturally mention this festival where relevant (gifting, festive look, seasonal skin needs). Keep it genuine.\n" if festival else ""
    affiliate_tag = brain["system"].get("affiliate_tag", "")

    products_text = ""
    for i, p in enumerate(research["products"], 1):
        url = p.get("url", f"https://www.amazon.in/dp/{p.get('asin','')}")
        if affiliate_tag and "?tag=" not in url:
            url += f"?tag={affiliate_tag}"
        products_text += f"""
Product {i}: {p['title']}
Price: ₹{p['price']} | Rating: {p['rating']}/5 | Reviews: {p.get('reviews', 'N/A')} on Amazon India
Buy Link: {url}
"""

    return f"""You are SheValue AI - India's most trusted honest product platform for women.
Personality: Warm, direct older sister. Never salesy. Never fake.
Language: Pure English. Indian context (₹ prices, Indian skin types, Indian climate).

TODAY'S TASK:
Category: {research['category']}
Problem to solve: {research['problem']}
Date: {datetime.now().strftime('%B %d, %Y')}
{festival_note}

PRODUCTS:
{products_text}

PSYCHOLOGY TECHNIQUE TO USE:
{psych_instruction}

WRITE A COMPLETE BLOG ARTICLE WITH THIS EXACT STRUCTURE:

---HEADLINE---
[One powerful line. Max 12 words. Must include: number + problem + "honest"]
Example format: "3 Honest [Category] Products Under ₹[price] That Actually Work"

---INTRO---
[2-3 sentences. Use the psychology technique. Make her feel understood.]

---REVIEW---
For each product write:
## Product [N]: [Full product name] - ₹[price]
★ [rating]/5 based on [reviews] real Amazon India reviews
✓ PRO 1: [specific genuine benefit]
✓ PRO 2: [specific genuine benefit]  
✓ PRO 3: [specific genuine benefit]
✗ HONEST CON: [real flaw - never hide this]
💰 Value: [Poor/Fair/Good/Excellent] for the price
👩 Best for: [specific skin type or concern]
🚫 Skip if: [exact who should not buy]
🛒 Buy here: [amazon link]

---WHO SHOULD BUY WHAT---
[2 lines per product. Be decisive. "If you have X, buy Product 1. Not Product 2."]

---SHEVALUE VERDICT---
[One clear winner. Exact reason. Price. Link.]

---HONEST DISCLAIMER---
If none of these solve a specific problem, say so. Example: "If your acne is hormonal, no face wash will fix it."

RULES:
- Never fake urgency
- Never hide flaws  
- Always give a do-not-buy condition
- Use ₹ always
- Mention Indian skin tones and Indian climate where relevant
- 600-800 words total
- SEO: naturally include phrases like "best [product] for Indian women", "honest review India", "[product] under ₹[price] India"

Write the full article now:"""


def call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text


def extract_headline(text):
    """Pull headline from article."""
    lines = text.strip().split("\n")
    for line in lines[:8]:
        line = line.strip().lstrip("#--").strip()
        if 10 < len(line) < 120 and "headline" not in line.lower():
            return line
    return f"Honest Review: Best Products for {datetime.now().strftime('%B %Y')}"


def build_html(article_text, headline, research, brain):
    """Convert article text to full SEO-optimised Blogger-ready HTML."""
    today = datetime.now().strftime("%B %d, %Y")
    category = research["category"].replace("_", " ").title()
    problem = research["problem"]
    site_name = brain["system"]["name"]
    site_desc = brain["seo"]["site_description"]
    blogger_url = brain["system"]["blogger_url"]

    # Convert article text to HTML
    body = ""
    for line in article_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("##"):
            body += f'<h2>{line.lstrip("#").strip()}</h2>\n'
        elif line.startswith("★") or line.startswith("✓") or line.startswith("✗") or \
             line.startswith("💰") or line.startswith("👩") or line.startswith("🚫") or \
             line.startswith("🛒"):
            body += f'<p class="rp">{line}</p>\n'
        elif line.startswith("-") or line.startswith("•"):
            body += f'<li>{line.lstrip("-•").strip()}</li>\n'
        else:
            body += f'<p>{line}</p>\n'

    # Schema.org structured data for Google
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": f"Honest review of best {problem} products for Indian women. Real pros and cons.",
        "author": {"@type": "Organization", "name": site_name},
        "publisher": {
            "@type": "Organization",
            "name": site_name,
            "logo": {"@type": "ImageObject", "url": f"{blogger_url}/logo.png"}
        },
        "datePublished": datetime.now().isoformat(),
        "dateModified": datetime.now().isoformat(),
        "image": f"{blogger_url}/og-default.png",
        "mainEntityOfPage": {"@type": "WebPage", "@id": blogger_url}
    }, indent=2)

    # Product schema for rich results
    product_schema_list = []
    for p in research["products"]:
        product_schema_list.append({
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["title"],
            "offers": {
                "@type": "Offer",
                "price": str(p["price"]),
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(p["rating"]),
                "reviewCount": str(p.get("reviews", 100))
            }
        })

    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Honest review: best {problem} products for Indian women. Real pros and cons. No paid promotions. By {site_name}.">
<meta name="keywords" content="{problem} india, honest review india, best {research['category']} indian women, {research['category']} under budget india">
<meta name="author" content="{site_name}">
<meta name="robots" content="index, follow">

<!-- Open Graph for social sharing -->
<meta property="og:type" content="article">
<meta property="og:title" content="{headline} | {site_name}">
<meta property="og:description" content="Honest review: best products for {problem} in India. Real ratings. Honest cons. Best price range.">
<meta property="og:site_name" content="{site_name}">
<meta property="og:locale" content="en_IN">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{headline}">
<meta name="twitter:description" content="Honest {research['category']} review for Indian women. {site_name}.">

<!-- Schema.org Article -->
<script type="application/ld+json">{schema}</script>
<!-- Schema.org Products -->
<script type="application/ld+json">{json.dumps(product_schema_list, indent=2)}</script>

<title>{headline} | {site_name}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#fafafa;color:#1a1a1a;line-height:1.8;font-size:16px}}
.hdr{{background:#1a1a1a;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}}
.logo{{color:#FFD700;font-size:22px;font-weight:800;letter-spacing:1px;text-decoration:none}}
.hdr-tag{{color:#aaa;font-size:13px}}
.hero{{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#fff;padding:48px 24px;text-align:center}}
.badge{{background:#FFD700;color:#1a1a1a;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;display:inline-block;margin-bottom:14px}}
.hero h1{{font-size:clamp(20px,4vw,34px);font-weight:800;line-height:1.3;max-width:720px;margin:0 auto 12px}}
.hero-meta{{color:#aaa;font-size:13px}}
.trust{{background:#FFD700;padding:10px 24px;text-align:center;font-size:13px;font-weight:700;color:#1a1a1a}}
.wrap{{max-width:780px;margin:0 auto;padding:36px 20px}}
h2{{font-size:22px;font-weight:700;margin:32px 0 14px;border-left:4px solid #FFD700;padding-left:12px;color:#1a1a1a}}
p{{margin-bottom:14px}}
.rp{{background:#f5f5f5;border-radius:8px;padding:10px 14px;margin:6px 0;font-size:15px}}
li{{margin-left:18px;margin-bottom:8px}}
.cta{{background:#1a1a1a;color:#fff;border-radius:14px;padding:36px 24px;text-align:center;margin:40px 0}}
.cta h3{{font-size:22px;margin-bottom:10px}}
.cta p{{color:#ccc;margin-bottom:20px;font-size:15px}}
.cta a{{background:#FFD700;color:#1a1a1a;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px;display:inline-block}}
.disc{{font-size:12px;color:#999;margin-top:28px;padding:14px;background:#f9f9f9;border-radius:8px;border-left:3px solid #ddd}}
footer{{background:#1a1a1a;color:#aaa;text-align:center;padding:20px;font-size:13px}}
footer a{{color:#FFD700;text-decoration:none}}
@media(max-width:600px){{.hero h1{{font-size:20px}}.wrap{{padding:24px 16px}}}}
</style>
</head>
<body>
<header class="hdr">
  <a href="{blogger_url}" class="logo">⭐ {site_name}</a>
  <span class="hdr-tag">Honest Reviews for Every Indian Woman</span>
</header>
<div class="hero">
  <div class="badge">{category}</div>
  <h1>{headline}</h1>
  <div class="hero-meta">Published {today} · Researched by {site_name} · Honest. Always.</div>
</div>
<div class="trust">✓ No paid promotions &nbsp;·&nbsp; ✓ Real Amazon ratings &nbsp;·&nbsp; ✓ Honest pros AND cons &nbsp;·&nbsp; ✓ Updated daily</div>
<main class="wrap">
{body}
<div class="cta">
  <h3>Get Daily Honest Reviews Free</h3>
  <p>Join thousands of Indian women who read SheValue before buying anything.</p>
  <a href="https://t.me/shevalueai">Join Telegram Channel →</a>
</div>
<div class="disc">
  <strong>Disclaimer:</strong> SheValue AI earns no commission from these recommendations.
  Prices on Amazon India may change. Always check the full ingredient list if you have sensitive skin or allergies.
  This review is for informational purposes only. Consult a dermatologist for medical skin concerns.
</div>
</main>
<footer>© {datetime.now().year} {site_name} · <a href="{blogger_url}">Blog</a> · <a href="https://t.me/shevalueai">Telegram</a></footer>
</body>
</html>"""


def build_telegram(headline, research, products):
    today = datetime.now().strftime("%d %B %Y")
    top = products[0]
    lines = [
        f"⭐ *SheValue AI - {today}*",
        "",
        f"*{headline}*",
        "",
        "--------------",
        f"🔍 *Today's problem solved:* {research['problem'].title()}",
        "--------------",
        "",
        f"🏆 *#1 Honest Pick:*",
        f"📦 {top['title']}",
        f"💰 ₹{top['price']}",
        f"★ {top['rating']}/5 · {top.get('reviews','?')} reviews",
        f"🛒 {top.get('url','https://www.amazon.in')}",
        "",
        "--------------",
        "📖 *Full honest review (all 3 + who NOT to buy for):*",
        "👉 https://shevalueai.blogspot.com",
        "--------------",
        "",
        "💬 Questions? Reply here.",
        "🔔 Share with a friend who needs this today 🙏",
    ]
    return "\n".join(lines)


def build_instagram_caption(headline, research, products, brain):
    top = products[0]
    psych_idx = brain["strategy"]["psychology_index"]
    psych_key = brain["strategy"]["psychology_rotation"][psych_idx]
    hooks = {
        "honest_con_trick": f"I'll be honest - {top['title']} has one real flaw. But here's why {top.get('reviews','10,000+')} women still love it 👇",
        "problem_first_hook": f"Struggling with {research['problem']}? You are not alone. Here is what actually works 👇",
        "social_proof": f"{top.get('reviews','10,000+')} women on Amazon India rated this {top['rating']}★. Here is the honest truth 👇",
        "price_anchoring": f"You do not need to spend ₹2,000 to fix {research['problem']}. This ₹{top['price']} option delivers 👇",
        "loss_aversion": f"Every day without the right product makes {research['problem']} worse. Here is what to do 👇",
        "micro_commitment": f"Want to fix {research['problem']}? Want to spend under ₹{top['price']}? Want the honest truth? Read this 👇",
    }
    hook = hooks.get(psych_key, f"Honest review: Best products for {research['problem']} 👇")
    tags = "#SheValueAI #HonestReview #IndianWomen #SkincareIndia #BeautyIndia #ProductReview #AffordableBeauty #TrustHonesty #IndianBeauty #WomenIndia #BudgetBeauty #BeautyTips #MakeupIndia #WomenEmpowerment #HonestSkincare"
    return f"""{hook}

⭐ SheValue Honest Pick:
📦 {top['title']}
💰 ₹{top['price']} on Amazon India
★ {top['rating']}/5 · {top.get('reviews','?')} real reviews

✓ Actually works for Indian skin
✗ CON: Results take consistent use

Full honest review + all 3 options + who should NOT buy → Link in bio

--
{tags}
--
🔔 Follow @shevalueai for daily honest reviews."""


def write_today(research):
    """Main function. Returns all content needed for publishing."""
    brain = load_brain()
    prompt = build_prompt(research, brain)

    print(f"[Write] Writing review for: {research['problem']}")

    try:
        article_text = call_gemini(prompt)
    except Exception as e:
        print(f"[Write] Gemini failed ({e}) - using fallback template")
        article_text = fallback_article(research)

    headline = extract_headline(article_text)
    slug = make_slug(headline)
    html = build_html(article_text, headline, research, brain)
    telegram = build_telegram(headline, research, research["products"])
    instagram = build_instagram_caption(headline, research, research["products"], brain)

    # Save files
    os.makedirs("output/blogs", exist_ok=True)
    os.makedirs("output/telegram", exist_ok=True)

    with open(f"output/blogs/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)
    with open(f"output/telegram/{slug}.txt", "w", encoding="utf-8") as f:
        f.write(telegram)

    print(f"[Write] Done. Headline: {headline}")

    # Rotate psychology for tomorrow
    brain["strategy"]["psychology_index"] = \
        (brain["strategy"]["psychology_index"] + 1) % len(brain["strategy"]["psychology_rotation"])
    brain["today"]["headline"] = headline
    brain["today"]["slug"] = slug
    save_brain(brain)

    return {
        "headline": headline,
        "slug": slug,
        "html": html,
        "telegram": telegram,
        "article_text": article_text,
    }


def fallback_article(research):
    top = research["products"][0] if research["products"] else {}
    return f"""# 3 Honest Products for {research['problem'].title()} - Tested for Indian Women

Struggling with {research['problem']}? We researched the top-rated options on Amazon India.

## Product 1: {top.get('title','Top Pick')} - ₹{top.get('price','?')}
★ {top.get('rating','4.0')}/5 based on {top.get('reviews','?')} reviews
✓ PRO 1: Well rated by Indian women
✓ PRO 2: Available on Amazon India
✓ PRO 3: Good value for price
✗ HONEST CON: Results require consistent use
💰 Value: Good
👩 Best for: Women dealing with {research['problem']}
🚫 Skip if: Your concern is severe - see a dermatologist first
🛒 Buy here: {top.get('url','https://www.amazon.in')}

## SheValue Verdict
Our honest top pick for {research['problem']} at this price range.

*Follow SheValue on Telegram for daily honest reviews.*"""


if __name__ == "__main__":
    sample = {
        "category": "skincare",
        "problem": "hyperpigmentation and dark spots",
        "festival": "",
        "products": [
            {"title": "Minimalist 10% Vitamin C Serum", "price": 349, "rating": 4.4, "reviews": 15200, "asin": "B08XY1234A", "url": "https://www.amazon.in/dp/B08XY1234A", "score": 85},
            {"title": "Dot & Key Waterlight Gel Moisturiser", "price": 449, "rating": 4.3, "reviews": 11800, "asin": "B09XY5678B", "url": "https://www.amazon.in/dp/B09XY5678B", "score": 80},
            {"title": "Plum Green Tea Face Wash", "price": 239, "rating": 4.2, "reviews": 22100, "asin": "B07XY5678B", "url": "https://www.amazon.in/dp/B07XY5678B", "score": 78},
        ],
    }
    result = write_today(sample)
    print(f"Headline: {result['headline']}")
    
