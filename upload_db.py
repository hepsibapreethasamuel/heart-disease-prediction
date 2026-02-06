import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("heart.csv")

# MySQL connection (CHANGE password)
engine = create_engine("mysql+pymysql://root:Hepsiba%402006@localhost/heart_db")

# Upload dataframe to MySQL
df.to_sql("heart_data", engine, if_exists="replace", index=False)

print("Heart dataset successfully pushed to MySQL!")
