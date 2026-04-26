import csv
import requests
import os
import json
from datetime import datetime

def get_actual_bitcoin_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return data['bitcoin']['usd']
    except:
        with open('data/historical_prices.csv', 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            return float(rows[-1]['price'])

if __name__ == "__main__":
    # Read submission
    with open('submission.csv', 'r') as f:
        reader = csv.DictReader(f)
        submission = list(reader)[0]
    
    prediction = float(submission['prediction'])
    username = submission['username']
    actual_price = get_actual_bitcoin_price()
    
    # Calculate accuracy
    absolute_error = abs(prediction - actual_price)
    percentage_error = (absolute_error / actual_price) * 100
    accuracy = round(max(0, 100 - percentage_error), 2)
    
    # SAVE TO A FILE THAT WILL PERSIST - THIS IS KEY!
    result_data = {
        'username': username,
        'prediction': prediction,
        'actual_price': actual_price,
        'accuracy': accuracy,
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Save as JSON
    with open('score_result.json', 'w') as f:
        json.dump(result_data, f)
    
    # Also save as CSV
    with open('score_result.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=result_data.keys())
        writer.writeheader()
        writer.writerow(result_data)
    
    # Save as GITHUB ENVIRONMENT VARIABLE for next workflow
    with open(os.environ['GITHUB_ENV'], 'a') as f:
        f.write(f"SCORE_USERNAME={username}\n")
        f.write(f"SCORE_ACCURACY={accuracy}\n")
        f.write(f"SCORE_PREDICTION={prediction}\n")
        f.write(f"SCORE_ACTUAL={actual_price}\n")
    
    print(f"accuracy={accuracy}%")
    print(f"✅ Score saved for {username}")
