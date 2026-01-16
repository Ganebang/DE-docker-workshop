import sys
import pandas as pd

print("arguments:", sys.argv)
month = int(sys.argv[1])

df = pd.DataFrame({"day": [1, 2], "Number_of_passengers": [3, 4]})
df["month"] = month
print(df.head())

df.to_parquet(f"output_month-{month}.parquet")
print(f"Hello pipeline month = {month}")