from flask import Flask, render_template, request, jsonify
import os
import pickle
import pandas as pd
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Lazy-loaded globals
model = None
engine = None

def load_model():
    global model
    if model is None:
        if not os.path.exists("heart_rf_model.pkl"):
            raise FileNotFoundError("Model file 'heart_rf_model.pkl' not found. Run model.py first.")
        model = pickle.load(open("heart_rf_model.pkl", "rb"))
    return model

def get_engine():
    global engine
    if engine is None:
        engine = create_engine("mysql+pymysql://root:Hepsiba%402006@localhost/heart_db", pool_pre_ping=True)
        # Test connection (SQLAlchemy 2.0 compatible)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    return engine

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    risk = None

    if request.method == "POST":
        model = load_model()
        engine = get_engine()

        age = float(request.form["age"])
        sex = float(request.form["sex"])
        cp = float(request.form["cp"])
        trestbps = float(request.form["trestbps"])
        chol = float(request.form["chol"])
        fbs = float(request.form["fbs"])
        restecg = float(request.form["restecg"])
        thalach = float(request.form["thalach"])
        exang = float(request.form["exang"])
        oldpeak = float(request.form["oldpeak"])
        slope = float(request.form["slope"])
        ca = float(request.form["ca"])
        thal = float(request.form["thal"])

        # ==========================
        # MEDICAL RULE ENGINE
        # ==========================

        if trestbps >= 200 or chol >= 300 or oldpeak >= 4 or (exang == 1 and cp >= 2) or ca >= 3:
            prediction = "🚨 CRITICAL HEART RISK – Seek Immediate Medical Care"
            risk = "95%"

            df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                                thalach,exang,oldpeak,slope,ca,thal,1]],
                              columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                       "thalach","exang","oldpeak","slope","ca","thal","target"])

            df.to_sql("user_predictions", engine, if_exists="append", index=False)

            return render_template("index.html", prediction=prediction, risk=risk)

        # ==========================
        # ML Prediction
        # ==========================

        features = [[age,sex,cp,trestbps,chol,fbs,restecg,
                     thalach,exang,oldpeak,slope,ca,thal]]

        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        prediction = "❤️ Heart Disease Detected" if pred == 1 else "✅ No Heart Disease"
        risk = f"{round(prob*100,2)}%"

        df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                            thalach,exang,oldpeak,slope,ca,thal,pred]],
                          columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                   "thalach","exang","oldpeak","slope","ca","thal","target"])

        df.to_sql("user_predictions", engine, if_exists="append", index=False)

    return render_template("index.html", prediction=prediction, risk=risk)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        model = load_model()
        engine = get_engine()

        data = request.json

        age = float(data["age"])
        sex = float(data["sex"])
        cp = float(data["cp"])
        trestbps = float(data["trestbps"])
        chol = float(data["chol"])
        fbs = float(data["fbs"])
        restecg = float(data["restecg"])
        thalach = float(data["thalach"])
        exang = float(data["exang"])
        oldpeak = float(data["oldpeak"])
        slope = float(data["slope"])
        ca = float(data["ca"])
        thal = float(data["thal"])

        # ==========================
        # MEDICAL RULE ENGINE
        # ==========================
        if trestbps >= 200 or chol >= 300 or oldpeak >= 4 or (exang == 1 and cp >= 2) or ca >= 3:
            df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                                thalach,exang,oldpeak,slope,ca,thal,1]],
                              columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                       "thalach","exang","oldpeak","slope","ca","thal","target"])
            df.to_sql("user_predictions", engine, if_exists="append", index=False)

            return jsonify({
                "prediction": "Heart Disease Detected ⚠️",
                "risk": 95.0,
                "success": True
            })

        # ==========================
        # ML Prediction
        # ==========================
        features = [[age,sex,cp,trestbps,chol,fbs,restecg,
                     thalach,exang,oldpeak,slope,ca,thal]]

        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        prediction = "Heart Disease Detected ⚠️" if pred == 1 else "No Heart Disease ✓"
        risk = round(prob * 100, 2)

        df = pd.DataFrame([[age,sex,cp,trestbps,chol,fbs,restecg,
                            thalach,exang,oldpeak,slope,ca,thal,pred]],
                          columns=["age","sex","cp","trestbps","chol","fbs","restecg",
                                   "thalach","exang","oldpeak","slope","ca","thal","target"])

        df.to_sql("user_predictions", engine, if_exists="append", index=False)

        return jsonify({
            "prediction": prediction,
            "risk": risk,
            "success": True
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 400

if __name__ == "__main__":
    app.run(debug=True, port=8000)
