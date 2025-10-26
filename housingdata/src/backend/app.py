from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
import joblib
import pandas as pd
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
app = Flask(__name__, static_folder=BUILD_DIR, static_url_path="/")
CORS(app)

df = pd.read_parquet('src/backend/etuovi_vFINAL.parquet')
df = df.rename(columns={'postcode': 'PostCode', 'searchPrice': 'Price', 'area': 'Size'})
model_data = joblib.load('src/backend/random_forest_model.pkl')
model_data_la = joblib.load('src/backend/random_forest_model_living_area.pkl')
print(model_data)
model = model_data['model']

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/predict', methods=['POST'])
def test_function():
    data = request.get_json()
    postal_code = data.get('postalCode')
    living_space = data.get('livingSpace')
    apartment_price = data.get('apartmentPrice')
    print(f"postalCode: {postal_code}, livingSpace: {living_space}, apartmentPrice: {apartment_price}")


    normalization_params = model_data['normalization_params']
    print(f"Normalization params: {normalization_params}")
    # Get normalization parameters instead of hardcoding
    living_area_min = normalization_params['living_area_min']
    living_area_max = normalization_params['living_area_max']
    price_min = normalization_params['price_min']
    price_max = normalization_params['price_max']
    living_space_norm = (float(living_space) - living_area_min) / (living_area_max - living_area_min)
    apartment_price_norm = (float(apartment_price) - price_min) / (price_max - price_min)


    predicted_price = predict_price(postal_code, living_space_norm)
    predicted_living_space = predict_living_space(postal_code, float(apartment_price_norm))
    print('given apartment price:')
    get_typical_house(postal_code, float(apartment_price))

    #remove normalization
    #these variables should be gotten from the model, not hardcoded

    print('normalization params:')
    print(normalization_params)
    predicted_price = predicted_price * (price_max - price_min) + price_min
    predicted_living_space = predicted_living_space * (living_area_max - living_area_min) + living_area_min
    print(f"Predicted Price: {predicted_price}")
    print(f"Postal Code: {postal_code}, Living Space: {living_space}")
    print(f"Predicted Living Space for given price: {predicted_living_space}")

    #use these functions to get the house ID and link to the house 
    #that is most similar to the predicted house from the users input
    closest_house_id = get_closest_house(predicted_price, postal_code, living_space)
    link = make_link(closest_house_id) if closest_house_id else None
    print(link)

    result = {"predicted_price": predicted_price,
              "predicted_living_space": predicted_living_space,
              "given_postal_code": postal_code,
              "given_living_space": living_space,
              "given_apartment_price": apartment_price,
              "apartment_link": link}
    
    return jsonify(result)

def predict_price(postal_code, living_space):

    # Make a prediction
    feature_names = ['PostCode', 'Living Space']
    input_data = pd.DataFrame([[postal_code, living_space]], columns=feature_names)
    prediction = model.predict(input_data)
    return prediction[0]

def predict_living_space(postal_code, price):

    # Make a prediction
    feature_names = ['PostCode', 'Price']
    input_data = pd.DataFrame([[postal_code, price]], columns=feature_names)
    prediction = model_data_la.predict(input_data)
    print('non normalized living area prediction')
    print(prediction)
    return prediction[0]


def get_typical_house(postal_code, price):
    # see what you can get in this area for the price that the user gave
    df_area = df[df['PostCode'].astype(str).str.startswith(str(postal_code))]

    price_lower = price * 0.95
    price_upper = price * 1.05
    df_filtered = df_area[(df_area['Price'] >= price_lower) & (df_area['Price'] <= price_upper)]
    living_space = df_filtered['Size'].mean()
    median_price = df_filtered['Price'].median()
    print(f"Typical house in area for given price: Living Space: {living_space}, Median Price: {median_price}")

    return

def get_closest_house(price, postal_code, living_space):
    # find the closest house in the dataset to the given parameters
    df_area = df[df['PostCode'].astype(str).str.startswith(str(postal_code))]
    df_area['PriceDiff'] = (df_area['Price'] - float(price)).abs()
    df_area['LivingSpaceDiff'] = (df_area['Size'] - float(living_space)).abs()
    df_area['TotalDiff'] = df_area['PriceDiff'] + df_area['LivingSpaceDiff']
    closest_house = df_area.loc[df_area['TotalDiff'].idxmin()]
    house_id = closest_house['friendlyId']
    print(f"House ID: {house_id}")
    return house_id



def make_link(id):
    return f'https://www.etuovi.com/kohde/{id}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)