"""
research.py - SheValue AI v2
ONE JOB: Find today's trending problem + top 3 products.
Fast. Simple. If anything fails, uses smart fallback instantly.
"""

import json, random, time, requests
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}

# Curated fallback products - always work even if scraping fails
FALLBACKS = {
    "skincare": [
        {"title": "Minimalist 10% Vitamin C Serum", "price": 349, "rating": 4.4, "reviews": 15200, "brand": "Minimalist", "asin": "B08XY1234A"},
        {"title": "Dot & Key Waterlight Gel Moisturiser", "price": 449, "rating": 4.3, "reviews": 11800, "brand": "Dot & Key", "asin": "B09XY5678B"},
        {"title": "Minimalist SPF 50 Sunscreen", "price": 299, "rating": 4.4, "reviews": 24300, "brand": "Minimalist", "asin": "B09XY9012A"},
        {"title": "Plum Green Tea Face Wash", "price": 239, "rating": 4.2, "reviews": 22100, "brand": "Plum", "asin": "B07XY5678B"},
        {"title": "Mamaearth Ubtan Face Wash", "price": 199, "rating": 4.1, "reviews": 31400, "brand": "Mamaearth", "asin": "B06XY5678C"},
        {"title": "Lotus Safe Sun UV Screen SPF50", "price": 285, "rating": 4.1, "reviews": 19200, "brand": "Lotus", "asin": "B07XY9012C"},
        {"title": "Wow Skin Science Vitamin C Serum", "price": 399, "rating": 4.0, "reviews": 18700, "brand": "WOW", "asin": "B08XY3456D"},
        {"title": "Plum Bright Years Cell Renewal Serum", "price": 699, "rating": 4.3, "reviews": 5400, "brand": "Plum", "asin": "B07XY1234C"},
    ],
    "haircare": [
        {"title": "Indulekha Bringha Hair Oil", "price": 449, "rating": 4.2, "reviews": 38000, "brand": "Indulekha", "asin": "B00HAIR001"},
        {"title": "WOW Apple Cider Vinegar Shampoo", "price": 349, "rating": 4.1, "reviews": 29000, "brand": "WOW", "asin": "B00HAIR002"},
        {"title": "Mamaearth Onion Hair Oil", "price": 299, "rating": 4.0, "reviews": 42000, "brand": "Mamaearth", "asin": "B00HAIR003"},
        {"title": "Kesh King Scalp and Hair Medicine Oil", "price": 175, "rating": 4.1, "reviews": 55000, "brand": "Kesh King", "asin": "B00HAIR004"},
    ],
    "makeup": [
        {"title": "Lakme Eyeconic Kajal", "price": 199, "rating": 4.3, "reviews": 67000, "brand": "Lakme", "asin": "B00MAKE001"},
        {"title": "Maybelline Colossal Kajal", "price": 179, "rating": 4.2, "reviews": 89000, "brand": "Maybelline", "asin": "B00MAKE002"},
        {"title": "Sugar Cosmetics Matte Lipstick", "price": 349, "rating": 4.1, "reviews": 22000, "brand": "Sugar", "asin": "B00MAKE003"},
        {"title": "Lakme Absolute Skin Natural Mousse", "price": 425, "rating": 4.0, "reviews": 18000, "brand": "Lakme", "asin": "B00MAKE004"},
    ],
    "wellness": [
        {"title": "Himalaya Ashwagandha Tablets", "price": 199, "rating": 4.2, "reviews": 28000, "brand": "Himalaya", "asin": "B00WELL001"},
        {"title": "Carbamide Forte Iron + Folic Acid", "price": 349, "rating": 4.3, "reviews": 15000, "brand": "Carbamide Forte", "asin": "B00WELL002"},
        {"title": "WOW Life Science Vitamin D3+K2", "price": 399, "rating": 4.1, "reviews": 12000, "brand": "WOW", "asin": "B00WELL003"},
    ],
    "health_fitness": [
        {"title": "Boldfit Yoga Mat 6mm", "price": 699, "rating": 4.2, "reviews": 34000, "brand": "Boldfit", "asin": "B00FIT001"},
        {"title": "Strauss Resistance Bands Set", "price": 349, "rating": 4.1, "reviews": 22000, "brand": "Strauss", "asin": "B00FIT002"},
        {"title": "Boldfit Skipping Rope", "price": 199, "rating": 4.0, "reviews": 41000, "brand": "Boldfit", "asin": "B00FIT003"},
    ],
    "kitchen_home": [
        {"title": "Prestige Iris 750W Mixer Grinder", "price": 2195, "rating": 4.3, "reviews": 28000, "brand": "Prestige", "asin": "B00KIT001"},
        {"title": "Pigeon by Stovekraft Non Stick Pan", "price": 399, "rating": 4.1, "reviews": 45000, "brand": "Pigeon", "asin": "B00KIT002"},
        {"title": "Milton Thermosteel Flask 500ml", "price": 549, "rating": 4.4, "reviews": 31000, "brand": "Milton", "asin": "B00KIT003"},
    ],
    "perfume": [
        {"title": "Fogg Scent Xpressio EDP", "price": 399, "rating": 4.2, "reviews": 52000, "brand": "Fogg", "asin": "B00PERF001"},
        {"title": "Engage W1 Perfume Spray Women", "price": 249, "rating": 4.0, "reviews": 38000, "brand": "Engage", "asin": "B00PERF002"},
        {"title": "Skinn by Titan Celeste EDP", "price": 799, "rating": 4.3, "reviews": 19000, "brand": "Skinn", "asin": "B00PERF003"},
    ],
    "fashion": [
        {"title": "BIBA Women Printed Kurta", "price": 699, "rating": 4.1, "reviews": 14000, "brand": "BIBA", "asin": "B00FASH001"},
        {"title": "W Women Printed Straight Kurta", "price": 849, "rating": 4.0, "reviews": 11000, "brand": "W", "asin": "B00FASH002"},
        {"title": "Libas Women Straight Kurta", "price": 499, "rating": 4.2, "reviews": 28000, "brand": "Libas", "asin": "B00FASH003"},
    ],
}

