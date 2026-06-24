import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="Email Phishing Analytics",

    layout="wide"
)

st.title("📧 Email Phishing & Spam Analytics Dashboard")

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# -----------------------------------
# Load Email Data
# -----------------------------------

query = """

SELECT * FROM results

WHERE platform='Email'

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
        "No Email analytics data found."
    )

    st.stop()

# -----------------------------------
# Metrics Calculation
# -----------------------------------

total_emails = len(df)

spam_emails = len(

    df[df['prediction'] == 'Spam/Fake']
)

genuine_emails = len(

    df[df['prediction'] == 'Genuine']
)

avg_links = round(

    df['link_count'].mean(),
    2
)

avg_urgent_words = round(

    df['urgent_words'].mean(),
    2
)

avg_confidence = round(

    df['confidence'].mean() * 100,
    2
)

spam_percentage = round(

    (spam_emails / total_emails) * 100,
    2
)

# -----------------------------------
# Metric Cards
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Emails",
    total_emails
)

col2.metric(
    "Phishing/Spam Emails",
    spam_emails
)

col3.metric(
    "Genuine Emails",
    genuine_emails
)

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric(
    "Avg Suspicious Links",
    avg_links
)

col5.metric(
    "Avg Urgent Words",
    avg_urgent_words
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
    "🟢 Phishing vs Genuine Email Distribution"
)

distribution_df = pd.DataFrame({

    "Category": [

        "Spam/Fake",
        "Genuine"
    ],

    "Count": [

        spam_emails,
        genuine_emails
    ]
})

pie_fig = px.pie(

    distribution_df,

    names="Category",

    values="Count",

    hole=0.4,

    title="Email Spam Distribution"
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# -----------------------------------
# Suspicious Link Analysis
# -----------------------------------

st.subheader(
    "🔗 Suspicious Link Analysis"
)

link_fig = px.histogram(

    df,

    x='link_count',

    nbins=15,

    title="Suspicious Link Distribution"
)

st.plotly_chart(
    link_fig,
    use_container_width=True
)

# -----------------------------------
# Urgent Word Analysis
# -----------------------------------

st.subheader(
    "⚠ Urgency Keyword Analysis"
)

urgent_fig = px.box(

    df,

    y='urgent_words',

    title="Urgent Word Distribution"
)

st.plotly_chart(
    urgent_fig,
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
# Email Risk Gauge
# -----------------------------------

st.subheader(
    "⚠ Email Phishing Risk Gauge"
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
# Detected Phishing Emails Table
# -----------------------------------

st.subheader(
    "🚨 Detected Phishing Emails"
)

spam_df = df[
    df['prediction'] == 'Spam/Fake'
]

st.dataframe(

    spam_df[

        [

            'text',

            'link_count',

            'urgent_words',

            'confidence'
        ]
    ],

    use_container_width=True
)

# -----------------------------------
# Recent Email Activity
# -----------------------------------

st.subheader(
    "📝 Recent Email Activity"
)

recent_df = df.tail(10)

st.dataframe(

    recent_df[

        [

            'text',

            'prediction',

            'link_count',

            'urgent_words',

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

    label="⬇ Download Email Analytics",

    data=csv,

    file_name="email_analytics.csv",

    mime="text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "Email Analytics Loaded Successfully"
)