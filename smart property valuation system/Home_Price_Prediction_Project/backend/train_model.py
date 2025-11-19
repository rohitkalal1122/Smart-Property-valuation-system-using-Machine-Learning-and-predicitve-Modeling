import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('../data/house_data.csv')
X = df[['SqFt','Bedrooms','Bathrooms','YearBuilt','WalkIndex','RiskScore']]
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

pickle.dump(model, open('home_price_model.pkl', 'wb'))
print("Model trained and saved!")