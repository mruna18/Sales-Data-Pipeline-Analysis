import pandas as pd
import mysql.connector

# Load cleaned data
df = pd.read_csv("cleaned_sales_data.csv")

#Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="root",  
    database="sales_db"
)
cursor = conn.cursor()

#  Insert Data into MySQL Table with Print Debugging
for _, row in df.iterrows():
    print("Inserting:", row.to_dict())  # Print the row being inserted
    
    cursor.execute("""
        INSERT INTO sales (order_id, date, customer_name, product, quantity, price_per_unit, total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Commit and Close Connection
conn.commit()
conn.close()

print("Data successfully loaded into MySQL!")
