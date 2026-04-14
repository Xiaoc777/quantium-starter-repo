import pandas as pd
from pathlib import Path

data_folder = Path("data")

files = [
    data_folder / "daily_sales_data_0.csv",
    data_folder / "daily_sales_data_1.csv",
    data_folder / "daily_sales_data_2.csv",
]

dataframes = [pd.read_csv(file) for file in files]
df = pd.concat(dataframes, ignore_index=True)

df = df[df["product"].str.strip().str.lower() == "pink morsel"].copy()

df["price"] = df["price"].replace("[$]", "", regex=True).astype(float)

df["sales"] = df["price"] * df["quantity"]

output_df = df[["sales", "date", "region"]].copy()
output_df.columns = ["Sales", "Date", "Region"]

output_df.to_csv("formatted_sales_data.csv", index=False)

print("Done. formatted_sales_data.csv has been created.")