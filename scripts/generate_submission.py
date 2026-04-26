 # Participants run this
"""
Run this script to generate submission.csv
Usage: python scripts/generate_submission.py
"""

import sys
import os
import csv
from datetime import datetime

# Add parent directory to path so we can import template
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from template import predict_price

def get_github_username():
    """Try to get GitHub username from git config"""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    return "unknown_user"

def generate_submission():
    """Generate the submission CSV file"""
    
    # Get prediction from user's template
    try:
        prediction = predict_price()
        if not isinstance(prediction, (int, float)):
            raise ValueError(f"Prediction must be number, got {type(prediction)}")
    except Exception as e:
        print(f"❌ Error in your predict_price() function: {e}")
        sys.exit(1)
    
    # Get username
    username = get_github_username()
    
    # Create submission data
    submission_data = {
        'username': username,
        'prediction': prediction,
        'timestamp': datetime.now().isoformat(),
        'status': 'pending'
    }
    
    # Write to CSV
    with open('submission.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=submission_data.keys())
        writer.writeheader()
        writer.writerow(submission_data)
    
    print(f"✅ submission.csv created successfully!")
    print(f"   Username: {username}")
    print(f"   Prediction: ${prediction:,.2f}")
    print(f"\n📤 Next steps:")
    print(f"   1. git add submission.csv")
    print(f"   2. git commit -m 'Add my prediction'")
    print(f"   3. git push")
    print(f"   4. Open a Pull Request")

if __name__ == "__main__":
    generate_submission()
