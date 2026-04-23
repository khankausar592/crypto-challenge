# simple baseline
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("C:\\Users\\Afifa\\crypto-challenge\\data\\train.csv")

X = df[['Close']]
y = df['Target']

model = LinearRegression()
model.fit(X, y)

test = pd.read_csv("../data/test.csv")
pred = model.predict(test[['Close']])

pd.DataFrame({
    "id": test['id'],
    "prediction": pred
}).to_csv("../submissions/sample_submission.csv", index=False)
