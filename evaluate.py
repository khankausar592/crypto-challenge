import argparse, json, pandas as pd

GROUND_TRUTH = "data/ground_truth.csv"

parser = argparse.ArgumentParser()
parser.add_argument("--submission")
parser.add_argument("--username")
parser.add_argument("--output")
args = parser.parse_args()

try:
    sub = pd.read_csv(args.submission)
    gt = pd.read_csv(GROUND_TRUTH)

    # ✅ Validation
    if list(sub.columns) != ["id", "prediction"]:
        raise ValueError("CSV must have columns: id,prediction")

    if len(sub) != len(gt):
        raise ValueError("Submission length does not match test set")

    if not sub["prediction"].isin([0,1]).all():
        raise ValueError("Predictions must be 0 or 1 only")

    # ✅ Accuracy
    accuracy = (sub["prediction"] == gt["Target"]).mean()

    result = {
        "valid": True,
        "score": float(accuracy),
        "username": args.username
    }

except Exception as e:
    result = {
        "valid": False,
        "error": str(e),
        "username": args.username
    }

with open(args.output, "w") as f:
    json.dump(result, f)