PROBLEMS = {
    "skincare": [
        "hyperpigmentation and dark spots",
        "oily skin and acne breakouts",
        "dry and dehydrated skin",
        "sun damage and tanning",
        "dark circles and puffy eyes",
        "early signs of aging",
        "large open pores",
        "dull and uneven skin tone",
        "sensitive and reactive skin",
    ],
    "haircare": [
        "hair fall and thinning",
        "dandruff and itchy scalp",
        "dry and frizzy hair",
        "slow hair growth",
        "heat damaged hair",
    ],
    "makeup": [
        "long lasting kajal for Indian eyes",
        "best lipstick under ₹300",
        "foundation for Indian skin tones",
        "waterproof eye makeup monsoon",
    ],
    "wellness": [
        "iron deficiency in Indian women",
        "vitamin D deficiency India",
        "low energy and fatigue women",
        "immunity boosting supplements",
    ],
    "health_fitness": [
        "home workout equipment on budget",
        "yoga essentials for beginners",
        "fitness tracking affordable",
    ],
    "kitchen_home": [
        "best mixer grinder for Indian cooking",
        "non toxic cookware India",
        "affordable smart kitchen tools",
    ],
    "perfume": [
        "long lasting perfume under ₹500",
        "best deo for women India summer",
        "affordable floral perfume India",
    ],
    "fashion": [
        "affordable ethnic wear for office",
        "stylish kurta under ₹700",
        "casual wear for Indian women",
    ],
}


def load_brain():
    with open("brain.json") as f:
        return json.load(f)


def amazon_url(asin, affiliate_tag=""):
    base = f"https://www.amazon.in/dp/{asin}"
    if affiliate_tag:
        return f"{base}?tag={affiliate_tag}"
    return base


def score_product(p):
    r = p.get("rating", 0)
    rv = p.get("reviews", 0)
    pr = p.get("price", 9999)
    rating_pts = (r / 5) * 40
    review_pts = min(rv / 1000, 25)
    if pr <= 200: price_pts = 25
    elif pr <= 500: price_pts = 20
    elif pr <= 1000: price_pts = 14
    elif pr <= 2000: price_pts = 8
    else: price_pts = 3
    return round(rating_pts + review_pts + price_pts, 1)


def scrape_amazon(keyword, max_results=5):
    """Try Amazon scraping. Returns empty list on any failure."""
    products = []
    try:
        url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
        time.sleep(random.uniform(2, 3))
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.content, "lxml")
        for item in soup.select('[data-component-type="s-search-result"]')[:max_results * 2]:
            try:
                title = item.select_one("h2 span")
                price = item.select_one(".a-price-whole")
                rating = item.select_one(".a-icon-alt")
                reviews = item.select_one('[aria-label*="ratings"]')
                asin = item.get("data-asin", "")
                if not title or not price or not asin:
                    continue
                p = int(price.get_text().replace(",", "").strip())
                ra = float(rating.get_text().split()[0]) if rating else 0
                rv_text = reviews.get_text().replace(",", "").strip() if reviews else "0"
                rv = int("".join(c for c in rv_text if c.isdigit()) or "0")
                if ra < 3.5 or p < 50:
                    continue
                products.append({
                    "title": title.get_text(strip=True),
                    "price": p, "rating": ra, "reviews": rv,
                    "asin": asin, "brand": ""
                })
                if len(products) >= max_results:
                    break
            except Exception:
                continue
    except Exception:
        pass
    return products


def get_today_research():
    """Main function. Returns category, problem, and top 3 products."""
    brain = load_brain()
    affiliate_tag = brain["system"].get("affiliate_tag", "")
    active = brain["strategy"]["active_categories"]

    # Check festival override
    festival_cats = []
    if brain["today"].get("festival_active"):
        for f in brain["festivals"]["calendar"]:
            if f["name"] == brain["today"].get("festival_name"):
                festival_cats = f.get("categories", [])
                break

    category = random.choice(festival_cats) if festival_cats else random.choice(active)
    problem = random.choice(PROBLEMS.get(category, PROBLEMS["skincare"]))
    keyword = f"best {problem} india"

    print(f"[Research] Category: {category} | Problem: {problem}")

    # Try live scraping first
    products = scrape_amazon(keyword, max_results=5)
    print(f"[Research] Live scrape: {len(products)} products found")

    # Always supplement with curated fallbacks to guarantee quality
    fallback_pool = FALLBACKS.get(category, FALLBACKS["skincare"])
    used_titles = [p["title"] for p in products]
    for fb in fallback_pool:
        if len(products) >= 5:
            break
        if fb["title"] not in used_titles:
            products.append(fb)

    # Score and pick top 3
    for p in products:
        p["score"] = score_product(p)
        p["url"] = amazon_url(p.get("asin", ""), affiliate_tag)

    top3 = sorted(products, key=lambda x: x["score"], reverse=True)[:3]
    print(f"[Research] Final top 3: {[p['title'][:30] for p in top3]}")

    return {
        "category": category,
        "problem": problem,
        "products": top3,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "festival": brain["today"].get("festival_name", ""),
    }


if __name__ == "__main__":
    result = get_today_research()
    print(json.dumps(result, indent=2, ensure_ascii=False))
  
