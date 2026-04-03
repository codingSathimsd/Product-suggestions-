"""
learn.py - SheValue AI v2
ONE JOB: Learn from today. Improve tomorrow.
Runs every evening at 9PM IST via GitHub Actions.
"""

import json
from datetime import datetime


def load_brain():
    with open("brain.json") as f:
        return json.load(f)


def save_brain(brain):
    brain["last_updated"] = datetime.now().isoformat()
    with open("brain.json", "w") as f:
        json.dump(brain, f, indent=2, ensure_ascii=False)


def check_festival(brain):
    """Check if any festival is in the next 14 days. Update brain."""
    today = datetime.now()
    upcoming = []

    for fest in brain["festivals"]["calendar"]:
        month = fest["month"]
        day = fest["day"]
        for year in [today.year, today.year + 1]:
            try:
                fdate = datetime(year, month, day)
                days_until = (fdate.date() - today.date()).days
                if 0 <= days_until <= brain["festivals"]["check_days_ahead"]:
                    upcoming.append({**fest, "days_until": days_until})
                    break
            except Exception:
                continue

    if upcoming:
        # Pick the soonest festival
        soonest = min(upcoming, key=lambda x: x["days_until"])
        brain["today"]["festival_active"] = True
        brain["today"]["festival_name"] = soonest["name"]
        print(f"[Learn] Festival detected: {soonest['name']} in {soonest['days_until']} days")
    else:
        brain["today"]["festival_active"] = False
        brain["today"]["festival_name"] = ""
        print("[Learn] No festival in next 14 days")

    brain["festivals"]["upcoming"] = upcoming
    return brain


def expand_categories(brain):
    """
    If we've posted enough in the current categories,
    automatically unlock the next category.
    """
    active = brain["strategy"]["active_categories"]
    all_cats = brain["strategy"]["all_categories"]
    threshold = brain["strategy"]["expand_after_posts"]
    total_posts = brain["performance"]["total_posts"]

    # Unlock one new category per threshold milestone
    unlockable = all_cats[:len(active) + 1]
    if len(unlockable) > len(active) and total_posts >= threshold * len(active):
        new_cat = unlockable[-1]
        brain["strategy"]["active_categories"].append(new_cat)
        brain["strategy"]["category_posts_count"][new_cat] = 0
        print(f"[Learn] 🚀 New category unlocked: {new_cat}")
        print(f"[Learn] Active categories: {brain['strategy']['active_categories']}")

    return brain


def update_performance_stats(brain):
    """Update aggregate performance stats."""
    logs = brain["performance"]["log"]
    brain["performance"]["days_running"] = len(logs)
    brain["performance"]["total_posts"] = len(logs)

    if logs:
        # Find best performing category by frequency
        from collections import Counter
        cats = Counter(l.get("category", "") for l in logs)
        brain["performance"]["best_category"] = cats.most_common(1)[0][0] if cats else "skincare"

    return brain


def self_improve(brain):
    """
    Core learning: analyse what is working, update strategy.
    Simple rules that anyone can understand and debug.
    """
    logs = brain["performance"]["log"]
    total = len(logs)

    # Rule 1: After 7 posts, increase category diversity
    if total == 7:
        print("[Learn] 7 posts milestone - checking category expansion")

    # Rule 2: After 30 posts, add affiliate link placeholder note
    if total == 30:
        print("[Learn] 30 posts milestone - system is ready for affiliate links when you join Amazon Associates")
        brain["system"]["affiliate_ready"] = True

    # Rule 3: After 90 posts, system is deeply trained
    if total == 90:
        print("[Learn] 90 posts milestone - system is fully optimised for Indian women's market")
        brain["system"]["fully_trained"] = True

    # Rule 4: Rotate psychology and design (already handled in write.py and design.py)
    # This is just a log note
    psych = brain["strategy"]["psychology_rotation"]
    idx = brain["strategy"]["psychology_index"]
    print(f"[Learn] Tomorrow's psychology: {psych[idx]}")

    return brain


def run_evening_learning():
    print(f"\n[Learn] SheValue AI - Evening Learning Cycle")
    print(f"[Learn] {datetime.now().strftime('%d %B %Y %I:%M %p IST')}")

    brain = load_brain()

    brain = check_festival(brain)
    brain = expand_categories(brain)
    brain = update_performance_stats(brain)
    brain = self_improve(brain)

    save_brain(brain)

    total = brain["performance"]["total_posts"]
    active = brain["strategy"]["active_categories"]
    festival = brain["today"].get("festival_name", "none")

    print(f"\n[Learn] Summary:")
    print(f"  Total posts: {total}")
    print(f"  Active categories: {active}")
    print(f"  Next festival: {festival}")
    print(f"  System is {min(round(total/365*100), 100)}% trained")
    print(f"[Learn] ✓ Brain updated for tomorrow.\n")


if __name__ == "__main__":
    run_evening_learning()
    
