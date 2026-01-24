"""
Generate sample sales data for testing and development
"""
import pandas as pd
import numpy as np
from faker import Faker
import random
import logging
import sys
from config import setup_logging

# Setup logging
logger = setup_logging()

def generate_sales_data(num_records: int = 500, output_file: str = "sales_data.csv") -> bool:
    """
    Generate sample sales data
    
    Args:
        num_records: Number of records to generate
        output_file: Output CSV file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"Starting data generation for {num_records} records...")
        
        # Initialize Faker
        fake = Faker()
        
        # Generate sales data
        logger.info("Generating order IDs...")
        data = {
            "order_id": [fake.uuid4()[:8] for _ in range(num_records)],
            "date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_records)],
            "customer_name": [fake.name() for _ in range(num_records)],
            "product": [random.choice(["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"]) 
                       for _ in range(num_records)],
            "quantity": [random.randint(1, 5) for _ in range(num_records)],
            "price_per_unit": [round(random.uniform(100, 2000), 2) for _ in range(num_records)],
        }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Calculate total price
        df["total_price"] = (df["quantity"] * df["price_per_unit"]).round(2)
        
        # Save to CSV
        logger.info(f"Saving data to {output_file}...")
        df.to_csv(output_file, index=False)
        
        logger.info(f"✅ Successfully generated {len(df)} records and saved to '{output_file}'")
        logger.info(f"Data summary: {len(df)} rows, {len(df.columns)} columns")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error generating sales data: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    try:
        # Get number of records from command line or use default
        num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 500
        success = generate_sales_data(num_records)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("Data generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
