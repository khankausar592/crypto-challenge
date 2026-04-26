#!/usr/bin/env python3
import csv
import os
import glob
import json
from datetime import datetime

def update_leaderboard():
    scores = []
    
    # Look for downloaded score data
    score_files = glob.glob('.score-data/score_*.csv')
    score_files.extend(glob.glob('score_result.csv'))
    
    for score_file in score_files:
        if os.path.exists(score_file):
            with open(score_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    scores.append(row)
                    print(f"Found: {row.get('username')} - {row.get('accuracy')}%")
    
    # Also check JSON
    json_files = glob.glob('.score-data/score_*.json')
    json_files.extend(glob.glob('score_result.json'))
    
    for json_file in json_files:
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                scores.append(data)
                print(f"Found JSON: {data.get('username')} - {data.get('accuracy')}%")
    
    if not scores:
        print("No scores found, skipping...")
        return
    
    # Group by username, keep best score
    best_scores = {}
    for score in scores:
        username = score.get('username')
        accuracy = float(score.get('accuracy', 0))
        
        if username not in best_scores or accuracy > best_scores[username]['accuracy']:
            best_scores[username] = {
                'username': username,
                'prediction': float(score.get('prediction', 0)),
                'actual_price': float(score.get('actual_price', 0)),
                'accuracy': accuracy,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
    
    # Sort and write leaderboard
    sorted_users = sorted(best_scores.values(), key=lambda x: x['accuracy'], reverse=True)
    
    with open('leaderboard.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Username', 'Prediction', 'Actual Price', 'Accuracy %', 'Date'])
        
        for rank, user in enumerate(sorted_users, 1):
            writer.writerow([
                rank,
                user['username'],
                f"${user['prediction']:,.2f}",
                f"${user['actual_price']:,.2f}",
                f"{user['accuracy']}%",
                user['date']
            ])
    
    print(f"\n✅ Updated leaderboard with {len(sorted_users)} participants")

if __name__ == "__main__":
    update_leaderboard()
