import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --------------------------------
# Page Setup
# --------------------------------

st.set_page_config(
    page_title="Platform Analytics",
    layout="wide"
)

st.title("📊 Platform-Based Spam Analytics")

# --------------------------------
# Database Connection
# --------------------------------

conn = sqlite3.connect(
    "database/spam_results.db",
    check_same_thread=False
)

# --------------------------------
# Load Data
# --------------------------------

df = pd.read_sql(
    "SELECT * FROM results",
    conn
)

# --------------------------------
# Empty Check
# --------------------------------

if df.empty:

    st.warning(
        "No analytics data found."
    )

    st.stop()

# --------------------------------
# Platform Selection
# --------------------------------

platforms = df['platform'].unique()

selected_platform = st.selectbox(

    "Choose Platform",

    platforms
)

# --------------------------------
# Filter Data
# --------------------------------

platform_df = df[
    df['platform'] == selected_platform
]

# --------------------------------
# Metrics
# --------------------------------

total = len(platform_df)

spam = len(
    platform_df[
        platform_df['prediction'] == 'Spam/Fake'
    ]
)

genuine = len(
    platform_df[
        platform_df['prediction'] == 'Genuine'
    ]
)

avg_confidence = round(
    platform_df['confidence'].mean() * 100,
    2
)

# --------------------------------
# Metric Cards
# --------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Messages",
    total
)

col2.metric(
    "Spam Messages",
    spam
)

col3.metric(
    "Genuine Messages",
    genuine
)

col4.metric(
    "Avg Confidence",
    f"{avg_confidence}%"
)

st.divider()

# --------------------------------
# Pie Chart
# --------------------------------

st.subheader(
    f"🟢 {selected_platform} Spam Distribution"
)

chart_df = pd.DataFrame({

    "Category": [
        "Spam/Fake",
        "Genuine"
    ],

    "Count": [
        spam,
        genuine
    ]
})

pie_fig = px.pie(

    chart_df,

    names="Category",

    values="Count",

    hole=0.4
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# --------------------------------
# Bar Chart
# --------------------------------

st.subheader(
    "📈 Detection Count"
)

bar_fig = px.bar(

    chart_df,

    x="Category",

    y="Count",

    text="Count"
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

# --------------------------------
# Confidence Histogram
# --------------------------------

st.subheader(
    "🎯 Confidence Distribution"
)

hist_fig = px.histogram(

    platform_df,

    x="confidence",

    nbins=20
)

st.plotly_chart(
    hist_fig,
    use_container_width=True
)

# --------------------------------
# Spam Messages Table
# --------------------------------

st.subheader(
    "🚨 Detected Spam Messages"
)

spam_df = platform_df[
    platform_df['prediction'] == 'Spam/Fake'
]

st.dataframe(
    spam_df,
    use_container_width=True
)

# --------------------------------
# Recent Predictions
# --------------------------------

st.subheader(
    "📝 Recent Predictions"
)

st.dataframe(
    platform_df.tail(10),
    use_container_width=True
)

# --------------------------------
# Download Button
# --------------------------------

csv = platform_df.to_csv(index=False)

st.download_button(

    label=f"⬇ Download {selected_platform} Analytics",

    data=csv,

    file_name=f"{selected_platform}_analytics.csv",

    mime="text/csv"
)