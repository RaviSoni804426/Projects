import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="StockPulse | Intelligent Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Styling
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .decision-buy { color: #238636; font-weight: bold; font-size: 24px; }
    .decision-sell { color: #da3633; font-weight: bold; font-size: 24px; }
    .decision-hold { color: #8b949e; font-weight: bold; font-size: 24px; }
    .header-style { 
        background: linear-gradient(90deg, #1f6feb, #8e2de2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE LOGIC (ENGINE)
# ==========================================
class StockEngine:
    @staticmethod
    def fetch_data(symbol, period="1y"):
        """Fetch stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if df.empty:
                return None
            return df
        except Exception:
            return None

    @staticmethod
    def calculate_indicators(df):
        """Add technical indicators for analysis"""
        # Close Price (Latest)
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Volatility
        df['Volatility'] = df['Close'].pct_change().rolling(window=21).std() * np.sqrt(252)
        return df

    @staticmethod
    def get_decision(df):
        """Intelligent decision engine based on indicators"""
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        score = 0
        reasons = []
        
        # Trend Analysis
        if latest['Close'] > latest['SMA_20']:
            score += 20
            reasons.append("Price is above 20-Day SMA (Short-term Bullish)")
        
        if latest['SMA_20'] > latest['SMA_50']:
            score += 20
            reasons.append("Golden Cross formation (20 SMA > 50 SMA)")
        
        # momentum (RSI)
        if latest['RSI'] < 30:
            score += 30
            reasons.append("Oversold condition (RSI < 30) - Potential Reversal")
        elif latest['RSI'] > 70:
            score -= 20
            reasons.append("Overbought condition (RSI > 70) - Risk of Pullback")
        else:
            score += 10
            reasons.append(f"Neutral Momentum (RSI: {latest['RSI']:.1f})")
            
        # Volume Analysis
        if latest['Volume'] > df['Volume'].tail(20).mean() * 1.5:
            score += 20
            reasons.append("High Volume breakout detected")

        # Final Decision
        if score >= 60:
            decision = "BUY"
            confidence = min(score, 95)
        elif score <= 20:
            decision = "SELL"
            confidence = min(abs(score) + 40, 95)
        else:
            decision = "HOLD"
            confidence = 50 + (score // 2)
            
        return decision, confidence, reasons

# ==========================================
# 3. USER INTERFACE (UI)
# ==========================================
def main():
    # Sidebar Setup
    st.sidebar.markdown("# 🔧 Controls")
    symbol = st.sidebar.text_input("Enter NSE Stock Symbol", value="RELIANCE").upper()
    if not symbol.endswith(".NS") and "^" not in symbol:
        symbol += ".NS"
    
    period = st.sidebar.selectbox("Select Time Period", ["6mo", "1y", "2y", "5y"], index=1)
    
    st.markdown('<h1 class="header-style">StockPulse</h1>', unsafe_allow_html=True)
    st.markdown("### Intelligent Stock Analysis for Freshers & Professionals")
    st.divider()

    # App Logic
    if symbol:
        with st.spinner(f"Analyzing {symbol}..."):
            engine = StockEngine()
            data = engine.fetch_data(symbol, period)
            
            if data is not None and len(data) > 50:
                data = engine.calculate_indicators(data)
                decision, confidence, reasons = engine.get_decision(data)
                
                # Metrics Row
                col1, col2, col3, col4 = st.columns(4)
                latest_price = data['Close'].iloc[-1]
                change = latest_price - data['Close'].iloc[-2]
                pct_change = (change / data['Close'].iloc[-2]) * 100
                
                col1.metric("Current Price", f"₹{latest_price:,.2f}", f"{pct_change:+.2f}%")
                col2.metric("RSI (14)", f"{data['RSI'].iloc[-1]:.1f}")
                col3.metric("Volatility", f"{data['Volatility'].iloc[-1]*100:.1f}%")
                col4.metric("Decision", decision)

                # Decision Card
                st.markdown("---")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.subheader("Final Decision")
                    color = "decision-buy" if decision == "BUY" else "decision-sell" if decision == "SELL" else "decision-hold"
                    st.markdown(f'<span class="{color}">{decision}</span>', unsafe_allow_html=True)
                    st.write(f"**Confidence Level:** {confidence}%")
                    st.progress(confidence / 100)
                
                with c2:
                    st.subheader("Analysis Breakdown")
                    for r in reasons:
                        st.write(f"- {r}")

                # Charts
                st.markdown("---")
                st.subheader("Technical Chart")
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                   vertical_spacing=0.1, subplot_titles=('Price & Moving Averages', 'RSI Momentum'),
                                   row_width=[0.3, 0.7])

                # Candlestick
                fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                            low=data['Low'], close=data['Close'], name="Price"), row=1, col=1)
                
                # SMAs
                fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1), name="SMA 20"), row=1, col=1)
                fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], line=dict(color='cyan', width=1), name="SMA 50"), row=1, col=1)
                
                # RSI
                fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='magenta', width=1), name="RSI"), row=2, col=1)
                fig.add_trace(go.Scatter(x=data.index, y=[70]*len(data), line=dict(color='red', width=1, dash='dash'), name="Overbought"), row=2, col=1)
                fig.add_trace(go.Scatter(x=data.index, y=[30]*len(data), line=dict(color='green', width=1, dash='dash'), name="Oversold"), row=2, col=1)

                fig.update_layout(height=600, template="plotly_dark", showlegend=False, 
                                  xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

                # Data Table
                with st.expander("View Raw Data"):
                    st.dataframe(data.tail(10), use_container_width=True)
            else:
                st.error("Data fetch failed. Please check the symbol (e.g., RELIANCE, TCS, INFY).")

    # Footer
    st.sidebar.divider()
    st.sidebar.info("Developed for Portfolio Showcase. \n\nDisclaimer: Not Financial Advice.")

if __name__ == "__main__":
    main()
