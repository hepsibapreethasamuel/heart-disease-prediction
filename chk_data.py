import pandas as pd

df = pd.read_csv("heart.csv")

print(df.head())       # first 5 rows
print(df.shape)       # rows, columns
print(df.columns)     # column names
print(df.isnull().sum())  # missing values
