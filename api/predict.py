import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Yükleme Kısmı (Dosya adlarının aynı klasörde olduğunu varsayar)
try:
    with open("diabetes_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    with open("scaler.pkl", "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    print("Modeller başarıyla yüklendi.")
except Exception as e:
    print(f"Model yükleme hatası: {e}")
    # Hata yönetimi burada daha önemlidir.

@app.route("/")
def home():
    return "Diabetes Prediction App is runnung"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = pd.DataFrame([data])

        
        if not data:
            return jsonify({"error": "Input data not provided"})
        
        required_columns = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]

        if not all(col in input_data.columns for col in required_columns):
                return jsonify({"error": f"Required columns missing. Required columns: {required_columns}"}), 400

        input_data = input_data[required_columns]

        print(input_data)

        # scale the data
        scaled_data = scaler.transform(input_data)

        # make prediction
        prediction = model.predict(scaled_data)

        response = {
                "prediction": "Diabetes" if prediction[0] == 1 else "No Diabetes"
        }
        print(response)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
