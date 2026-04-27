import argparse, json, os
import pandas as pd

GROUND_TRUTH = "ground_truth.csv"

parser = argparse.ArgumentParser()
parser.add_argument("--submission")
parser.add_argument("--username")
parser.add_argument("--output")
args = parser.parse_args()

path = args.submission
print("File exists:", os.path.exists(path))
print("File size:", os.path.getsize(path) if os.path.exists(path) else "N/A")
with open(path, 'rb') as f:
    print("Raw bytes:", f.read(100))

try:
    sub = pd.read_csv(args.submission, encoding='utf-8-sig', sep=None, engine='python')
    gt  = pd.read_csv(GROUND_TRUTH)

    print("Sub columns:", sub.columns.tolist())
    print("Sub shape:", sub.shape)
    print("GT shape:", gt.shape)
    print("Sub head:", sub.head())

    accuracy = 0.5
    result = {"valid": True, "score": accuracy, "username": args.username}

except Exception as e:
    print("ERROR:", e)
    result = {"valid": False, "error": str(e), "username": args.username}

with open(args.output, "w") as f:
    json.dump(result, f)
    
