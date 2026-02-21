@echo off
echo [1/4] Creating virtual environment...
python -m venv venv

echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip

echo [4/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Setup complete! Virtual environment 'venv' is ready.
echo To activate it, run: venv\Scripts\activate
pause
