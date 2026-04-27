import json, re
from datetime import datetime

# Load existing scores
try:
    with open("scores.json") as f:
        scores = json.load(f)
except FileNotFoundError:
    scores = {}

# Load new result
with open("result.json") as f:
    result = json.load(f)

username = result["username"]
new_score = result["score"]

# Keep only best score
if username not in scores or new_score > scores[username]:
    scores[username] = new_score

with open("scores.json", "w") as f:
    json.dump(scores, f, indent=2)

# Build leaderboard table
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

rows = "\n".join(
    f"| {i+1} | [{u}](https://github.com/{u}) | {round(s*100, 2)}% |"
    for i, (u, s) in enumerate(sorted_scores)
)

table = f"""<!-- LEADERBOARD_START -->
## Leaderboard
_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_

| Rank | Participant | Accuracy |
|------|-------------|----------|
{rows}
<!-- LEADERBOARD_END -->"""

with open("README.md", "r") as f:
    content = f.read()

updated = re.sub(
    r"<!-- LEADERBOARD_START -->.*<!-- LEADERBOARD_END -->",
    table,
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(updated)
