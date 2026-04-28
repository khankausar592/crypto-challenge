import json, re
from datetime import datetime

# ----------------------------
# Load scores safely
# ----------------------------
try:
    with open("scores.json") as f:
        scores = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    scores = {}

# ----------------------------
# Load result
# ----------------------------
with open("result.json") as f:
    result = json.load(f)

# ❌ Ignore invalid submissions
if not result.get("valid", False):
    print("Invalid submission. Skipping leaderboard update.")
    exit()

username = result["username"]
new_score = result["score"]

# ----------------------------
# Keep best score only
# ----------------------------
if username not in scores or new_score > scores[username]:
    scores[username] = new_score

# Save updated scores
with open("scores.json", "w") as f:
    json.dump(scores, f, indent=2)

# ----------------------------
# Build leaderboard
# ----------------------------
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

if sorted_scores:
    rows = "\n".join(
        f"| {i+1} | [{u}](https://github.com/{u}) | {round(s*100, 2)}% |"
        for i, (u, s) in enumerate(sorted_scores)
    )
else:
    rows = "| - | No submissions yet | - |"

table = f"""<!-- LEADERBOARD_START -->
## 🏆 Leaderboard
_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_

| Rank | Participant | Accuracy |
|------|-------------|----------|
{rows}
<!-- LEADERBOARD_END -->"""

# ----------------------------
# Update README safely
# ----------------------------
try:
    with open("README.md", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = ""

# If block doesn't exist → append it
if "<!-- LEADERBOARD_START -->" not in content:
    content += "\n\n" + table
else:
    content = re.sub(
        r"<!-- LEADERBOARD_START -->.*<!-- LEADERBOARD_END -->",
        table,
        content,
        flags=re.DOTALL
    )

with open("README.md", "w") as f:
    f.write(content)

print("Leaderboard updated successfully ✅")
