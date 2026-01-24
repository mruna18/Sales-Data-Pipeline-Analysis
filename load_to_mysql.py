"""
Load cleaned sales data into MySQL database
Uses bulk insert for better performance
"""
import pandas as pd
import mysql.connector
import logging
import sys
from config import setup_logging, DB_CONFIG
from utils import get_db_connection, validate_sales_data

# Setup logging
logger = setup_logging()

def load_data_to_mysql(input_file: str = "cleaned_sales_data.csv", 
                      batch_size: int = 100) -> bool:
    """
    Load cleaned sales data into MySQL database using bulk insert
    
    Args:
        input_file: Input CSV file path
        batch_size: Number of records to insert per batch
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = None
    cursor = None
    
    try:
        logger.info(f"Loading data from {input_file}...")
        
        # Load cleaned data
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} rows from {input_file}")
        
        # Validate data before loading
        logger.info("Validating data before loading...")
        is_valid, errors = validate_sales_data(df)
        if not is_valid:
            logger.error(f"❌ Data validation failed: {errors}")
            return False
        logger.info("✅ Data validation passed")
        
        # Connect to MySQL Database
        logger.info("Connecting to MySQL database...")
        conn = get_db_connection(DB_CONFIG)
        cursor = conn.cursor()
        
        # Prepare data for bulk insert
        logger.info("Preparing data for bulk insert...")
        # Convert date to string format for MySQL
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # Prepare insert statement
        insert_query = """
            INSERT INTO sales (order_id, date, customer_name, product, quantity, price_per_unit, total_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date = VALUES(date),
                customer_name = VALUES(customer_name),
                product = VALUES(product),
                quantity = VALUES(quantity),
                price_per_unit = VALUES(price_per_unit),
                total_price = VALUES(total_price)
        """
        
        # Convert DataFrame to list of tuples for bulk insert
        data_tuples = [
            tuple(row) for row in df[
                ['order_id', 'date', 'customer_name', 'product', 
                 'quantity', 'price_per_unit', 'total_price']
            ].values
        ]
        
        # Insert data in batches
        total_rows = len(data_tuples)
        inserted_count = 0
        
        logger.info(f"Inserting {total_rows} rows in batches of {batch_size}...")
        
        for i in range(0, total_rows, batch_size):
            batch = data_tuples[i:i + batch_size]
            try:
                cursor.executemany(insert_query, batch)
                inserted_count += len(batch)
                logger.info(f"Inserted batch: {inserted_count}/{total_rows} rows")
            except mysql.connector.Error as e:
                logger.error(f"Error inserting batch {i//batch_size + 1}: {e}")
                # Continue with next batch
                continue
        
        # Commit transaction
        conn.commit()
        logger.info(f"✅ Successfully loaded {inserted_count} rows into MySQL database!")
        
        # Get summary statistics
        cursor.execute("SELECT COUNT(*) FROM sales")
        total_in_db = cursor.fetchone()[0]
        logger.info(f"Total records in database: {total_in_db}")
        
        return True
        
    except FileNotFoundError:
        logger.error(f"❌ Input file not found: {input_file}")
        return False
    except mysql.connector.Error as e:
        logger.error(f"❌ MySQL error: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        logger.error(f"❌ Error loading data to MySQL: {e}", exc_info=True)
        if conn:
            conn.rollback()
        return False
    finally:
        # Close connections
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    try:
        input_file = sys.argv[1] if len(sys.argv) > 1 else "cleaned_sales_data.csv"
        batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        success = load_data_to_mysql(input_file, batch_size)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("Data loading interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
