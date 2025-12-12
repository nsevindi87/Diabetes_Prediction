import streamlit as st
import requests
import pandas as pd
import numpy as np

API_URL = 'http://127.0.0.1:5000/predict'

PARAM_RANGES = {
    "Pregnancies": {"label": "Number of Pregnancies (0-17)", "min": 0, "max": 17, "default": 1, "step": 1},
    "Glucose": {"label": "Glucose (Plasma) Level (70-250 mg/dL)", "min": 50.0, "max": 250.0, "default": 120.0, "step": 0.1},
    "BloodPressure": {"label": "Diastolic Blood Pressure (40-140 mmHg)", "min": 40.0, "max": 140.0, "default": 70.0, "step": 0.1},
    "SkinThickness": {"label": "Triceps Skin Fold Thickness (0-100 mm)", "min": 0.0, "max": 100.0, "default": 20.0, "step": 0.1},
    "Insulin": {"label": "2-Hour Serum Insulin (0-850 mu/U per ml)", "min": 0.0, "max": 850.0, "default": 79.79, "step": 0.1},
    "BMI": {"label": "Body Mass Index (BMI) (15-65)", "min": 15.0, "max": 65.0, "default": 25.0, "step": 0.1},
    "DiabetesPedigreeFunction": {"label": "Diabetes Pedigree Function (0.07-2.5)", "min": 0.07, "max": 2.5, "default": 0.5, "step": 0.001},
    "Age": {"label": "Age (21-100)", "min": 21, "max": 100, "default": 30, "step": 1}
}



st.set_page_config(page_title="Diabetes Prediction App", layout="wide")

st.title("🩺 Diabetes Prediction System")
st.markdown("""
    Please enter the patient's biometric data. The model will estimate the risk of diabetes based on the provided values.
""")

result_placeholder = st.empty()

with st.form("diabetes_form"):
    st.subheader("Patient Information")
    
    col1, col2 = st.columns(2)
    
    input_data = {}
    
    params1 = list(PARAM_RANGES.keys())[:4]
    for param in params1:
        with col1:
            r = PARAM_RANGES[param]
            if r['step'] >= 1: 
                input_data[param] = st.slider(r['label'], r['min'], r['max'], r['default'], r['step'])
            else: 
                input_data[param] = st.number_input(r['label'], r['min'], r['max'], r['default'], r['step'], format="%.3f")
    
    params2 = list(PARAM_RANGES.keys())[4:]
    for param in params2:
        with col2:
            r = PARAM_RANGES[param]
            if r['step'] >= 1:
                input_data[param] = st.slider(r['label'], r['min'], r['max'], r['default'], r['step'])
            else:
                input_data[param] = st.number_input(r['label'], r['min'], r['max'], r['default'], r['step'], format="%.3f")

    submitted = st.form_submit_button("Start Prediction")

if submitted:
    
    try:
        response = requests.post(API_URL, json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")

            with result_placeholder.expander("Prediction Result", expanded=True):
                st.subheader("Model Output")
                
                if prediction == "Diabetes":
                    st.error("⚠️ Prediction Result: HIGH DIABETES RISK")
                    st.markdown("""
                        **Disclaimer:** This is not a diagnostic tool. Please consult a specialist for a definitive diagnosis.
                    """)
                elif prediction == "No Diabetes":
                    st.success("✅ Prediction Result: LOW DIABETES RISK")
                    st.markdown("""
                        **Recommendation:** Regular check-ups are still advised.
                    """)
                else:
                    st.warning(f"Unexpected response from the model: {prediction}")

        else:
            error_message = response.json().get("error", "Unknown error message from API.")
            with result_placeholder.expander("Error", expanded=True):
                st.error(f"API Error ({response.status_code}): {error_message}")

    except requests.exceptions.ConnectionError:
        with result_placeholder.expander("Connection Error", expanded=True):
            st.error(f"""
                ❌ **Connection Error:** Your Flask API server ({API_URL}) might be down or running on the wrong address.
                Please ensure your Flask application is running in a separate terminal.
            """)
    except Exception as e:
        with result_placeholder.expander("Application Error", expanded=True):
            st.error(f"Application Error: {e}")