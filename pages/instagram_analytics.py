import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="Instagram Analytics",

    layout="wide"
)

st.title("📸 Instagram Fake Account & Spam Analytics")

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# -----------------------------------
# Load Instagram Data
# -----------------------------------

query = """

SELECT * FROM results

WHERE platform='Instagram'

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
        "No Instagram analytics data found."
    )

    st.stop()

# -----------------------------------
# Metrics Calculation
# -----------------------------------

total_posts = len(df)

spam_posts = len(

    df[df['prediction'] == 'Spam/Fake']
)

genuine_posts = len(

    df[df['prediction'] == 'Genuine']
)

avg_hashtags = round(

    df['hashtag_count'].mean(),
    2
)

avg_follower_ratio = round(

    df['follower_ratio'].mean(),
    2
)

avg_confidence = round(

    df['confidence'].mean() * 100,
    2
)

spam_percentage = round(

    (spam_posts / total_posts) * 100,
    2
)

# -----------------------------------
# Metric Cards
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Posts",
    total_posts
)

col2.metric(
    "Spam/Fake Posts",
    spam_posts
)

col3.metric(
    "Genuine Posts",
    genuine_posts
)

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric(
    "Avg Hashtag Count",
    avg_hashtags
)

col5.metric(
    "Avg Follower Ratio",
    avg_follower_ratio
)

col6.metric(
    "Avg Confidence",
    f"{avg_confidence}%"
)

st.divider()

# -----------------------------------
# Spam Distribution Pie Chart
# -----------------------------------

st.subheader(
    "🟢 Spam vs Genuine Distribution"
)

distribution_df = pd.DataFrame({

    "Category": [

        "Spam/Fake",
        "Genuine"
    ],

    "Count": [

        spam_posts,
        genuine_posts
    ]
})

pie_fig = px.pie(

    distribution_df,

    names="Category",

    values="Count",

    hole=0.4,

    title="Instagram Spam Distribution"
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# -----------------------------------
# Hashtag Analysis
# -----------------------------------

st.subheader(
    "#️⃣ Hashtag Usage Analysis"
)

hashtag_fig = px.histogram(

    df,

    x='hashtag_count',

    nbins=20,

    title="Hashtag Count Distribution"
)

st.plotly_chart(
    hashtag_fig,
    use_container_width=True
)

# -----------------------------------
# Follower Ratio Analysis
# -----------------------------------

st.subheader(
    "👥 Follower Ratio Analysis"
)

ratio_fig = px.box(

    df,

    y='follower_ratio',

    title="Follower Ratio Distribution"
)

st.plotly_chart(
    ratio_fig,
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
# Spam Risk Gauge
# -----------------------------------

st.subheader(
    "⚠ Instagram Spam Risk Gauge"
)

gauge_fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=spam_percentage,

        title={
            'text': "Spam Percentage"
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
# Spam/Fake Posts Table
# -----------------------------------

st.subheader(
    "🚨 Detected Spam/Fake Instagram Posts"
)

spam_df = df[
    df['prediction'] == 'Spam/Fake'
]

st.dataframe(

    spam_df[

        [

            'text',

            'hashtag_count',

            'follower_ratio',

            'confidence'
        ]
    ],

    use_container_width=True
)

# -----------------------------------
# Recent Instagram Posts
# -----------------------------------

st.subheader(
    "📝 Recent Instagram Activity"
)

recent_df = df.tail(10)

st.dataframe(

    recent_df[

        [

            'text',

            'prediction',

            'hashtag_count',

            'follower_ratio',

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

    label="⬇ Download Instagram Analytics",

    data=csv,

    file_name="instagram_analytics.csv",

    mime="text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "Instagram Analytics Loaded Successfully"
)