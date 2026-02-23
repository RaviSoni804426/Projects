import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page config
st.set_page_config(page_title="YouTube Trending Analysis", layout="wide")

st.title("📊 YouTube Trending Video Analysis")

# File Path
CSV_PATH = "trending_videos.csv"

if not os.path.exists(CSV_PATH):
    st.error(f"Data file '{CSV_PATH}' not found. Please run the data collection script first.")
else:
    # Load Data
    df = pd.read_csv(CSV_PATH)
    
    # Preprocessing
    df['description'].fillna('No description', inplace=True)
    df['published_at'] = pd.to_datetime(df['published_at'])
    
    # Sidebar Filters
    st.sidebar.header("Filters")
    channel_search = st.sidebar.text_input("Search Channel")
    if channel_search:
        df = df[df['channel_title'].str.contains(channel_search, case=False)]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Videos", len(df))
    col2.metric("Total Views", f"{df['view_count'].sum():,.0f}")
    col3.metric("Total Likes", f"{df['like_count'].sum():,.0f}")
    col4.metric("Avg Views", f"{df['view_count'].mean():,.0f}")

    # Data Display
    st.subheader("Trending Videos Data")
    st.dataframe(df[['title', 'channel_title', 'view_count', 'like_count', 'comment_count', 'published_at']].head(50), use_container_width=True)

    # Visualizations
    st.subheader("Engagement Distributions")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.histplot(df['view_count'], bins=30, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('View Count Distribution')
    
    sns.histplot(df['like_count'], bins=30, kde=True, ax=axes[1], color='green')
    axes[1].set_title('Like Count Distribution')
    
    sns.histplot(df['comment_count'], bins=30, kde=True, ax=axes[2], color='red')
    axes[2].set_title('Comment Count Distribution')
    
    st.pyplot(fig)

    # Correlation
    st.subheader("Correlation Heatmap")
    corr = df[['view_count', 'like_count', 'comment_count']].corr()
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax_corr)
    st.pyplot(fig_corr)

    # Top Channels
    st.subheader("Top Channels by View Count")
    top_channels = df.groupby('channel_title')['view_count'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_channels)
