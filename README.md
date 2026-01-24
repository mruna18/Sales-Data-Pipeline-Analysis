# Sales-Data-Pipeline-Analysis 

## 🚀 Project Overview  
This project is a **Sales Data Pipeline & Analysis** system built using **Python, Pandas, MySQL, Matplotlib, and Seaborn**.  
It includes an **ETL (Extract, Transform, Load) pipeline** to process and analyze sales data, optimize SQL queries, and visualize insights.

The pipeline demonstrates production-ready practices including error handling, logging, data validation, and optimized database operations.

---

## 🔹 Features  
✔️ **Data Generation** - Generate synthetic sales data for testing  
✔️ **Data Cleaning** - Transform and clean data using Pandas with validation  
✔️ **Database Integration** - Load data into MySQL with bulk insert optimization  
✔️ **Data Analysis** - Analyze top products, total sales, and customer insights  
✔️ **Visualizations** - Generate comprehensive sales trend visualizations  
✔️ **Error Handling** - Robust error handling and logging throughout  
✔️ **Data Validation** - Automated data quality checks  
✔️ **Configuration Management** - Environment-based configuration  

---

## 🛠️ Technologies Used  
- **Python 3.8+** (NumPy, Pandas, Faker)  
- **MySQL 8.0+** (For data storage)  
- **Matplotlib, Seaborn** (For data visualization)  
- **python-dotenv** (For environment configuration)  

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher**
- **MySQL Server 8.0 or higher**
- **pip** (Python package manager)
- **Git** (optional, for cloning the repository)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Sales-Data-Pipeline-Analysis
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

1. **Start MySQL Server** (if not already running)

2. **Create Database and Tables**
   ```bash
   mysql -u root -p < schema.sql
   ```
   Or manually run the SQL commands in `schema.sql` using MySQL Workbench or command line.

3. **Verify Database Creation**
   ```sql
   SHOW DATABASES;
   USE sales_db;
   SHOW TABLES;
   ```

### Step 5: Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   # On Windows
   copy .env.example .env
   
   # On Linux/Mac
   cp .env.example .env
   ```

2. **Edit `.env` file** with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=sales_db
   DB_PORT=3306
   LOG_LEVEL=INFO
   ```

---

## 📖 Usage

### Complete Pipeline Workflow

Run the pipeline in the following order:

#### 1. Generate Sample Data
```bash
python generate_sales_data.py [num_records]
```
- Generates synthetic sales data
- Default: 500 records
- Output: `sales_data.csv`

**Example:**
```bash
python generate_sales_data.py 1000
```

#### 2. Clean the Data
```bash
python clean_sales_data.py [input_file] [output_file]
```
- Removes duplicates, handles missing values, validates dates
- Default input: `sales_data.csv`
- Default output: `cleaned_sales_data.csv`

**Example:**
```bash
python clean_sales_data.py sales_data.csv cleaned_sales_data.csv
```

#### 3. Load Data to MySQL
```bash
python load_to_mysql.py [input_file] [batch_size]
```
- Loads cleaned data into MySQL database
- Uses bulk insert for performance
- Default input: `cleaned_sales_data.csv`
- Default batch size: 100

**Example:**
```bash
python load_to_mysql.py cleaned_sales_data.csv 200
```

#### 4. Analyze and Visualize
```bash
python analyze_sales.py [output_dir]
```
- Analyzes sales data from database
- Generates visualizations and summary statistics
- Default output directory: `output`

**Example:**
```bash
python analyze_sales.py output
```

### Output Files

After running the analysis, you'll find:
- `output/daily_sales_trend.png` - Daily sales trend line chart
- `output/top_products.png` - Top 5 products bar chart
- `output/monthly_sales_trend.png` - Monthly sales bar chart
- `output/product_quantity.png` - Product quantity distribution
- `output/sales_summary.csv` - Summary statistics in CSV format
- `sales_pipeline.log` - Application logs

---

## 📁 Project Structure

