#!/usr/bin/env python3
"""Regenerate _data/commit_activity.json from ALL of the author's local git repos.

The homepage heatmap is baked (static JSON) because GitHub Pages CI only checks
out this one repo — it can't see the other projects. Run this locally whenever
you want the graph to reflect recent work, then commit the updated JSON:

    python3 tools/refresh-activity.py && git add _data/commit_activity.json

Edit AUTHOR_EMAILS / SCAN_ROOTS below if your identity or project layout changes.
"""
import json
import subprocess
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

AUTHOR_EMAILS = {
    "safishamsi98@gmail.com",
    "yayasafihas@gmail.com",
    "yayaalisafi997@gmail.com",
}
HOME = Path.home()
SCAN_ROOTS = [HOME / "projects", HOME / "school", HOME / "freelance",
              HOME / "dotfiles", HOME / "cv", HOME / "portfolio"]
EXCLUDE = ("node_modules", "vendor", "/reference/")
WEEKS = 53
OUT = Path(__file__).resolve().parent.parent / "_data" / "commit_activity.json"


def find_repos():
    repos = []
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for gitdir in root.glob("**/.git"):
            p = str(gitdir)
            if any(x in p for x in EXCLUDE):
                continue
            repos.append(gitdir.parent)
    return repos


def collect_dates(repos):
    counts = Counter()
    for repo in repos:
        try:
            out = subprocess.run(
                ["git", "-C", str(repo), "log", "--pretty=%ae|%ad", "--date=short"],
                capture_output=True, text=True, timeout=20).stdout
        except Exception:
            continue
        for line in out.splitlines():
            if "|" not in line:
                continue
            email, d = line.split("|", 1)
            if email.strip().lower() in AUTHOR_EMAILS:
                counts[d.strip()] += 1
    return counts


def level(c):
    if c == 0: return 0
    if c <= 2: return 1
    if c <= 5: return 2
    if c <= 9: return 3
    return 4


def main():
    counts = collect_dates(find_repos())
    today = date.today()
    start = today - timedelta(days=WEEKS * 7)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # snap to Sunday

    days, active, total = [], 0, 0
    d = start
    while d <= today:
        c = counts.get(d.isoformat(), 0)
        if c:
            active += 1
            total += c
        days.append({"date": d.isoformat(), "count": c, "level": level(c)})
        d += timedelta(days=1)

    OUT.write_text(json.dumps({"days": days, "total": total, "active_days": active}))
    print(f"wrote {OUT} — {total} commits across {active} active days, {len(days)} cells")


if __name__ == "__main__":
    main()
