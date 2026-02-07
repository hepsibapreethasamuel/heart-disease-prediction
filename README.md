# ❤️ Heart Disease Prediction System

An end-to-end Machine Learning web application for predicting heart disease using a **Random Forest classifier**, integrated with **MySQL** and deployed via **Flask**.

The system combines ML prediction with real-world medical rule validation, ensuring extreme clinical values are handled safely instead of being treated as statistical outliers.

> ⚠️ Educational Project — Not intended for real medical diagnosis.

---

## ✨ Features

### 🫀 ML-Based Prediction
- Random Forest classifier (~98.5% accuracy)
- Binary classification (Heart Disease / No Heart Disease)
- Risk probability display

### 🏥 Medical Rule Engine (Hybrid System)
- Critical clinical thresholds override ML
- Prevents dangerous inputs from being treated as outliers
- High-risk & critical warnings

### 🗄 Database Integration
- Dataset stored in MySQL
- Model trained directly from database
- User predictions logged back into MySQL

### 🌐 Web Interface
- Flask-based frontend
- Real-time prediction
- Clean input form
- Risk feedback and lifestyle suggestions

---

## 🧠 Hybrid Decision Architecture

This project uses two decision layers:

### 1️⃣ Medical Rule Engine (Primary Layer)

Extreme medical values are evaluated **BEFORE ML**:

- Resting BP ≥ 200 mmHg  
- Cholesterol ≥ 300 mg/dl  
- ST Depression ≥ 4  
- Exercise angina + severe chest pain  
- Multiple blocked vessels  

If triggered:

🚨 CRITICAL HEART RISK – Seek Immediate Medical Care

These values are **not treated as ML outliers**.

---

### 2️⃣ Machine Learning (Secondary Layer)

If no critical rules fire:

- Input passed to Random Forest  
- Prediction generated  
- Risk probability displayed  

This creates a **Hybrid Clinical + ML System**.

---

## 🧩 Tech Stack

- Python  
- Flask  
- Scikit-learn  
- Pandas  
- MySQL  
- SQLAlchemy  
- HTML / CSS  

---

## 🏗 Architecture Workflow

```text
Public Dataset
│
├── Uploaded to MySQL Database
│
├── Loaded into Pandas DataFrame
│
├── Random Forest Model Training
│
├── Model Saved (heart_rf_model.pkl)
│
├── Flask Web Application
│
├── User Inputs Clinical Data
│
├── Medical Rule Engine Validation
│
├── ML Prediction (Random Forest)
│
└── Prediction Stored Back in MySQL

```

## 📁 Project Structure

```text
heart-disease-prediction/
│
├── app.py                 # Flask web application
├── train_rf_model.py     # Random Forest model training
├── upload_db.py          # CSV dataset → MySQL
├── heart_rf_model.pkl    # Trained ML model
│
├── templates/
│   └── index.html        # Frontend UI
│
├── screenshots/
│   ├── ui.png            # Web interface
│   ├── prediction.png   # Prediction result
│   └── database.png     # MySQL database view
│
└── README.md             # Project documentation

```
## ▶ How to Run

Clone repository:

```bash
git clone https://github.com/yourusername/heart-disease-prediction.git
```

Install dependencies:

```bash
pip install -r requirements.txt

```

Run Flask app:

```bash
python app.py

```

Open browser:

```bash
http://127.0.0.1:8000

```

## 📊 Dataset

The dataset contains 13 clinical attributes:

1. Age

2. Sex

3. Chest pain type

4. Blood pressure

5. Cholesterol

6. Fasting blood sugar

7. ECG

8. Max heart rate

9. Exercise angina

10. ST depression

11. ST slope

12. Major vessels

13. Thalassemia

## 📈 Model Performance

- Algorithm: Random Forest Classifier
- Accuracy: ~98.5%
- Dataset Size: 1025 records
- Features: 13 clinical attributes

Evaluation performed using train-test split.

### Target:

0 → No Heart Disease  
1 → Heart Disease

## 🌟 Key Highlights

- End-to-end ML pipeline (Dataset → DB → Model → Web App)
- Hybrid Clinical Rule + Machine Learning system
- Real-time prediction using Flask
- MySQL database integration
- Medical safety layer for extreme values
- Prediction history stored in database

## 🎓 Learning Outcomes

- Built full-stack ML application
- Integrated MySQL with ML pipeline
- Implemented clinical rule engine
- Deployed Flask backend
- Learned GitHub project management

## 🏥 Medical Disclaimer

This system is for academic demonstration only.

Predictions are based on historical patterns and simplified clinical rules.

Not intended to replace professional medical advice.

## 👩‍💻 Author

Hepsiba Preetha Samuel
B.Tech Artificial Intelligence & Data Science
