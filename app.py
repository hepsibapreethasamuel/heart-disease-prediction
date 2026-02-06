from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Load trained model
try:
    model = pickle.load(open("heart_rf_model.pkl", "rb"))
except:
    model = None

# MySQL connection
engine = create_engine("mysql+pymysql://root:Hepsiba%402006@localhost/heart_db")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        data = request.json
        
        # Extract features in the correct order (13 features)
        age = float(data['age'])
        sex = float(data['sex'])
        cp = float(data['cp'])
        trestbps = float(data['trestbps'])
        chol = float(data['chol'])
        fbs = float(data['fbs'])
        restecg = float(data['restecg'])
        thalach = float(data['thalach'])
        exang = float(data['exang'])
        oldpeak = float(data['oldpeak'])
        slope = float(data['slope'])
        ca = float(data['ca'])
        thal = float(data['thal'])

        # =========================
        # MEDICAL RULE ENGINE (Override ML for Critical Cases)
        # =========================
        if trestbps >= 200 or chol >= 300 or oldpeak >= 4 or (exang == 1 and cp >= 2) or ca >= 3:
            prediction = 1
            result = "Heart Disease Detected ⚠️"
            risk_percentage = 95.0

            df = pd.DataFrame([[
                age, sex, cp, trestbps, chol, fbs,
                restecg, thalach, exang, oldpeak,
                slope, ca, thal, prediction
            ]], columns=[
                "age","sex","cp","trestbps","chol","fbs","restecg",
                "thalach","exang","oldpeak","slope","ca","thal","target"
            ])
            df.to_sql("user_predictions", engine, if_exists="append", index=False)

            return jsonify({
                "prediction": result,
                "risk": risk_percentage,
                "success": True
            })

        risk_score = 0
        if age >= 65:
            risk_score += 1
        if trestbps >= 160:
            risk_score += 1
        if chol >= 240:
            risk_score += 1
        if fbs == 1:
            risk_score += 1
        if thalach <= 120:
            risk_score += 1
        if restecg != 0:
            risk_score += 1

        if risk_score >= 3:
            prediction = 1
            result = "Heart Disease Detected ⚠️"
            risk_percentage = 75.0

            df = pd.DataFrame([[
                age, sex, cp, trestbps, chol, fbs,
                restecg, thalach, exang, oldpeak,
                slope, ca, thal, prediction
            ]], columns=[
                "age","sex","cp","trestbps","chol","fbs","restecg",
                "thalach","exang","oldpeak","slope","ca","thal","target"
            ])
            df.to_sql("user_predictions", engine, if_exists="append", index=False)

            return jsonify({
                "prediction": result,
                "risk": risk_percentage,
                "success": True
            })

        features = np.array([[
            age, sex, cp, trestbps, chol, fbs,
            restecg, thalach, exang, oldpeak,
            slope, ca, thal
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        result = "Heart Disease Detected ⚠️" if prediction == 1 else "No Heart Disease ✓"
        risk_percentage = round(probability[1] * 100, 2)
        
        # Save to database
        df = pd.DataFrame([[
            float(data['age']), float(data['sex']), float(data['cp']),
            float(data['trestbps']), float(data['chol']), float(data['fbs']),
            float(data['restecg']), float(data['thalach']), float(data['exang']),
            float(data['oldpeak']), float(data['slope']), float(data['ca']),
            float(data['thal']), prediction
        ]], columns=[
            "age","sex","cp","trestbps","chol","fbs","restecg",
            "thalach","exang","oldpeak","slope","ca","thal","target"
        ])
        df.to_sql("user_predictions", engine, if_exists="append", index=False)
        
        return jsonify({
            "prediction": result,
            "risk": risk_percentage,
            "success": True
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
