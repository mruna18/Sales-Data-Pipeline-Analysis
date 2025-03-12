import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

#  Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sales_db"
)

# Read Data into Pandas DataFrame
query = "SELECT * FROM sales"
df = pd.read_sql(query, conn)

#  Close Connection
conn.close()

# Convert 'date' column to datetime
df["date"] = pd.to_datetime(df["date"])

#Check the Data
print(df.head())  
print(df.info())  # Ensure correct data types

#  Total Sales
total_sales = df["total_price"].sum()
print(f"💰 Total Sales: {total_sales}")

#  Top 5 Selling Products
top_products = df.groupby("product")["total_price"].sum().sort_values(ascending=False).head(5)
print("🏆 Top 5 Products by Sales:\n", top_products)

#  Top 5 Customers
top_customers = df.groupby("customer_name")["total_price"].sum().sort_values(ascending=False).head(5)
print("👥 Top 5 Customers by Total Spend:\n", top_customers)

#  Group by Date to See Sales Trends
daily_sales = df.groupby("date")["total_price"].sum()

#  Plot the Sales Trend
plt.figure(figsize=(10, 5))
sns.lineplot(x=daily_sales.index, y=daily_sales.values, marker="o", color="b")
plt.title("📊 Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Plot Top 5 Selling Products
plt.figure(figsize=(8, 5))
sns.barplot(x=top_products.values, y=top_products.index, palette="Blues_r")
plt.title("🏆 Top 5 Best-Selling Products")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.show()
