# Rebuilds leaderboard
"""
Updates the master leaderboard with all submissions
"""

import csv
import os
import glob
from datetime import datetime

def update_leaderboard():
    """Collect all scores and create sorted leaderboard"""
    
    # Store all submissions
    all_submissions = []
    
    # Look for score_result.csv from each run
    score_files = glob.glob('score_result_*.csv')
    
    # Also check main score_result.csv
    if os.path.exists('score_result.csv'):
        score_files.append('score_result.csv')
    
    # Read all score files
    for score_file in score_files:
        try:
            with open(score_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_submissions.append(row)
        except:
            pass
    
    # Check submissions folder for historical data
    submission_files = glob.glob('submissions/*.csv')
    for sub_file in submission_files:
        try:
            with open(sub_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # If it has accuracy, add it
                    if 'accuracy' in row:
                        all_submissions.append(row)
        except:
            pass
    
    # Remove duplicates (keep highest accuracy for each user)
    user_best = {}
    for sub in all_submissions:
        username = sub['username']
        accuracy = float(sub['accuracy'])
        
        if username not in user_best or accuracy > user_best[username]['accuracy']:
            user_best[username] = {
                'username': username,
                'prediction': float(sub['prediction']),
                'actual_price': float(sub.get('actual_price', 0)),
                'accuracy': accuracy,
                'best_date': datetime.now().strftime('%Y-%m-%d')
            }
    
    # Sort by accuracy (highest first)
    sorted_users = sorted(user_best.values(), key=lambda x: x['accuracy'], reverse=True)
    
    # Write leaderboard with ranks
    with open('leaderboard.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Username', 'Prediction', 'Actual Price', 'Accuracy %', 'Date'])
        
        for rank, user in enumerate(sorted_users, 1):
            writer.writerow([
                rank,
                user['username'],
                f"${user['prediction']:,.2f}",
                f"${user['actual_price']:,.2f}",
                user['accuracy'],
                user['best_date']
            ])
    
    print(f"✅ Leaderboard updated with {len(sorted_users)} participants")
    
    # Print top 5
    print("\n🏆 TOP 5 LEADERBOARD 🏆")
    for i, user in enumerate(sorted_users[:5], 1):
        print(f"{i}. {user['username']}: {user['accuracy']}%")

if __name__ == "__main__":
    update_leaderboard()
