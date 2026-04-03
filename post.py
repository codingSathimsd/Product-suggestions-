"""
post.py — SheValue AI v2
ONE JOB: Publish content to Blogger + Telegram.
All free. All automatic.

Blogger:  Uses Blogger API v3 (free, Google account).
Telegram: Bot API (free, instant).

Instagram: Coming later — will be added when ready.
"""

import json, os
import requests
from datetime import datetime


def load_brain():
    with open("brain.json") as f:
        return json.load(f)


def save_brain(brain):
    with open("brain.json", "w") as f:
        json.dump(brain, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# BLOGGER
# ─────────────────────────────────────────────

def post_to_blogger(html_content, headline, research):
    """
    Post to Blogger using Blogger API v3.
    Requires: BLOGGER_API_KEY + BLOGGER_BLOG_ID as GitHub secrets.
    How to get:
      1. Go to console.cloud.google.com
      2. Enable Blogger API
      3. Create API Key → save as BLOGGER_API_KEY
      4. Your Blog ID is in Blogger dashboard URL → save as BLOGGER_BLOG_ID
    """
    api_key = os.environ.get("BLOGGER_API_KEY", "")
    blog_id = os.environ.get("BLOGGER_BLOG_ID", "")

    if not api_key or not blog_id:
        print("[Post] Blogger credentials missing — saving to docs/ as fallback")
        return post_to_github_pages(html_content, headline, research)

    category = research["category"].replace("_", " ").title()
    labels = [
        category,
        "Honest Review",
        "Women India",
        "Product Review",
        research["problem"].title(),
    ]
    if research.get("festival"):
        labels.append(research["festival"])

    payload = {
        "title": headline,
        "content": html_content,
        "labels": labels,
    }

    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/?key={api_key}"
    try:
        r = requests.post(url, json=payload, timeout=20)
        if r.status_code == 200:
            post_url = r.json().get("url", "")
            print(f"[Post] ✓ Blogger: {post_url}")
            return post_url
        else:
            print(f"[Post] Blogger failed ({r.status_code}): {r.text[:200]}")
            return post_to_github_pages(html_content, headline, research)
    except Exception as e:
        print(f"[Post] Blogger exception: {e}")
        return post_to_github_pages(html_content, headline, research)


def post_to_github_pages(html_content, headline, research):
    """Fallback: save to docs/ for GitHub Pages if Blogger fails."""
    slug = load_brain()["today"].get("slug", datetime.now().strftime("%Y-%m-%d-post"))
    os.makedirs("docs/blog", exist_ok=True)
    path = f"docs/blog/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    update_index(slug, headline)
    print(f"[Post] ✓ GitHub Pages fallback: {path}")
    return f"https://shevalueai.github.io/blog/{slug}.html"


def update_index(slug, headline):
    """Update blog index page."""
    index_path = "docs/index.html"
    history_path = "docs/posts.json"

    try:
        with open(history_path) as f:
            posts = json.load(f)
    except Exception:
        posts = []

    posts.insert(0, {
        "slug": slug,
        "headline": headline,
        "date": datetime.now().strftime("%B %d, %Y"),
        "url": f"blog/{slug}.html"
    })
    posts = posts[:60]

    with open(history_path, "w") as f:
        json.dump(posts, f, indent=2)

    cards = ""
    for p in posts:
        cards += f"""<article class="card">
  <div class="date">{p['date']}</div>
  <h2><a href="{p['url']}">{p['headline']}</a></h2>
  <a href="{p['url']}" class="btn">Read Honest Review →</a>
</article>\n"""

    html = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="SheValue AI — India's most honest product reviews for women. Daily reviews. No paid promotions.">
<title>SheValue AI — Honest Product Reviews for Indian Women</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#fafafa;color:#1a1a1a}}
.hdr{{background:#1a1a1a;padding:18px 28px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}}
.logo{{color:#FFD700;font-size:24px;font-weight:800;text-decoration:none}}
.tag{{color:#aaa;font-size:13px}}
.hero{{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#fff;padding:56px 28px;text-align:center}}
.hero h1{{font-size:clamp(24px,5vw,44px);font-weight:800;margin-bottom:14px}}
.hero p{{color:#ccc;font-size:17px;max-width:580px;margin:0 auto 24px}}
.pills{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}
.pill{{background:#333;color:#FFD700;padding:7px 18px;border-radius:20px;font-size:13px;font-weight:600}}
.wrap{{max-width:860px;margin:0 auto;padding:44px 20px}}
.sec-title{{font-size:26px;font-weight:700;margin-bottom:28px;border-left:5px solid #FFD700;padding-left:14px}}
.card{{background:#fff;border-radius:12px;padding:26px;margin-bottom:18px;box-shadow:0 2px 10px rgba(0,0,0,.06);border:1px solid #f0f0f0}}
.date{{color:#888;font-size:13px;margin-bottom:7px}}
.card h2{{font-size:19px;margin-bottom:14px;line-height:1.4}}
.card h2 a{{color:#1a1a1a;text-decoration:none}}
.card h2 a:hover{{color:#C9562B}}
.btn{{background:#1a1a1a;color:#FFD700;padding:9px 18px;border-radius:7px;text-decoration:none;font-size:13px;font-weight:600}}
.tg{{background:#1a1a1a;color:#fff;border-radius:14px;padding:36px;text-align:center;margin:44px 0}}
.tg h2{{font-size:24px;margin-bottom:10px}}
.tg p{{color:#ccc;margin-bottom:20px}}
.tg a{{background:#FFD700;color:#1a1a1a;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px}}
footer{{background:#1a1a1a;color:#aaa;text-align:center;padding:20px;font-size:13px}}
footer a{{color:#FFD700;text-decoration:none}}
</style>
</head>
<body>
<header class="hdr">
  <a href="/" class="logo">⭐ SheValue AI</a>
  <span class="tag">Honest Reviews for Every Indian Woman</span>
</header>
<div class="hero">
  <h1>The Honest Truth About Every Product</h1>
  <p>Daily honest product reviews for Indian women. Real pros. Real cons. No paid promotions. Ever.</p>
  <div class="pills">
    <div class="pill">✓ No paid promotions</div>
    <div class="pill">✓ Real ratings only</div>
    <div class="pill">✓ Updated daily</div>
    <div class="pill">✓ Indian context</div>
  </div>
</div>
<div class="wrap">
  <div class="sec-title">Latest Honest Reviews</div>
  {cards}
  <div class="tg">
    <h2>Get Daily Reviews on Telegram</h2>
    <p>Join thousands of Indian women who read SheValue before buying anything.</p>
    <a href="https://t.me/shevalueai">Join Free Telegram Channel →</a>
  </div>
</div>
<footer>
  © {datetime.now().year} SheValue AI ·
  <a href="https://t.me/shevalueai">Telegram</a>
</footer>
</body>
</html>"""

    os.makedirs("docs", exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[Post] ✓ Index updated")


# ─────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────

def post_to_telegram(message, image_path=None):
    """
    Post to Telegram channel using Bot API.
    How to set up:
      1. Message @BotFather on Telegram → /newbot → copy token
      2. Create a Telegram channel → add your bot as admin
      3. Get channel ID via @userinfobot
      4. Save as TELEGRAM_BOT_TOKEN + TELEGRAM_CHANNEL_ID in GitHub secrets
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    channel = os.environ.get("TELEGRAM_CHANNEL_ID", "")

    if not token or not channel:
        print("[Post] Telegram credentials missing — skipping")
        return False

    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img:
                r = requests.post(
                    f"https://api.telegram.org/bot{token}/sendPhoto",
                    data={
                        "chat_id": channel,
                        "caption": message[:1024],
                        "parse_mode": "Markdown"
                    },
                    files={"photo": img},
                    timeout=20,
                )
        else:
            r = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": channel,
                    "text": message,
                    "parse_mode": "Markdown"
                },
                timeout=20,
            )

        if r.status_code == 200:
            print("[Post] ✓ Telegram posted")
            return True
        else:
            print(f"[Post] Telegram error {r.status_code}: {r.text[:150]}")
            return False

    except Exception as e:
        print(f"[Post] Telegram exception: {e}")
        return False


# ─────────────────────────────────────────────
# MAIN PUBLISHER
# ─────────────────────────────────────────────

def publish_all(write_result, image_path, research):
    """Publish to Blogger + Telegram. Log results."""
    results = {}

    print("\n[Post] Publishing...")

    # 1. Blogger
    results["blogger"] = post_to_blogger(
        write_result["html"],
        write_result["headline"],
        research
    )

    # 2. Telegram
    results["telegram"] = post_to_telegram(
        write_result["telegram"],
        image_path
    )

    # Log to brain
    brain = load_brain()
    log_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "headline": write_result["headline"],
        "category": research["category"],
        "results": {k: bool(v) for k, v in results.items()},
    }
    brain["performance"]["log"].insert(0, log_entry)
    brain["performance"]["log"] = brain["performance"]["log"][:60]
    brain["performance"]["total_posts"] = brain["performance"].get("total_posts", 0) + 1
    save_brain(brain)

    success = [k for k, v in results.items() if v]
    print(f"[Post] Published to: {', '.join(success) if success else 'none — check credentials'}")
    return results


if __name__ == "__main__":
    print("Checking credentials...")
    print(f"Blogger API key:  {'✓ Set' if os.environ.get('BLOGGER_API_KEY') else '✗ Missing'}")
    print(f"Blogger Blog ID:  {'✓ Set' if os.environ.get('BLOGGER_BLOG_ID') else '✗ Missing'}")
    print(f"Telegram token:   {'✓ Set' if os.environ.get('TELEGRAM_BOT_TOKEN') else '✗ Missing'}")
    print(f"Telegram channel: {'✓ Set' if os.environ.get('TELEGRAM_CHANNEL_ID') else '✗ Missing'}")
          
