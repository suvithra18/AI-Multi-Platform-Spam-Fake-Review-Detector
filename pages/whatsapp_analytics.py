import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="WhatsApp Scam Analytics",

    layout="wide"
)

st.title("💬 WhatsApp Scam Analytics Dashboard")

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# -----------------------------------
# Load WhatsApp Data
# -----------------------------------

query = """

SELECT * FROM results

WHERE platform='WhatsApp'

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
        "No WhatsApp analytics data found."
    )

    st.stop()

# -----------------------------------
# Metrics Calculation
# -----------------------------------

total_messages = len(df)

spam_messages = len(

    df[df['prediction'] == 'Spam/Fake']
)

genuine_messages = len(

    df[df['prediction'] == 'Genuine']
)

avg_forward_count = round(

    df['forward_count'].mean(),
    2
)

avg_links = round(

    df['link_count'].mean(),
    2
)

avg_confidence = round(

    df['confidence'].mean() * 100,
    2
)

spam_percentage = round(

    (spam_messages / total_messages) * 100,
    2
)

# -----------------------------------
# Metric Cards
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Messages",
    total_messages
)

col2.metric(
    "Spam Messages",
    spam_messages
)

col3.metric(
    "Genuine Messages",
    genuine_messages
)

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric(
    "Avg Forward Count",
    avg_forward_count
)

col5.metric(
    "Avg Suspicious Links",
    avg_links
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

        spam_messages,
        genuine_messages
    ]
})

pie_fig = px.pie(

    distribution_df,

    names="Category",

    values="Count",

    hole=0.4,

    title="WhatsApp Scam Distribution"
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# -----------------------------------
# Forward Count Analysis
# -----------------------------------

st.subheader(
    "📤 Forward Count Analysis"
)

forward_fig = px.histogram(

    df,

    x='forward_count',

    nbins=20,

    title="Forward Count Distribution"
)

st.plotly_chart(
    forward_fig,
    use_container_width=True
)

# -----------------------------------
# Suspicious Link Analysis
# -----------------------------------

st.subheader(
    "🔗 Suspicious Link Analysis"
)

link_fig = px.box(

    df,

    y='link_count',

    title="Suspicious Link Distribution"
)

st.plotly_chart(
    link_fig,
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
    "⚠ WhatsApp Scam Risk Gauge"
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
# Spam Messages Table
# -----------------------------------

st.subheader(
    "🚨 Detected Scam Messages"
)

spam_df = df[
    df['prediction'] == 'Spam/Fake'
]

st.dataframe(

    spam_df[

        [

            'text',

            'forward_count',

            'link_count',

            'confidence'
        ]
    ],

    use_container_width=True
)

# -----------------------------------
# Recent WhatsApp Messages
# -----------------------------------

st.subheader(
    "📝 Recent WhatsApp Messages"
)

recent_df = df.tail(10)

st.dataframe(

    recent_df[

        [

            'text',

            'prediction',

            'forward_count',

            'link_count',

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

    label="⬇ Download WhatsApp Analytics",

    data=csv,

    file_name="whatsapp_analytics.csv",

    mime="text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "WhatsApp Analytics Loaded Successfully"
)