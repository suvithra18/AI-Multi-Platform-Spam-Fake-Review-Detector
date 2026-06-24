import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="Website Review Analytics",

    layout="wide"
)

st.title("🌐 Website Fake Review Analytics Dashboard")

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# -----------------------------------
# Load Website Review Data
# -----------------------------------

query = """

SELECT * FROM results

WHERE platform='Website Review'

"""

df = pd.read_sql(
    query,
    conn
)

# -----------------------------------
# Empty Data Check
# -----------------------------------

if df.empty:

    st.warning(
        "No Website Review data found."
    )

    st.stop()

# -----------------------------------
# Metrics Calculation
# -----------------------------------

total_reviews = len(df)

fake_reviews = len(

    df[df['prediction'] == 'Spam/Fake']
)

genuine_reviews = len(

    df[df['prediction'] == 'Genuine']
)

avg_rating = round(

    df['rating'].mean(),
    2
)

avg_duplicate_score = round(

    df['duplicate_score'].mean(),
    2
)

avg_confidence = round(

    df['confidence'].mean() * 100,
    2
)

fake_percentage = round(

    (fake_reviews / total_reviews) * 100,
    2
)

# -----------------------------------
# Metric Cards
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Reviews",
    total_reviews
)

col2.metric(
    "Fake Reviews",
    fake_reviews
)

col3.metric(
    "Genuine Reviews",
    genuine_reviews
)

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric(
    "Average Rating",
    avg_rating
)

col5.metric(
    "Avg Duplicate Score",
    avg_duplicate_score
)

col6.metric(
    "Avg Confidence",
    f"{avg_confidence}%"
)

st.divider()

# -----------------------------------
# Fake vs Genuine Distribution
# -----------------------------------

st.subheader(
    "🟢 Fake vs Genuine Review Distribution"
)

distribution_df = pd.DataFrame({

    "Category": [

        "Fake Reviews",
        "Genuine Reviews"
    ],

    "Count": [

        fake_reviews,
        genuine_reviews
    ]
})

pie_fig = px.pie(

    distribution_df,

    names="Category",

    values="Count",

    hole=0.4,

    title="Website Review Distribution"
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# -----------------------------------
# Rating Analysis
# -----------------------------------

st.subheader(
    "⭐ Rating Distribution"
)

rating_fig = px.histogram(

    df,

    x='rating',

    nbins=5,

    title="Review Rating Distribution"
)

st.plotly_chart(
    rating_fig,
    use_container_width=True
)

# -----------------------------------
# Duplicate Score Analysis
# -----------------------------------

st.subheader(
    "📄 Duplicate Review Score Analysis"
)

duplicate_fig = px.box(

    df,

    y='duplicate_score',

    title="Duplicate Score Distribution"
)

st.plotly_chart(
    duplicate_fig,
    use_container_width=True
)

# -----------------------------------
# Confidence Distribution
# -----------------------------------

st.subheader(
    "🎯 Prediction Confidence Distribution"
)

confidence_fig = px.histogram(

    df,

    x='confidence',

    nbins=20,

    title="Confidence Score Distribution"
)

st.plotly_chart(
    confidence_fig,
    use_container_width=True
)

# -----------------------------------
# Fake Review Risk Gauge
# -----------------------------------

st.subheader(
    "⚠ Fake Review Risk Gauge"
)

gauge_fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=fake_percentage,

        title={
            'text': "Fake Review Percentage"
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'thickness': 0.3
            },

            'steps': [

                {
                    'range': [0, 30],
                    'color': "lightgreen"
                },

                {
                    'range': [30, 70],
                    'color': "yellow"
                },

                {
                    'range': [70, 100],
                    'color': "red"
                }
            ]
        }
    )
)

st.plotly_chart(
    gauge_fig,
    use_container_width=True
)

# -----------------------------------
# Fake Reviews Table
# -----------------------------------

st.subheader(
    "🚨 Detected Fake Reviews"
)

fake_df = df[
    df['prediction'] == 'Spam/Fake'
]

st.dataframe(

    fake_df[

        [

            'text',

            'rating',

            'duplicate_score',

            'confidence'
        ]
    ],

    use_container_width=True
)

# -----------------------------------
# Recent Reviews
# -----------------------------------

st.subheader(
    "📝 Recent Website Reviews"
)

recent_df = df.tail(10)

st.dataframe(

    recent_df[

        [

            'text',

            'prediction',

            'rating',

            'duplicate_score',

            'confidence'
        ]
    ],

    use_container_width=True
)

# -----------------------------------
# Download Analytics CSV
# -----------------------------------

csv = df.to_csv(index=False)

st.download_button(

    label="⬇ Download Website Review Analytics",

    data=csv,

    file_name="website_review_analytics.csv",

    mime="text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "Website Review Analytics Loaded Successfully"
)