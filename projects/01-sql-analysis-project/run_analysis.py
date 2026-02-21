import sqlite3
import pandas as pd
import os

def run_sql_analysis():
    print("Starting SQL Analysis Project...")
    
    # Define database path
    db_path = 'sales_analysis.db'
    
    # 1. Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. Read and execute schema
    print("Creating schema and inserting data...")
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    # 3. Run analytical queries and show results with Pandas
    print("\nExecuting analytical queries...")
    
    # Query 1: Revenue per product
    query1 = """
    SELECT p.product_name, SUM(s.quantity * p.price) as total_revenue
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    GROUP BY p.product_name
    ORDER BY total_revenue DESC;
    """
    df1 = pd.read_sql_query(query1, conn)
    print("\nRevenue per Product:")
    print(df1)
    
    # Query 2: Top Category
    query2 = """
    SELECT p.category, SUM(s.quantity) as total_quantity
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    GROUP BY p.category
    ORDER BY total_quantity DESC
    LIMIT 1;
    """
    df2 = pd.read_sql_query(query2, conn)
    print("\nTop Selling Category:")
    print(df2)
    
    conn.close()
    print(f"\nAnalysis complete. Database saved to {db_path}")

if __name__ == "__main__":
    run_sql_analysis()
