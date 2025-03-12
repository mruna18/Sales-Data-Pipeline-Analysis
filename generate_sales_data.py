import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Define the number of records
num_records = 500

# Generate sales data
data = {
    "order_id": [fake.uuid4()[:8] for _ in range(num_records)],  # Unique Order IDs
    "date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_records)],  # Random Dates
    "customer_name": [fake.name() for _ in range(num_records)],  # Customer Names
    "product": [random.choice(["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"]) for _ in range(num_records)],
    "quantity": [random.randint(1, 5) for _ in range(num_records)],  # Random Quantity
    "price_per_unit": [random.uniform(100, 2000) for _ in range(num_records)],  # Random Prices
    "total_price": [0] * num_records,  # Placeholder for total price
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate total price
df["total_price"] = df["quantity"] * df["price_per_unit"]

# Save to CSV
df.to_csv("sales_data.csv", index=False)

print("Sample sales data generated and saved as 'sales_data.csv'.")
