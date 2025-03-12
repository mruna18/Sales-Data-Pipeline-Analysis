import pandas as pd

# Load the data
df = pd.read_csv("sales_data.csv")

# remove duplicate rows (if any)
df.drop_duplicates(inplace=True)

# handle missing values (fill with default values)
df.fillna({
    "customer_name": "Unknown",
    "product": "Unknown",
    "quantity": 1,
    "price_per_unit": df["price_per_unit"].mean(),  # Fill missing prices with the average price
}, inplace=True)

# to ensure 'date' column is in proper datetime format
df["date"] = pd.to_datetime(df["date"], errors="coerce")

#drop rows where 'date' conversion failed
df.dropna(subset=["date"], inplace=True)

#round 'price_per_unit' & 'total_price' to 2 decimal places
df["price_per_unit"] = df["price_per_unit"].round(2)
df["total_price"] = df["total_price"].round(2)

#save the cleaned data
df.to_csv("cleaned_sales_data.csv", index=False)

print("Data cleaning complete! Saved as 'cleaned_sales_data.csv'.")


