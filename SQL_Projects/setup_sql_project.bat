@echo off
echo ==========================================
echo 🛠️  SQL EDA Workspace Initializer
echo ==========================================

:: Check if venv exists
if not exist "..\venv" (
    echo ❌ Virtual environment not found in parent directory.
    echo Please run setup_env.bat in the root folder first.
    pause
    exit /b
)

echo 📦 Installing required SQL tools...
..\venv\Scripts\pip install duckdb pandas sqlalchemy ipython-sql

echo ✅ Setup complete!
echo 💡 To start analyzing, open YouTube_EDA.ipynb
pause
