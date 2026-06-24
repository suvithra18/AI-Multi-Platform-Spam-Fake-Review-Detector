import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="Overall Analytics",

    layout="wide"
)

st.title("🌍 Overall Multi-Platform Spam Analytics")

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# -----------------------------------
# Load Complete Dataset
# -----------------------------------

query = """

SELECT * FROM results

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
        "No analytics data found."
    )

    st.stop()

# -----------------------------------
# Metrics Calculation
# -----------------------------------

total_records = len(df)

spam_records = len(

    df[df['prediction'] == 'Spam/Fake']
)

genuine_records = len(

    df[df['prediction'] == 'Genuine']
)

avg_confidence = round(

    df['confidence'].mean() * 100,
    2
)

spam_percentage = round(

    (spam_records / total_records) * 100,
    2
)

platform_count = df['platform'].nunique()

# -----------------------------------
# Metric Cards
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Records",
    total_records
)

col2.metric(
    "Spam/Fake Records",
    spam_records
)

col3.metric(
    "Genuine Records",
    genuine_records
)

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric(
    "Spam Percentage",
    f"{spam_percentage}%"
)

col5.metric(
    "Avg Confidence",
    f"{avg_confidence}%"
)

col6.metric(
    "Platforms Monitored",
    platform_count
)

st.divider()

# -----------------------------------
# Platform Distribution
# -----------------------------------

st.subheader(
    "📊 Platform Distribution"
)

platform_df = df.groupby(
    'platform'
).size().reset_index(name='count')

platform_fig = px.bar(

    platform_df,

    x='platform',

    y='count',

    text='count',

    title="Records by Platform"
)

st.plotly_chart(
    platform_fig,
    use_container_width=True
)

# -----------------------------------
# Spam vs Genuine Distribution
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

        spam_records,
        genuine_records
    ]
})

pie_fig = px.pie(

    distribution_df,

    names='Category',

    values='Count',

    hole=0.4,

    title="Overall Spam Distribution"
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# -----------------------------------
# Platform Wise Spam Analysis
# -----------------------------------

st.subheader(
    "⚠ Platform Wise Spam Analysis"
)

platform_spam_df = df.groupby(

    ['platform', 'prediction']

).size().reset_index(name='count')

spam_fig = px.bar(

    platform_spam_df,

    x='platform',

    y='count',

    color='prediction',

    barmode='group',

    title="Platform Wise Spam Comparison"
)

st.plotly_chart(
    spam_fig,
    use_container_width=True
)

# -----------------------------------
# Confidence Score Distribution
# -----------------------------------

st.subheader(
    "🎯 Prediction Confidence Distribution"
)

confidence_fig = px.histogram(

    df,

    x='confidence',

    nbins=25,

    title="Confidence Score Distribution"
)

st.plotly_chart(
    confidence_fig,
    use_container_width=True
)

# -----------------------------------
# Platform Wise Average Confidence
# -----------------------------------

st.subheader(
    "📈 Platform Wise Average Confidence"
)

confidence_platform_df = df.groupby(

    'platform'

)['confidence'].mean().reset_index()

confidence_platform_fig = px.line(

    confidence_platform_df,

    x='platform',

    y='confidence',

    markers=True,

    title="Average Confidence by Platform"
)

st.plotly_chart(
    confidence_platform_fig,
    use_container_width=True
)

# -----------------------------------
# Spam Risk Gauge
# -----------------------------------

st.subheader(
    "🚨 Overall Spam Risk Gauge"
)

gauge_fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=spam_percentage,

        title={
            'text': "Overall Spam Percentage"
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
# Recent Activity Table
# -----------------------------------

st.subheader(
    "📝 Recent Platform Activity"
)

recent_df = df.tail(15)

st.dataframe(

    recent_df[

        [

            'platform',

            'text',

            'prediction',

            'confidence'
        ]
    ],

    use_container_width=True
)

# -----------------------------------
# Platform Filter
# -----------------------------------

st.subheader(
    "🔍 Filter Platform Data"
)

selected_platform = st.selectbox(

    "Choose Platform",

    df['platform'].unique()
)

filtered_df = df[
    df['platform'] == selected_platform
]

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------------
# Download Analytics CSV
# -----------------------------------

csv = df.to_csv(index=False)

st.download_button(

    label="⬇ Download Overall Analytics",

    data=csv,

    file_name="overall_analytics.csv",

    mime="text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "Overall Multi-Platform Analytics Loaded Successfully"
)