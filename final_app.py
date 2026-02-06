from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

app = Flask(__name__)

# ===============================
# Load Random Forest Model
# ===============================
model = pickle.load(open("heart_rf_model.pkl", "rb"))

# ===============================
# MySQL Connection
# ===============================
engine = create_engine("mysql+pymysql://root:Hepsiba%402006@localhost/heart_db")

# ===============================
# Home Route
# ===============================
@app.route("/")
def home():
    return render_template("index.html")

# ===============================
# Predict Route (JSON API)
# ===============================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data
        data = request.json
        
        # Extract values
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
        
        # CRITICAL CONDITION - Immediate medical attention
        if trestbps >= 200 or chol >= 300 or oldpeak >= 4 or (exang == 1 and cp >= 2) or ca >= 3:
            # Save to DB with high risk flag
            df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                                thalach,exang,oldpeak,slope,ca,thal,1]],
                              columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                      "thalach","exang","oldpeak","slope","ca","thal","target"])
            df.to_sql("user_predictions", engine, if_exists="append", index=False)
            
            return jsonify({
                "prediction": "Heart Disease Detected ⚠️",
                "risk": 95.0,  # Critical risk level
                "success": True
            })

        # HIGH RISK SCORE - Multiple risk factors
        risk_score = 0
        if age >= 65: risk_score += 1
        if trestbps >= 160: risk_score += 1
        if chol >= 240: risk_score += 1
        if fbs == 1: risk_score += 1
        if thalach <= 120: risk_score += 1
        if restecg != 0: risk_score += 1

        if risk_score >= 3:  # Multiple risk factors present
            # Save to DB
            df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                                thalach,exang,oldpeak,slope,ca,thal,1]],
                              columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                      "thalach","exang","oldpeak","slope","ca","thal","target"])
            df.to_sql("user_predictions", engine, if_exists="append", index=False)
            
            return jsonify({
                "prediction": "Heart Disease Detected ⚠️",
                "risk": 75.0,  # High risk level
                "success": True
            })

        # =========================
        # ML Prediction (for normal cases)
        # =========================
        features = np.array([[
            age, sex, cp, trestbps, chol, fbs,
            restecg, thalach, exang, oldpeak,
            slope, ca, thal
        ]])

        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]
        
        result = "Heart Disease Detected ⚠️" if pred == 1 else "No Heart Disease ✓"
        risk_percentage = round(prob * 100, 2)

        # =========================
        # Save Prediction to DB
        # =========================
        df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                            thalach,exang,oldpeak,slope,ca,thal,pred]],
                          columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                  "thalach","exang","oldpeak","slope","ca","thal","target"])
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

# ===============================
# Run App
# ===============================
if __name__ == "__main__":
    app.run(debug=True, port=8000)
