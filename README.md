<!-- LEADERBOARD_START -->
## 🏆 Leaderboard

_No submissions yet_
<!-- LEADERBOARD_END -->

## 💡 Tips
- Try feature engineering — moving averages, RSI, price momentum
- The dataset is time-series — be careful not to use future data while training
- A simple baseline: always predict `1` (price goes up) — beat that first!
# 🪙 Crypto Price Prediction Challenge

Predict whether Bitcoin's price will go **UP or DOWN** the next day.  
This is a binary classification problem — your model outputs `1` (price goes up) or `0` (price goes down).

---

## 📊 Dataset

| File | Description |
|------|-------------|
| `train.csv` | Historical Bitcoin data with labels — use this to train your model |
| `test_features.csv` | Test set without labels — predict on this and submit |
| `sample_submission.csv` | Example of the correct submission format |

**Features available:** `Date`, `Open`, `High`, `Low`, `Close`, `Volume`
**Target:** Will the closing price be higher tomorrow? `1 = Yes`, `0 = No`

---

## 🚀 How to Participate

### Step 1 — Fork this repo
Click the **Fork** button at the top right of this page.

### Step 2 — Train your model
Use `train.csv` to build any model you like — logistic regression, random forest, LSTM, anything goes.

### Step 3 — Generate predictions
Run your model on `test_features.csv` and save predictions as a CSV with exactly two columns:

```csv
id,prediction
0,1
1,0
2,1
...
```

### Step 4 — Save your file
Save your predictions as `submissions/<your_github_username>.csv` inside the repo.  
For example if your username is `john123`, save it as `submissions/john123.csv`.

### Step 5 — Open a Pull Request
Open a PR to this repo. A bot will automatically:
- Validate your CSV format
- Calculate your accuracy score
- Post the result as a comment on your PR

### Step 6 — Resubmissions
Not happy with your score? Close the PR, update your CSV, and open a new one.  
Only your **best score** is kept on the leaderboard.

---

## 📏 Evaluation

Submissions are scored using **accuracy**:
