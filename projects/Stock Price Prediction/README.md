# 📈 StockPulse: Intelligent Stock Analysis Dashboard

A professional-grade, clean, and efficient stock analysis tool built with Python. This project is designed for **Freshers** to showcase their skills in Data Analysis, Financial Logic, and Web Dashboard development.

## 🚀 Key Features
- **Real-time Data**: Fetches latest market data using Yahoo Finance API.
- **Technical Indicators**: Calculates SMA (20, 50), RSI (14), and Annualized Volatility.
- **Intelligent Decision Engine**: A logic-based scoring system that provides BUY/SELL/HOLD recommendations with a confidence percentage.
- **Interactive Visuals**: Gorgeous Candlestick charts and RSI momentum graphs using Plotly.
- **Premium UI**: Clean, Dark-themed interface optimized for readability.

## 📁 Simple Folder Structure
```text
Stock Price/
├── main.py            # Complete Logic (UI + Analytics Engine)
├── requirements.txt   # Project Dependencies
└── README.md          # Project Documentation
```

## 🛠️ Setup & Execution

1. **Clone the project** or copy the files.
2. **Install Dependencies**:
   Open terminal and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App**:
   ```bash
   streamlit run main.py
   ```

## 🧠 How the Engine Works
The dashboard uses a multi-factor scoring system:
1. **Trend Follow**: Checks if the price is above Moving Averages (Bullish/Bearish).
2. **Momentum**: Uses RSI to identify Oversold (Buy) or Overbought (Risk) zones.
3. **Volume**: Detects high-volume breakouts.
4. **Calculated Confidence**: Combines all factors into a final 0-100% confidence score.

## 💼 Skills Showcased
- **Python Programming**
- **Financial Analytics** (Quantitative Analysis)
- **Data Visualization** (Plotly, Streamlit)
- **Problem Solving** (Heuristic Engine Design)

---
*Disclaimer: This project is for educational and portfolio purposes only. It does not constitute financial advice.*