```
Sales-Data-Pipeline-Analysis/
│
├── generate_sales_data.py    # Generate synthetic sales data
├── clean_sales_data.py       # Clean and transform data
├── load_to_mysql.py          # Load data to MySQL database
├── analyze_sales.py          # Analyze and visualize data
├── config.py                 # Configuration management
├── utils.py                  # Utility functions (validation, DB connection)
├── schema.sql                # Database schema
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
│
├── sales_data.csv            # Generated raw data
├── cleaned_sales_data.csv    # Cleaned data
├── output/                   # Analysis outputs (created after analysis)
│   ├── daily_sales_trend.png
│   ├── top_products.png
│   ├── monthly_sales_trend.png
│   ├── product_quantity.png
│   └── sales_summary.csv
│
└── sales_pipeline.log        # Application logs
```

---

## 🔍 Key Features Explained

### Data Validation
- Checks for required columns
- Validates data types and ranges
- Detects duplicate order IDs
- Verifies price calculations

### Error Handling
- Comprehensive try-except blocks
- Database transaction rollback on errors
- Detailed error logging
- Graceful failure handling

### Logging
- File and console logging
- Configurable log levels
- Detailed operation tracking
- Error stack traces

### Performance Optimization
- Bulk database inserts (batch processing)
- Efficient pandas operations
- Database connection pooling ready
- Optimized SQL queries

---

## 🧪 Testing

### Manual Testing Steps

1. **Test Data Generation:**
   ```bash
   python generate_sales_data.py 100
   # Verify sales_data.csv is created with 100 rows
   ```

2. **Test Data Cleaning:**
   ```bash
   python clean_sales_data.py
   # Check logs for validation results
   # Verify cleaned_sales_data.csv is created
   ```

3. **Test Database Loading:**
   ```bash
   python load_to_mysql.py
   # Check database: SELECT COUNT(*) FROM sales;
   ```

4. **Test Analysis:**
   ```bash
   python analyze_sales.py
   # Verify output files are created
   ```

---

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
- Verify MySQL server is running
- Check credentials in `.env` file
- Ensure database `sales_db` exists
- Verify user has proper permissions

**2. Module Not Found Error**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**3. File Not Found Error**
- Ensure you run scripts in correct order
- Check file paths are correct
- Verify input files exist

**4. Permission Denied (MySQL)**
- Grant proper permissions: `GRANT ALL ON sales_db.* TO 'user'@'localhost';`
- Check MySQL user privileges

---

## 📊 Database Schema

The `sales` table structure:
- `order_id` (VARCHAR, PRIMARY KEY)
- `date` (DATE, INDEXED)
- `customer_name` (VARCHAR, INDEXED)
- `product` (VARCHAR, INDEXED)
- `quantity` (INT, CHECK > 0)
- `price_per_unit` (DECIMAL, CHECK >= 0)
- `total_price` (DECIMAL, CHECK >= 0)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Views Available:**
- `daily_sales_summary` - Daily aggregated sales
- `product_performance` - Product-level performance metrics

---

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- Use strong database passwords in production
- Consider using connection encryption for production
- Review and restrict database user permissions

---

## 📈 Future Enhancements

- [ ] Add unit tests with pytest
- [ ] Implement incremental data loading
- [ ] Add Apache Airflow for orchestration
- [ ] Deploy to cloud (AWS/GCP)
- [ ] Add ML models for sales forecasting
- [ ] Create REST API with FastAPI
- [ ] Add Docker containerization
- [ ] Implement data quality checks (Great Expectations)
- [ ] Add interactive dashboards (Plotly/Dash)

---

## 📝 License

This project is open source and available for educational purposes.

---

## 👤 Author

Created as part of a data engineering/data science portfolio project.

---

## 🙏 Acknowledgments

- Built with Python, Pandas, MySQL, Matplotlib, and Seaborn
- Follows industry best practices for ETL pipelines

---

**Happy Analyzing! 📊**


