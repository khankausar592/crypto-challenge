import argparse, json, pandas as pd
from sklearn.metrics import f1_score  # or whatever metric fits your task

GROUND_TRUTH = "ground_truth.csv"   # kept private or in a secret path

parser = argparse.ArgumentParser()
parser.add_argument("--submission")
parser.add_argument("--username")
parser.add_argument("--output")
args = parser.parse_args()

try:
    sub = pd.read_csv(args.submission)
    gt  = pd.read_csv(GROUND_TRUTH)

    assert list(sub.columns) == ["id", "prediction"], "Wrong columns"
    assert len(sub) == len(gt), "Wrong number of rows"

    score = round(f1_score(gt["label"], sub["prediction"].round()), 4)
    result = {"valid": True, "score": score}

except Exception as e:
    result = {"valid": False, "error": str(e)}

with open(args.output, "w") as f:
    json.dump(result, f)
