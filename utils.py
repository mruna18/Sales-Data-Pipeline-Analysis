"""
Utility functions for data validation and processing
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_sales_data(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate sales data DataFrame
    
    Args:
        df: DataFrame to validate
        
    Returns:
        tuple: (is_valid, list of error messages)
    """
    errors = []
    
    # Check required columns
    required_columns = ['order_id', 'date', 'customer_name', 'product', 
                       'quantity', 'price_per_unit', 'total_price']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
    
    # Check for empty DataFrame
    if df.empty:
        errors.append("DataFrame is empty")
        return False, errors
    
    # Check for duplicate order_ids
    if 'order_id' in df.columns:
        duplicates = df[df.duplicated(subset=['order_id'], keep=False)]
        if not duplicates.empty:
            errors.append(f"Found {len(duplicates)} duplicate order_ids")
    
    # Validate data types and ranges
    if 'quantity' in df.columns:
        invalid_quantity = df[df['quantity'] <= 0]
        if not invalid_quantity.empty:
            errors.append(f"Found {len(invalid_quantity)} rows with quantity <= 0")
    
    if 'price_per_unit' in df.columns:
        invalid_price = df[df['price_per_unit'] < 0]
        if not invalid_price.empty:
            errors.append(f"Found {len(invalid_price)} rows with negative price_per_unit")
    
    if 'total_price' in df.columns:
        invalid_total = df[df['total_price'] < 0]
        if not invalid_total.empty:
            errors.append(f"Found {len(invalid_total)} rows with negative total_price")
    
    # Check if total_price matches quantity * price_per_unit (with tolerance)
    if all(col in df.columns for col in ['quantity', 'price_per_unit', 'total_price']):
        calculated_total = df['quantity'] * df['price_per_unit']
        tolerance = 0.01
        mismatches = df[abs(df['total_price'] - calculated_total) > tolerance]
        if not mismatches.empty:
            errors.append(f"Found {len(mismatches)} rows where total_price doesn't match quantity * price_per_unit")
    
    is_valid = len(errors) == 0
    return is_valid, errors

def get_db_connection(config):
    """
    Create and return MySQL database connection
    
    Args:
        config: Database configuration dictionary
        
    Returns:
        MySQL connection object
    """
    import mysql.connector
    try:
        conn = mysql.connector.connect(**config)
        logger.info(f"Successfully connected to database: {config['database']}")
        return conn
    except mysql.connector.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise
