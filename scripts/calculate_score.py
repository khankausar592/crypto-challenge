
---

## 🔧 Updated Evaluation Metrics Code

Here's the **updated `scripts/calculate_score.py`** with all metrics:

```python
"""
Calculates comprehensive prediction metrics including:
- Accuracy score
- Absolute error
- Percentage error
- Direction accuracy
- Confidence score (if provided)
"""

import csv
import requests
import sys
import os
import json
from datetime import datetime

def get_actual_bitcoin_price():
    """Get real Bitcoin price from free API"""
    try:
        # CoinGecko free API (no key needed)
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
        # Fallback to historical
        return get_latest_historical_price()

def get_latest_historical_price():
    """Fallback to historical data"""
    try:
        with open('data/historical_prices.csv', 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            last_row = rows[-1]
            return float(last_row['price'])
    except:
        return 50000

def get_previous_price():
    """Get previous day's price for direction calculation"""
    try:
        with open('data/historical_prices.csv', 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if len(rows) >= 2:
                return float(rows[-2]['price'])
            else:
                return float(rows[-1]['price'])
    except:
        return 50000

def calculate_accuracy_metrics(prediction, actual):
    """Calculate all accuracy metrics"""
    
    # 1. Absolute Error
    absolute_error = abs(prediction - actual)
    
    # 2. Percentage Error
    percentage_error = (absolute_error / actual) * 100
    
    # 3. Accuracy Score (inverse of percentage error, capped at 100)
    accuracy = max(0, 100 - percentage_error)
    
    # 4. Direction Accuracy (check if predicted direction matches actual)
    # Note: For this to work, we need to know if price went up/down
    # We'll use previous day's price as baseline
    
    return {
        'accuracy': round(accuracy, 2),
        'absolute_error': round(absolute_error, 2),
        'percentage_error': round(percentage_error, 2),
        'prediction': prediction,
        'actual': actual
    }

def calculate_direction_accuracy(prediction, actual, previous_price):
    """Determine if predicted direction was correct"""
    
    actual_direction = "up" if actual > previous_price else "down" if actual < previous_price else "flat"
    predicted_direction = "up" if prediction > previous_price else "down" if prediction < previous_price else "flat"
    
    is_correct = (actual_direction == predicted_direction)
    
    return {
        'actual_direction': actual_direction,
        'predicted_direction': predicted_direction,
        'correct': is_correct
    }

def calculate_confidence_score(prediction, actual, absolute_error):
    """Calculate confidence based on historical error patterns"""
    # Simple confidence: inverse of error percentage (capped)
    error_rate = absolute_error / actual
    confidence = max(0, min(100, (1 - error_rate) * 100))
    return round(confidence, 2)

def get_rank(accuracy, all_scores=None):
    """Calculate approximate rank based on accuracy"""
    if accuracy >= 95:
        return "🏆 Top Tier"
    elif accuracy >= 85:
        return "🥇 Gold Tier"
    elif accuracy >= 75:
        return "🥈 Silver Tier"
    elif accuracy >= 60:
        return "🥉 Bronze Tier"
    else:
        return "📚 Learning Tier"

def get_recommendation(metrics):
    """Generate improvement recommendations"""
    recommendations = []
    
    if metrics['percentage_error'] > 20:
        recommendations.append("Consider using moving averages to reduce error")
    if metrics['accuracy'] < 70:
        recommendations.append("Try analyzing longer historical trends")
    if metrics['absolute_error'] > 10000:
        recommendations.append("Bitcoin is volatile - consider using volatility indicators")
    
    if not recommendations:
        recommendations.append("Great job! Consider adding technical indicators for even better accuracy")
    
    return recommendations

def score_submission():
    """Main scoring function with all metrics"""
    
    # Read submission
    submission_file = 'submission.csv'
    if not os.path.exists(submission_file):
        print("❌ Error: submission.csv not found")
        return None
    
    with open(submission_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if len(rows) == 0:
            print("❌ Error: submission.csv is empty")
            return None
        submission = rows[0]
    
    try:
        prediction = float(submission['prediction'])
        username = submission['username']
    except (KeyError, ValueError) as e:
        print(f"❌ Error reading submission: {e}")
        return None
    
    # Get actual price and previous price
    actual_price = get_actual_bitcoin_price()
    previous_price = get_previous_price()
    
    # Calculate all metrics
    metrics = calculate_accuracy_metrics(prediction, actual_price)
    direction = calculate_direction_accuracy(prediction, actual_price, previous_price)
    confidence = calculate_confidence_score(prediction, actual_price, metrics['absolute_error'])
    rank_tier = get_rank(metrics['accuracy'])
    recommendations = get_recommendation(metrics)
    
    # Format numbers for display
    def format_currency(value):
        return f"${value:,.2f}"
    
    # Print detailed results (what the bot will show)
    print("\n" + "="*60)
    print("📊 PREDICTION EVALUATION RESULTS")
    print("="*60)
    
    print(f"\n👤 Participant: {username}")
    print(f"📅 Evaluation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    print(f"\n🎯 PRICE COMPARISON:")
    print(f"   Your prediction: {format_currency(prediction)}")
    print(f"   Actual price:    {format_currency(actual_price)}")
    print(f"   Difference:      {format_currency(metrics['absolute_error'])}")
    
    print(f"\n📈 ACCURACY METRICS:")
    print(f"   • Accuracy Score:     {metrics['accuracy']}%")
    print(f"   • Percentage Error:   {metrics['percentage_error']}%")
    print(f"   • Absolute Error:     {format_currency(metrics['absolute_error'])}")
    
    print(f"\n🧭 DIRECTION ANALYSIS:")
    print(f"   • Actual direction:   {direction['actual_direction'].upper()}")
    print(f"   • Your direction:     {direction['predicted_direction'].upper()}")
    print(f"   • Direction correct?  {'✅ YES' if direction['correct'] else '❌ NO'}")
    
    print(f"\n⭐ CONFIDENCE SCORE: {confidence}%")
    print(f"   (Based on historical accuracy patterns)")
    
    print(f"\n🏅 RANK TIER: {rank_tier}")
    
    print(f"\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Calculate bonus points (optional features)
    bonus_points = 0
    if 'confidence_interval' in submission:
        bonus_points += 5
        print(f"\n🎁 BONUS: +5 points for providing confidence interval!")
    
    # Final score (0-100 + bonus)
    final_score = metrics['accuracy'] + bonus_points
    final_score = min(100, final_score)  # Cap at 100
    
    print(f"\n🏆 FINAL SCORE: {final_score:.2f}/100")
    print("="*60)
    
    # Save detailed results to CSV
    result_data = {
        'username': username,
        'prediction': prediction,
        'actual_price': actual_price,
        'accuracy': metrics['accuracy'],
        'absolute_error': metrics['absolute_error'],
        'percentage_error': metrics['percentage_error'],
        'direction_correct': direction['correct'],
        'confidence_score': confidence,
        'rank_tier': rank_tier,
        'final_score': final_score,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('score_result.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=result_data.keys())
        writer.writeheader()
        writer.writerow(result_data)
    
    # Also save as JSON for bot to use
    with open('score_result.json', 'w') as f:
        json.dump(result_data, f, indent=2)
    
    return final_score

if __name__ == "__main__":
    try:
        score = score_submission()
        if score is not None:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
