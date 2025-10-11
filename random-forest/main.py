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
def strip(string):
    return string.lstrip('0')
#df = pd.read_csv('housingdata/src/backend/american_housing_data.csv')
df = pd.read_parquet('random-forest/CleanData.parquet')

df = df[df['City'] == 'Helsinki']

df = df[df['Price'] > 70000]  # Remove entries with price less than 70,000g
df['PostCodeStripped'] = df['PostCode'].str.lstrip('0').fillna(value='0')
df['PostCodeStripped'] = pd.to_numeric(df['PostCodeStripped'], errors='coerce').fillna(0).astype(int)
#df = df[df['PostCodeStripped'] < 150]  # Remove entries with
post_code = df['PostCode']
living_area = df['Size']
price = df['Price']


# Normalize living_area to between 0 and 1
living_area_min = living_area.min()
living_area_max = living_area.max()
living_area_norm = (living_area - living_area_min) / (living_area_max - living_area_min)

price_min = price.min()
price_max = price.max()
price_norm = (price - price_min) / (price_max - price_min)

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
    'Price': price_norm,
    'Living Space': living_area_norm,
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


plt.scatter(price, model.predict(X)* (price_max - price_min) + price_min, color='red', label='Random Forest Predictions', alpha=0.5, facecolors='none', edgecolors='g', s=3)
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.legend()
plt.savefig('random_forest_price_vs_price.png', dpi=300)
plt.clf()

plt.scatter(living_area, model_living_area.predict(X_la)* (living_area_max - living_area_min) + living_area_min, color='red', label='Random Forest Predictions', alpha=0.5, facecolors='none', edgecolors='g', s=3)
plt.xlabel('Actual Living Area')
plt.ylabel('Predicted Living Area')
plt.legend()
plt.title('Random Forest Regression: Living Area vs Price')
plt.legend()
plt.savefig('random_forest_living_area.png', dpi=300)

# Get all houses where predicted price > actual price
predicted_prices = model.predict(X) * (price_max - price_min) + price_min
actual_prices = price

above_actual_mask = predicted_prices > actual_prices * 1.5
houses_above_actual = df[above_actual_mask]



def get_deals(threshold=1.5):
    above_actual_mask = predicted_prices > actual_prices * threshold
    houses_above_actual = df[above_actual_mask]
    houses_above_actual['Deviation'] = predicted_prices[above_actual_mask] - actual_prices[above_actual_mask]
    houses_sorted = houses_above_actual.sort_values(by='Deviation', ascending=False)
    #row numbers for top 10 deals
    rows = houses_sorted.head(10).index
    ids = df.loc[rows, 'Id']
    print(houses_sorted.head())
    return houses_sorted[['Price', 'Size', 'PostCode', 'Deviation']]

def make_link(id):
    return f'https://www.etuovi.com/kohde/{id}'

get_deals()


#{"addressLine2": "Taka-Töölö Helsinki",
#  "location": "Mechelininkatu 34b Taka-Töölö Helsinki",
#  "constructionFinishedYear": 2001,
#  "searchPrice": 924000,
#  "price": null,
#  "roomCount": "THREE_ROOMS",
#  "area": 109,
#  "totalArea": 109,
#  "id": 2340469,
#  "friendlyId": "37599385"}