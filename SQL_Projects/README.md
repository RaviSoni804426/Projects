# 📊 SQL Exploratory Data Analysis (EDA) Workspace

Welcome to your simplified SQL workspace! This project allows you to perform professional-grade data analysis using SQL directly on CSV files.

---

## 🚀 Quick Start
1.  **Setup**: Run `setup_sql_project.bat` to install the requirements (`duckdb`, `pandas`).
2.  **Analyze**: Open **`YouTube_EDA.ipynb`** in VS Code.
3.  **Run**: Select your Python kernel and run all cells to see the results.

---

## 📂 Project Structure
- **`YouTube_EDA.ipynb`**: Your main analysis notebook.
- **`data/`**: Folder containing your CSV datasets.
- **`setup_sql_project.bat`**: Setup script for beginners.

---

## 🛠️ How to Create Your Own SQL Project
1.  **Dataset**: Drop your CSV file into the `data/` folder.
2.  **SQL Engine**: We use **DuckDB** because it's serverless and queries files directly.
3.  **Querying**: Use the following pattern in a notebook:
    ```python
    import duckdb
    con = duckdb.connect()
    # Query your file
    df = con.execute("SELECT * FROM 'data/your_file.csv' LIMIT 5").df()
    ```
4.  **Analyze**: Use SQL basics like `GROUP BY`, `ORDER BY`, and `AVG` to find patterns.

---

## 💡 SQL Tips for EDA
- **Use `LIMIT 10`**: Don't load massive files all at once while testing.
- **Check for Nulls**: `SELECT COUNT(*) FROM table WHERE column IS NULL;`
- **Engagement**: Always calculate ratios (e.g., `likes/views`) to see true performance.
- **Be Portfolio Ready**: Add a short summary/conclusion after every query in the notebook.

---
Happy Querying! 🚀
