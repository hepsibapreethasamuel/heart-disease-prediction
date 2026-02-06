import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# MySQL connection (CHANGE password)
engine = create_engine("mysql+pymysql://root:Hepsiba%402006@localhost/heart_db")

# Load data from MySQL
df = pd.read_sql("SELECT * FROM heart_data", engine)

# Features & target
X = df.drop("target", axis=1)
y = df["target"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("Random Forest Accuracy:", acc)

# Save model
pickle.dump(model, open("heart_rf_model.pkl", "wb"))

print("Random Forest model saved!")
