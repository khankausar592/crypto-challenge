# Checks if CSV is valid
"""
Validates the submission.csv file from a PR
Returns exit code 0 if valid, 1 if invalid
"""

import sys
import csv
import os

def validate_submission(filepath='submission.csv'):
    """Check if submission.csv is properly formatted"""
    
    if not os.path.exists(filepath):
        print(f"❌ Error: {filepath} not found")
        print("   Make sure you ran generate_submission.py and committed the file")
        return False
    
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if len(rows) != 1:
                print(f"❌ Error: Expected 1 row, got {len(rows)}")
                return False
            
            row = rows[0]
            
            # Check required fields
            required_fields = ['username', 'prediction']
            for field in required_fields:
                if field not in row:
                    print(f"❌ Error: Missing '{field}' column")
                    return False
            
            # Check prediction is a number
            try:
                prediction = float(row['prediction'])
                if prediction <= 0:
                    print(f"❌ Error: Prediction must be positive")
                    return False
            except ValueError:
                print(f"❌ Error: Prediction must be a number, got '{row['prediction']}'")
                return False
            
            print(f"✅ Submission valid!")
            print(f"   Username: {row['username']}")
            print(f"   Prediction: ${prediction:,.2f}")
            return True
            
    except Exception as e:
        print(f"❌ Error reading submission.csv: {e}")
        return False

if __name__ == "__main__":
    if validate_submission():
        sys.exit(0)
    else:
        sys.exit(1)
