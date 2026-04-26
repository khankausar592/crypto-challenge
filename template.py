 # Participants edit this
"""
CRYPTOCURRENCY PRICE PREDICTION TEMPLATE
Edit the predict_price() function below with your prediction logic
"""

def predict_price():
    """
    Your prediction logic goes here.
    
    You can:
    - Use historical data from data/historical_prices.csv
    - Use APIs (make sure they're free/no key needed)
    - Implement any ML model
    - Or just hardcode a number
    
    Returns:
        float: Your predicted Bitcoin price in USD
    """
    
    # ===== EDIT BELOW THIS LINE ===== #
    
    # TODO: Write your prediction logic here
    # Example simple prediction:
    predicted_price = 65000.00
    
    # ===== EDIT ABOVE THIS LINE ===== #
    
    return predicted_price


# Advanced example (uncomment to use):
# def predict_price():
#     import pandas as pd
#     df = pd.read_csv('data/historical_prices.csv')
#     last_price = df['price'].iloc[-1]
#     return last_price * 1.02  # 2% increase
