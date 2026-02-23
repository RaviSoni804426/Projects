import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config
st.set_page_config(page_title="Mutual Fund Planner", layout="wide", page_icon="📈")

st.title("📈 Mutual Fund Investment Planner")
st.markdown("Analyze Nifty 50 stocks, evaluate risk/reward, and plan your long-term investments.")

# File Path
CSV_PATH = "nifty50_closing_prices.csv"

if not os.path.exists(CSV_PATH):
    st.error(f"Data file '{CSV_PATH}' not found.")
else:
    # Load Data
    data = pd.read_csv(CSV_PATH)
    data['Date'] = pd.to_datetime(data['Date'])
    data.fillna(method='ffill', inplace=True)
    
    # Sidebar - Stock Selection
    st.sidebar.header("Select Stocks")
    all_stocks = data.columns[1:]
    selected_stocks = st.sidebar.multiselect("Pick stocks for your portfolio:", all_stocks, default=["RELIANCE.NS", "TCS.NS", "INFY.NS"])

    if not selected_stocks:
        st.warning("Please select at least one stock to analyze.")
    else:
        # Performance Analysis
        st.subheader("Historical Performance")
        
        # Plot closing prices
        fig_prices = go.Figure()
        for stock in selected_stocks:
            fig_prices.add_trace(go.Scatter(x=data['Date'], y=data[stock], mode='lines', name=stock))
        
        fig_prices.update_layout(title="Closing Prices Over Time", xaxis_title="Date", yaxis_title="Price (INR)", template="plotly_dark")
        st.plotly_chart(fig_prices, use_container_width=True)

        # ROI and Volatility Calculation
        returns = data[selected_stocks].pct_change().dropna()
        avg_returns = returns.mean() * 100
        volatility = returns.std() * 100
        
        st.subheader("Risk-Reward Profile")
        metrics_df = pd.DataFrame({
            "Avg Daily Return (%)": avg_returns,
            "Volatility (Std Dev %)": volatility
        })
        st.table(metrics_df)

        # Investment Simulator
        st.divider()
        st.header("Investment Simulator (SIP)")
        col1, col2, col3 = st.columns(3)
        
        monthly_investment = col1.number_input("Monthly Investment (INR)", min_value=100, value=5000, step=500)
        investment_years = col2.slider("Investment Duration (Years)", 1, 30, 10)
        expected_annual_return = col3.slider("Expected Annual Return (%)", 5, 30, 15)

        # Calculation
        r = (expected_annual_return / 100) / 12
        n = investment_years * 12
        future_value = monthly_investment * (((1 + r)**n - 1) / r) * (1 + r)
        total_invested = monthly_investment * n
        wealth_gain = future_value - total_invested

        # Results Display
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Total Invested", f"₹{total_invested:,.0f}")
        res_col2.metric("Estimated Wealth Gain", f"₹{wealth_gain:,.0f}")
        res_col3.metric("Total Value", f"₹{future_value:,.0f}", delta=f"{wealth_gain/total_invested*100:.1f}%")

        # Wealth Growth Chart
        months = np.arange(1, n + 1)
        growth = [monthly_investment * (((1 + r)**m - 1) / r) * (1 + r) for m in months]
        invested_line = [monthly_investment * m for m in months]
        
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(x=months/12, y=growth, mode='lines', name='Total Value'))
        fig_growth.add_trace(go.Scatter(x=months/12, y=invested_line, mode='lines', name='Amount Invested', line=dict(dash='dash')))
        fig_growth.update_layout(title="Projected Wealth Growth", xaxis_title="Years", yaxis_title="Amount (INR)", template="plotly_dark")
        st.plotly_chart(fig_growth, use_container_width=True)
