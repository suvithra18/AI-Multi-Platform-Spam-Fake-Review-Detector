import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="Detection History",

    layout="wide"
)

st.title("📜 Spam Detection History")

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# -----------------------------------
# Load Data
# -----------------------------------

query = """

SELECT * FROM results
ORDER BY id DESC

"""

df = pd.read_sql(
    query,
    conn
)

# -----------------------------------
# Empty Check
# -----------------------------------

if df.empty:

    st.warning(
        "No detection history found."
    )

    st.stop()

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header("🔍 Filter History")

platform_filter = st.sidebar.multiselect(

    "Select Platform",

    options=df['platform'].unique(),

    default=df['platform'].unique()
)

prediction_filter = st.sidebar.multiselect(

    "Select Prediction",

    options=df['prediction'].unique(),

    default=df['prediction'].unique()
)

# -----------------------------------
# Apply Filters
# -----------------------------------

filtered_df = df[

    (df['platform'].isin(platform_filter)) &

    (df['prediction'].isin(prediction_filter))
]

# -----------------------------------
# Metrics
# -----------------------------------

total_records = len(filtered_df)

spam_count = len(

    filtered_df[
        filtered_df['prediction'] == 'Spam/Fake'
    ]
)

genuine_count = len(

    filtered_df[
        filtered_df['prediction'] == 'Genuine'
    ]
)

avg_confidence = round(

    filtered_df['confidence'].mean() * 100,
    2
)

# -----------------------------------
# Metric Cards
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    total_records
)

col2.metric(
    "Spam/Fake",
    spam_count
)

col3.metric(
    "Genuine",
    genuine_count
)

col4.metric(
    "Avg Confidence",
    f"{avg_confidence}%"
)

st.divider()

# -----------------------------------
# Platform Distribution
# -----------------------------------

st.subheader(
    "📊 Platform Distribution"
)

platform_chart = px.histogram(

    filtered_df,

    x='platform',

    color='prediction',

    barmode='group',

    title="Platform-wise Detection"
)

st.plotly_chart(
    platform_chart,
    use_container_width=True
)

# -----------------------------------
# Prediction Distribution
# -----------------------------------

st.subheader(
    "🟢 Spam vs Genuine Distribution"
)

prediction_counts = filtered_df[
    'prediction'
].value_counts().reset_index()

prediction_counts.columns = [

    'Prediction',
    'Count'
]

pie_chart = px.pie(

    prediction_counts,

    names='Prediction',

    values='Count',

    hole=0.4
)

st.plotly_chart(
    pie_chart,
    use_container_width=True
)

# -----------------------------------
# Confidence Analysis
# -----------------------------------

st.subheader(
    "🎯 Confidence Score Analysis"
)

confidence_chart = px.histogram(

    filtered_df,

    x='confidence',

    nbins=20,

    color='prediction',

    title="Confidence Distribution"
)

st.plotly_chart(
    confidence_chart,
    use_container_width=True
)

# -----------------------------------
# Detection History Table
# -----------------------------------

st.subheader(
    "📋 Detection Records"
)

display_columns = [

    'platform',

    'text',

    'prediction',

    'confidence',

    'link_count',

    'emoji_count',

    'hashtag_count',

    'follower_ratio',

    'duplicate_score',

    'forward_count',

    'urgent_words',

    'rating',

    'account_age_days'
]

st.dataframe(

    filtered_df[display_columns],

    use_container_width=True
)

# -----------------------------------
# Search Text
# -----------------------------------

st.subheader(
    "🔎 Search Messages"
)

search_text = st.text_input(
    "Search by text"
)

if search_text:

    search_df = filtered_df[

        filtered_df['text'].str.contains(

            search_text,

            case=False,

            na=False
        )
    ]

    st.dataframe(
        search_df,
        use_container_width=True
    )

# -----------------------------------
# Download CSV
# -----------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(

    label="⬇ Download History CSV",

    data=csv,

    file_name="spam_detection_history.csv",

    mime="text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "Detection History Loaded Successfully"
)