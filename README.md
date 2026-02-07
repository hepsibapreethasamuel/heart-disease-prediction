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


