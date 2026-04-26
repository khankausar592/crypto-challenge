# Scores the prediction
"""
Calculates accuracy score by comparing prediction to actual price
"""

import csv
import requests
import sys
import os

def get_actual_bitcoin_price():
    """Get real Bitcoin price from free API"""
    try:
        # Using CoinGecko free API (no key needed)
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        actual_price = data['bitcoin']['usd']
        return actual_price
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch live price: {e}")
        # Fallback to latest historical price
        return get_latest_historical_price()

def get_latest_historical_price():
    """Fallback: use historical data"""
    try:
        with open('data/historical_prices.csv', 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            last_row = rows[-1]
            return float(last_row['price'])
    except:
        return 50000  # Default fallback

def calculate_accuracy(prediction, actual):
    """Calculate accuracy percentage (100% = perfect prediction)"""
    difference = abs(prediction - actual)
    error_percentage = (difference / actual) * 100
    accuracy = max(0, 100 - error_percentage)
    return round(accuracy, 2)

def score_submission():
    """Main scoring function"""
    
    # Read submission
    submission_file = 'submission.csv'
    if not os.path.exists(submission_file):
        print("Error: submission.csv not found")
        return None
    
    with open(submission_file, 'r') as f:
        reader = csv.DictReader(f)
        submission = list(reader)[0]
    
    prediction = float(submission['prediction'])
    username = submission['username']
    
    # Get actual price
    actual_price = get_actual_bitcoin_price()
    
    # Calculate accuracy
    accuracy = calculate_accuracy(prediction, actual_price)
    
    # Save score
    score_data = {
        'username': username,
        'prediction': prediction,
        'actual_price': actual_price,
        'accuracy': accuracy,
        'timestamp': submission.get('timestamp', '')
    }
    
    # Write score to output
    with open('score_result.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=score_data.keys())
        writer.writeheader()
        writer.writerow(score_data)
    
    print(f"📊 Scoring Results:")
    print(f"   Username: {username}")
    print(f"   Your prediction: ${prediction:,.2f}")
    print(f"   Actual price: ${actual_price:,.2f}")
    print(f"   Accuracy: {accuracy}%")
    
    return accuracy

if __name__ == "__main__":
    accuracy = score_submission()
    if accuracy:
        sys.exit(0)
    else:
        sys.exit(1)
