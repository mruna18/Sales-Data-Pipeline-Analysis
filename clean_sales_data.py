"""
Clean and transform sales data
"""
import pandas as pd
import logging
import sys
from config import setup_logging
from utils import validate_sales_data

# Setup logging
logger = setup_logging()

def clean_sales_data(input_file: str = "sales_data.csv", 
                    output_file: str = "cleaned_sales_data.csv") -> bool:
    """
    Clean and transform sales data
    
    Args:
        input_file: Input CSV file path
        output_file: Output CSV file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"Loading data from {input_file}...")
        
        # Load the data
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} rows from {input_file}")
        
        initial_count = len(df)
        
        # Remove duplicate rows
        duplicates_before = len(df)
        df.drop_duplicates(inplace=True)
        duplicates_removed = duplicates_before - len(df)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        # Handle missing values
        missing_before = df.isnull().sum().sum()
        if missing_before > 0:
            logger.info(f"Found {missing_before} missing values, filling them...")
            
            # Calculate mean price before filling (to avoid NaN issues)
            mean_price = df["price_per_unit"].mean() if not df["price_per_unit"].isna().all() else 0
            
            df.fillna({
                "customer_name": "Unknown",
                "product": "Unknown",
                "quantity": 1,
                "price_per_unit": mean_price,
            }, inplace=True)
            
            # Recalculate total_price for rows where it might be missing
            if df["total_price"].isna().any():
                mask = df["total_price"].isna()
                df.loc[mask, "total_price"] = (df.loc[mask, "quantity"] * df.loc[mask, "price_per_unit"]).round(2)
        
        # Ensure 'date' column is in proper datetime format
        logger.info("Converting date column to datetime format...")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        
        # Drop rows where 'date' conversion failed
        invalid_dates = df["date"].isna().sum()
        if invalid_dates > 0:
            logger.warning(f"Dropping {invalid_dates} rows with invalid dates")
            df.dropna(subset=["date"], inplace=True)
        
        # Round 'price_per_unit' & 'total_price' to 2 decimal places
        df["price_per_unit"] = df["price_per_unit"].round(2)
        df["total_price"] = df["total_price"].round(2)
        
        # Validate cleaned data
        logger.info("Validating cleaned data...")
        is_valid, errors = validate_sales_data(df)
        if not is_valid:
            logger.warning(f"Data validation found issues: {errors}")
        else:
            logger.info("✅ Data validation passed")
        
        # Save the cleaned data
        logger.info(f"Saving cleaned data to {output_file}...")
        df.to_csv(output_file, index=False)
        
        final_count = len(df)
        logger.info(f"✅ Data cleaning complete!")
        logger.info(f"   Initial rows: {initial_count}")
        logger.info(f"   Final rows: {final_count}")
        logger.info(f"   Rows removed: {initial_count - final_count}")
        logger.info(f"   Saved to '{output_file}'")
        
        return True
        
    except FileNotFoundError:
        logger.error(f"❌ Input file not found: {input_file}")
        return False
    except Exception as e:
        logger.error(f"❌ Error cleaning sales data: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    try:
        input_file = sys.argv[1] if len(sys.argv) > 1 else "sales_data.csv"
        output_file = sys.argv[2] if len(sys.argv) > 2 else "cleaned_sales_data.csv"
        success = clean_sales_data(input_file, output_file)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("Data cleaning interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


