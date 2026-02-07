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

