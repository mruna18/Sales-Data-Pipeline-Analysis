"""
Analyze sales data from MySQL database
Generates insights and visualizations
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import sys
import os
from config import setup_logging, DB_CONFIG
from utils import get_db_connection

# Setup logging
logger = setup_logging()

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

def analyze_sales_data(output_dir: str = "output") -> bool:
    """
    Analyze sales data and generate visualizations
    
    Args:
        output_dir: Directory to save output files and visualizations
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = None
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("Connecting to MySQL database...")
        conn = get_db_connection(DB_CONFIG)
        
        # Read Data into Pandas DataFrame
        logger.info("Fetching sales data from database...")
        query = "SELECT * FROM sales ORDER BY date"
        df = pd.read_sql(query, conn)
        
        if df.empty:
            logger.error("❌ No data found in database")
            return False
        
        logger.info(f"Loaded {len(df)} rows from database")
        
        # Convert 'date' column to datetime
        df["date"] = pd.to_datetime(df["date"])
        
        # Check the Data
        logger.info("Data Summary:")
        logger.info(f"   Shape: {df.shape}")
        logger.info(f"   Date range: {df['date'].min()} to {df['date'].max()}")
        logger.info(f"   Products: {df['product'].nunique()}")
        logger.info(f"   Customers: {df['customer_name'].nunique()}")
        
        # Calculate key metrics
        logger.info("\n" + "="*50)
        logger.info("📊 SALES ANALYSIS RESULTS")
        logger.info("="*50)
        
        # Total Sales
        total_sales = df["total_price"].sum()
        logger.info(f"💰 Total Sales: ${total_sales:,.2f}")
        
        # Average order value
        avg_order_value = df["total_price"].mean()
        logger.info(f"📈 Average Order Value: ${avg_order_value:,.2f}")
        
        # Total orders
        total_orders = len(df)
        logger.info(f"🛒 Total Orders: {total_orders:,}")
        
        # Top 5 Selling Products
        top_products = df.groupby("product")["total_price"].sum().sort_values(ascending=False).head(5)
        logger.info("\n🏆 Top 5 Products by Sales:")
        for product, sales in top_products.items():
            logger.info(f"   {product}: ${sales:,.2f}")
        
        # Top 5 Customers
        top_customers = df.groupby("customer_name")["total_price"].sum().sort_values(ascending=False).head(5)
        logger.info("\n👥 Top 5 Customers by Total Spend:")
        for customer, spend in top_customers.items():
            logger.info(f"   {customer}: ${spend:,.2f}")
        
        # Monthly sales trend
        df['month'] = df['date'].dt.to_period('M')
        monthly_sales = df.groupby('month')['total_price'].sum()
        logger.info("\n📅 Monthly Sales Summary:")
        for month, sales in monthly_sales.items():
            logger.info(f"   {month}: ${sales:,.2f}")
        
        # Generate visualizations
        logger.info("\nGenerating visualizations...")
        
        # 1. Daily Sales Trend
        daily_sales = df.groupby("date")["total_price"].sum()
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=daily_sales.index, y=daily_sales.values, marker="o", color="b", linewidth=2)
        plt.title("📊 Daily Sales Trend", fontsize=16, fontweight='bold')
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Total Sales ($)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/daily_sales_trend.png", dpi=300, bbox_inches='tight')
        logger.info(f"   ✅ Saved: {output_dir}/daily_sales_trend.png")
        plt.close()
        
        # 2. Top 5 Selling Products
        plt.figure(figsize=(10, 6))
        top_products_plot = top_products.sort_values(ascending=True)
        sns.barplot(x=top_products_plot.values, y=top_products_plot.index, palette="Blues_r")
        plt.title("🏆 Top 5 Best-Selling Products", fontsize=16, fontweight='bold')
        plt.xlabel("Total Sales ($)", fontsize=12)
        plt.ylabel("Product", fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_products.png", dpi=300, bbox_inches='tight')
        logger.info(f"   ✅ Saved: {output_dir}/top_products.png")
        plt.close()
        
        # 3. Monthly Sales Trend
        plt.figure(figsize=(12, 6))
        monthly_sales_plot = monthly_sales.sort_index()
        sns.barplot(x=[str(m) for m in monthly_sales_plot.index], 
                   y=monthly_sales_plot.values, palette="viridis")
        plt.title("📅 Monthly Sales Trend", fontsize=16, fontweight='bold')
        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Total Sales ($)", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/monthly_sales_trend.png", dpi=300, bbox_inches='tight')
        logger.info(f"   ✅ Saved: {output_dir}/monthly_sales_trend.png")
        plt.close()
        
        # 4. Product Quantity Distribution
        plt.figure(figsize=(10, 6))
        product_quantity = df.groupby("product")["quantity"].sum().sort_values(ascending=False)
        sns.barplot(x=product_quantity.values, y=product_quantity.index, palette="coolwarm")
        plt.title("📦 Total Quantity Sold by Product", fontsize=16, fontweight='bold')
        plt.xlabel("Total Quantity", fontsize=12)
        plt.ylabel("Product", fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/product_quantity.png", dpi=300, bbox_inches='tight')
        logger.info(f"   ✅ Saved: {output_dir}/product_quantity.png")
        plt.close()
        
        # Save summary statistics to CSV
        summary_data = {
            'Metric': ['Total Sales', 'Average Order Value', 'Total Orders', 
                      'Unique Products', 'Unique Customers', 'Date Range Start', 'Date Range End'],
            'Value': [total_sales, avg_order_value, total_orders, 
                     df['product'].nunique(), df['customer_name'].nunique(),
                     str(df['date'].min()), str(df['date'].max())]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(f"{output_dir}/sales_summary.csv", index=False)
        logger.info(f"   ✅ Saved: {output_dir}/sales_summary.csv")
        
        logger.info("\n" + "="*50)
        logger.info("✅ Analysis complete! All outputs saved to 'output' directory")
        logger.info("="*50)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error analyzing sales data: {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    try:
        output_dir = sys.argv[1] if len(sys.argv) > 1 else "output"
        success = analyze_sales_data(output_dir)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
