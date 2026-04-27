import argparse, json
import pandas as pd

GROUND_TRUTH = "ground_truth.csv"

parser = argparse.ArgumentParser()
parser.add_argument("--submission")
parser.add_argument("--username")
parser.add_argument("--output")
args = parser.parse_args()

try:
    sub = pd.read_csv(args.submission, encoding='utf-8-sig', sep=None, engine='python')
    gt  = pd.read_csv(GROUND_TRUTH)

    print("Columns:", sub.columns.tolist())
    print("Shape:", sub.shape)
    print("Head:", sub.head())

    assert list(sub.columns) == ["id", "prediction"], "Columns must be: id, prediction"
    assert len(sub) == len(gt), f"Expected {len(gt)} rows, got {len(sub)}"
    assert set(sub["id"]) == set(gt["id"]), "Row IDs don't match"

    sub = sub.sort_values("id")
    gt  = gt.sort_values("id")

    correct = (sub["prediction"].values == gt["label"].values).sum()
    accuracy = round(correct / len(gt), 4)

    result = {"valid": True, "score": accuracy, "username": args.username}

except Exception as e:
    result = {"valid": False, "error": str(e), "username": args.username}

with open(args.output, "w") as f:
    json.dump(result, f)
