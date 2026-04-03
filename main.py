"""
main.py - SheValue AI v2
Master controller. Simple. Clear. Easy to debug.
Usage: python main.py [morning | evening]
"""

import sys, os, json, traceback
from datetime import datetime

from research import get_today_research
from write import write_today
from design import generate_image
from post import publish_all


def load_brain():
    with open("brain.json") as f:
        return json.load(f)


def check_keys():
    """Check which API keys are available."""
    keys = {
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "TELEGRAM_CHANNEL_ID": os.environ.get("TELEGRAM_CHANNEL_ID", ""),
        "BLOGGER_API_KEY": os.environ.get("BLOGGER_API_KEY", ""),
        "BLOGGER_BLOG_ID": os.environ.get("BLOGGER_BLOG_ID", ""),
        "IG_ACCESS_TOKEN": os.environ.get("IG_ACCESS_TOKEN", ""),
        "IG_BUSINESS_ACCOUNT_ID": os.environ.get("IG_BUSINESS_ACCOUNT_ID", ""),
    }
    print("\n[Main] API Key Status:")
    for name, val in keys.items():
        status = "✓ Set" if val else "✗ Missing"
        print(f"  {name}: {status}")

    if not keys["GEMINI_API_KEY"]:
        print("\n[Main] ERROR: GEMINI_API_KEY is required. Add it to GitHub Secrets.")
        sys.exit(1)
    print()


def run_morning():
    """Full daily pipeline: research → write → design → publish."""
    print("=" * 55)
    print(f"  SheValue AI - Morning Pipeline")
    print(f"  {datetime.now().strftime('%A, %d %B %Y - %I:%M %p IST')}")
    print("=" * 55)

    check_keys()

    try:
        # STEP 1: Research
        print("[Step 1/4] Researching today's topic...")
        research = get_today_research()
        print(f"  → Category: {research['category']}")
        print(f"  → Problem: {research['problem']}")
        print(f"  → Products: {len(research['products'])} found")

        # STEP 2: Write
        print("\n[Step 2/4] Writing honest review...")
        write_result = write_today(research)
        print(f"  → Headline: {write_result['headline']}")

        # STEP 3: Design
        print("\n[Step 3/4] Generating Instagram image...")
        image_path = generate_image({
            "headline": write_result["headline"],
            "category": research["category"],
            "slug": write_result["slug"],
            "products": research["products"],
        })
        print(f"  → Image: {image_path}")

        # STEP 4: Publish
        print("\n[Step 4/4] Publishing everywhere...")
        results = publish_all(write_result, image_path, research)

        print("\n" + "=" * 55)
        print("  ✅ DONE")
        print(f"  Post: {write_result['headline']}")
        published = [k for k, v in results.items() if v]
        print(f"  Published to: {', '.join(published) if published else 'files saved locally'}")
        print("=" * 55 + "\n")

    except Exception as e:
        print(f"\n[Main] ✗ Pipeline failed: {e}")
        print(traceback.format_exc())
        sys.exit(1)


def run_evening():
    """Evening learning pipeline."""
    from learn import run_evening_learning
    run_evening_learning()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    if mode == "morning":
        run_morning()
    elif mode == "evening":
        run_evening()
    else:
        print("Usage: python main.py [morning | evening]")
        sys.exit(1)
        
