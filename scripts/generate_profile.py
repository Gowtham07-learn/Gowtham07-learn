import os
import urllib.request
from collections import Counter
from datetime import datetime, timezone

USERNAME = "Gowtham07-learn"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "gowtham-profile-generator",
            "Authorization": f"Bearer {TOKEN}",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return __import__("json").load(response)

def esc(value):
    return (str(value).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))

user = api(f"/users/{USERNAME}")
repos = api(f"/users/{USERNAME}/repos?per_page=100&sort=updated")

repo_count = user.get("public_repos", 0)
followers = user.get("followers", 0)
stars = sum(r.get("stargazers_count", 0) for r in repos)

languages = Counter()
for repo in repos:
    if not repo.get("fork") and repo.get("language"):
        languages[repo["language"]] += 1
top_languages = languages.most_common(5)

try:
    recent_events = len(api(f"/users/{USERNAME}/events/public?per_page=100"))
except Exception:
    recent_events = 0

cards = []
for (label, value), x in zip(
    [("REPOSITORIES", repo_count), ("FOLLOWERS", followers),
     ("STARS", stars), ("RECENT EVENTS", recent_events)],
    [70, 320, 570, 820]
):
    cards.append(
        f'<g><rect x="{x}" y="265" width="210" height="105" rx="16" fill="#111827" stroke="#263244"/>'
        f'<text x="{x+22}" y="300" fill="#94a3b8" font-family="Arial" font-size="13" font-weight="700">{esc(label)}</text>'
        f'<text x="{x+22}" y="345" fill="#f8fafc" font-family="Arial" font-size="30" font-weight="800">{esc(value)}</text></g>'
    )

langs = []
max_count = top_languages[0][1] if top_languages else 1
for i, (lang, count) in enumerate(top_languages):
    y = 450 + i * 34
    width = max(35, int(560 * count / max_count))
    langs.append(
        f'<text x="95" y="{y}" fill="#e5e7eb" font-family="Arial" font-size="15" font-weight="600">{esc(lang)}</text>'
        f'<rect x="255" y="{y-13}" width="560" height="12" rx="6" fill="#1f2937"/>'
        f'<rect x="255" y="{y-13}" width="{width}" height="12" rx="6" fill="#60a5fa"/>'
        f'<text x="840" y="{y}" fill="#94a3b8" font-family="Arial" font-size="13">{count} repos</text>'
    )

generated = datetime.now(timezone.utc).strftime("%d %b %Y")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="700" viewBox="0 0 1100 700">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#070b12"/>
<stop offset="100%" stop-color="#111827"/>
</linearGradient>
<filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity=".28"/></filter>
</defs>
<rect width="1100" height="700" rx="28" fill="url(#bg)"/>
<circle cx="1020" cy="70" r="130" fill="#1d4ed8" opacity=".12"/>
<circle cx="100" cy="620" r="170" fill="#0ea5e9" opacity=".08"/>

<text x="70" y="72" fill="#60a5fa" font-family="Arial" font-size="14" font-weight="800" letter-spacing="3">GITHUB PROFILE</text>
<text x="70" y="125" fill="#f8fafc" font-family="Arial" font-size="40" font-weight="800">Gowtham P</text>
<text x="70" y="160" fill="#cbd5e1" font-family="Arial" font-size="18">Computer Science Engineering • AI/ML • Full Stack • Real-time Systems</text>
<line x1="70" y1="195" x2="1030" y2="195" stroke="#263244"/>
<text x="70" y="235" fill="#94a3b8" font-family="Arial" font-size="14">Building intelligent applications, scalable backends and developer tools.</text>

<g filter="url(#shadow)">{''.join(cards)}</g>

<text x="70" y="415" fill="#f8fafc" font-family="Arial" font-size="18" font-weight="800">TOP LANGUAGES</text>
{''.join(langs)}

<text x="70" y="655" fill="#64748b" font-family="Arial" font-size="12">Updated automatically • {generated} • github.com/{USERNAME}</text>
</svg>"""

with open("assets/profile.svg", "w", encoding="utf-8") as f:
    f.write(svg)
