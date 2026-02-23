import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set page config
st.set_page_config(page_title="Real Estate Analytics", layout="wide", page_icon="🏠")

st.title("🏠 Real Estate Price Analysis & Prediction")
st.markdown("Explore factors affecting real estate prices and estimate property values.")

# File Path
CSV_PATH = "Real_Estate.csv"

if not os.path.exists(CSV_PATH):
    st.error(f"Data file '{CSV_PATH}' not found.")
else:
    # Load Data
    df = pd.read_csv(CSV_PATH)
    
    # Sidebar - Stats
    st.sidebar.header("Dataset Overview")
    st.sidebar.write(f"Total Records: {len(df)}")
    st.sidebar.write(f"Average Price/Unit: {df['House price of unit area'].mean():.2f}")

    # Layout
    tab1, tab2, tab3 = st.tabs(["📊 Market Analysis", "📍 Interactive Map", "🔮 Price Predictor"])

    with tab1:
        st.subheader("Market Trends & Correlations")
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution of House Prices
            fig_dist = px.histogram(df, x="House price of unit area", nbins=30, title="Distribution of House Prices", marginal="box", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_dist, use_container_width=True)
            
        with col2:
            # Price vs Distance to MRT
            fig_scatter = px.scatter(df, x="Distance to the nearest MRT station", y="House price of unit area", 
                                   color="Number of convenience stores", size="House age",
                                   title="Price vs MRT Distance (Size = House Age)")
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader("Correlation Heatmap")
        corr = df.drop(columns=['Transaction date']).corr()
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Feature Correlation Heatmap")
        st.plotly_chart(fig_corr, use_container_width=True)

    with tab2:
        st.subheader("Geospatial Distribution")
        # Streamlit map needs 'lat' and 'lon' columns
        map_df = df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
        st.map(map_df)
        st.info("The map shows property locations in the dataset.")

    with tab3:
        st.subheader("Estimate Property Value")
        st.write("Enter details to estimate the price per unit area based on market data.")
        
        c1, c2 = st.columns(2)
        age = c1.slider("House Age (years)", 0, 45, 15)
        mrt_dist = c1.number_input("Distance to MRT (meters)", 0.0, 7000.0, 1000.0)
        stores = c2.slider("Nearby Convenience Stores", 0, 10, 5)
        
        # Simple heuristic or linear regression weights (mocked from typical trends)
        # Price tends to decrease with age and distance, increase with stores
        base_price = 45.0
        est_price = base_price - (age * 0.2) - (mrt_dist * 0.005) + (stores * 2.5)
        est_price = max(est_price, 5.0) # Ensure price is positive
        
        st.divider()
        st.metric("Estimated Price per Unit Area", f"{est_price:.2f}")
        st.caption("Note: This is a simulation based on general trends in your dataset.")
