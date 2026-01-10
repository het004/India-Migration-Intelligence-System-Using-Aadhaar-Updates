import pandas as pd

df = pd.read_parquet("Dataset/processed/forecast/future_forecast.parquet")
print(df)
