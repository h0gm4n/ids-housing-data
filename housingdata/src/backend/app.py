from flask import Flask, request
from flask_cors import CORS
import joblib
import pandas as pd
app = Flask(__name__)
CORS(app)

df = pd.read_csv('american_housing_data.csv')
zip_code = df['Zip Code']

@app.route('/', methods=['POST'])
def test_function():
    data = request.get_json()
    postal_code = data.get('postalCode')
    living_space = data.get('livingSpace')
    apartment_price = data.get('apartmentPrice')
    print(f"postalCode: {postal_code}, livingSpace: {living_space}, apartmentPrice: {apartment_price}")

    if int(postal_code) not in zip_code.values:
        # Find the nearest postal code in the dataset
        postal_codes = zip_code.astype(int)
        nearest_postal_code = postal_codes.iloc[(postal_codes - int(postal_code)).abs().argsort()[:1]].values[0]
        postal_code = str(nearest_postal_code)
        print(f"Using nearest postal code: {postal_code}")
  
    postal_code = str(postal_code)[:4]  # Use only the first 5 digits

    #
    # PLACEHOLDERS
    #
    beds = 4
    baths = 3



    predicted_price = predict_price(postal_code, living_space, beds, baths)
    print('given apartment price:')
    get_typical_house(postal_code, float(apartment_price))
    #inflation
    predicted_price *= 1.063
    print(f"Predicted Price: {predicted_price}")
    print(f"Postal Code: {postal_code}, Living Space: {living_space}, Beds: {beds}, Baths: {baths}")

    return 'Data received!'

def predict_price(postal_code, living_space, beds, baths):
    # Load the pre-trained model
    model = joblib.load('random_forest_model.pkl')
    # Make a prediction
    feature_names = ['Zip Code', 'Living Space', 'Beds', 'Baths']
    input_data = pd.DataFrame([[postal_code, living_space, beds, baths]], columns=feature_names)
    prediction = model.predict(input_data)
    return prediction[0]

def get_typical_house(postal_code, price):
    # see what you can get in this area for the price that the user gave
    df_area = df[df['Zip Code'].astype(str).str.startswith(str(postal_code))]

    price_lower = price * 0.95
    price_upper = price * 1.05
    df_filtered = df_area[(df_area['Price'] >= price_lower) & (df_area['Price'] <= price_upper)]
    beds = df_filtered['Beds'].mode()[0]
    baths = df_filtered['Baths'].mode()[0]
    living_space = df_filtered['Living Space'].mean()
    median_income = df_filtered['Median Household Income'].mean()
    print(f"Typical house in area for given price: Beds: {beds}, Baths: {baths}, Living Space: {living_space}, Median Income: {median_income}")

    return

if __name__ == '__main__':
    app.run(debug=True)