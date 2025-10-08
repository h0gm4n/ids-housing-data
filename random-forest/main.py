import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error, root_mean_squared_error
import joblib
import numpy as np
from sklearn.preprocessing import TargetEncoder
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
def linear_model(x, a, b):
    return a * x + b

#df = pd.read_csv('housingdata/src/backend/american_housing_data.csv')
df = pd.read_parquet('random-forest/CleanData.parquet')

df = df[df['City'] == 'Helsinki']

post_code = df['PostCode']
living_area = df['Size']
price = df['Price']


# Normalize living_area to between 0 and 1
living_area_min = living_area.min()
living_area_max = living_area.max()
living_area = (living_area - living_area_min) / (living_area_max - living_area_min)

price_min = price.min()
price_max = price.max()
price = (price - price_min) / (price_max - price_min)

# Save normalization parameters
normalization_params = {
    'living_area_min': living_area_min,
    'living_area_max': living_area_max,
    'price_min': price_min,
    'price_max': price_max
}
print(f'Living area min: {living_area_min}, max: {living_area_max}')
print(f'Price min: {price_min}, max: {price_max}')


correlation_vars = pd.DataFrame({
    'Price': price,
    'Living Space': living_area,
    'PostCode': post_code,
})

#random forest parameters:
# predicted variable: price
# predictors: living space, beds, baths, zip code

X = correlation_vars[['PostCode', 'Living Space']]
y = correlation_vars['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# encoder = TargetEncoder()
# X_train['Zip Code'] = encoder.fit_transform(X_train[['Zip Code']], y_train)
# X_test['Zip Code'] = encoder.transform(X_test[['Zip Code']])

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(X_train.head())

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
R2 = r2_score(y_test, y_pred)
MAPE = mean_absolute_percentage_error(y_test, y_pred)
RMSE = root_mean_squared_error(y_test, y_pred)

print(f'MAPE: {MAPE}')
print(f'RMSE: {RMSE}')
print(f'R^2: {R2}')
print(f'Mean Squared Error: {mse}')

model_data = {
    'model': model,
    'normalization_params': normalization_params
}
joblib.dump(model_data, 'housingdata/src/backend/random_forest_model.pkl')
print("Model and normalization parameters saved to 'random_forest_model.pkl'")


#model for predicting living area

model_living_area = RandomForestRegressor(n_estimators=100, random_state=42)
X_la = correlation_vars[['PostCode', 'Price']]
y_la = correlation_vars['Living Space']
X_train_la, X_test_la, y_train_la, y_test_la = train_test_split(X_la, y_la, test_size=0.2, random_state=42)
model_living_area.fit(X_train_la, y_train_la)
y_pred_la = model_living_area.predict(X_test_la)
mse_la = mean_squared_error(y_test_la, y_pred_la)
R2_la = r2_score(y_test_la, y_pred_la)
MAPE_la = mean_absolute_percentage_error(y_test_la, y_pred_la)
RMSE_la = root_mean_squared_error(y_test_la, y_pred_la)
print(f'Living Area Model - MAPE: {MAPE_la}')
print(f'Living Area Model - RMSE: {RMSE_la}')
print(f'Living Area Model - R^2: {R2_la}')
print(f'Living Area Model - Mean Squared Error: {mse_la}')
model_data_la = {
    'model': model_living_area,
    'normalization_params_la': normalization_params
}
joblib.dump(model_living_area, 'housingdata/src/backend/random_forest_model_living_area.pkl')

#predict the price of a house with 2000 sqft, 3 beds, 2 baths, zip code 10036
# Save the trained model to a file
# Save the trained model and normalization parameters to a file

plt.scatter(price, living_area, color='blue', label='Data points')
plt.scatter(price, model.predict(X), color='red', label='Random Forest Predictions', alpha=0.5)
plt.xlabel('Normalized Price')
plt.ylabel('Normalized Living Area')
plt.title('Random Forest Regression: Price vs Living Area')
plt.legend()
plt.show()

plt.scatter(price, living_area, color='blue', label='Data points')
plt.scatter(price, model_living_area.predict(X_la), color='green', label='Living Area Predictions', alpha=0.5)
plt.xlabel('Normalized Price')
plt.ylabel('Normalized Living Area')
plt.title('Random Forest Regression: Price vs Living Area')
plt.legend()
plt.show()