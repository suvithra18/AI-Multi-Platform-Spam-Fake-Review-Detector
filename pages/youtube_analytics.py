import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Setup
# ---------------------------------

st.set_page_config(
    page_title="YouTube Analytics",
    layout="wide"
)

st.title("📺 YouTube Spam Analytics")

# ---------------------------------
# Database Connection
# ---------------------------------

conn = sqlite3.connect(
    "database/spam_results.db"
)

# ---------------------------------
# Load YouTube Data
# ---------------------------------

df = pd.read_sql(

    """
    SELECT * FROM results
    WHERE platform='YouTube'
    """,

    conn
)

# ---------------------------------
# Empty Check
# ---------------------------------

if df.empty:

    st.warning(
        "No YouTube data found"
    )

    st.stop()

# ---------------------------------
# Metrics
# ---------------------------------

total_comments = len(df)

spam_comments = len(

    df[df['prediction'] == 'Spam/Fake']
)

genuine_comments = len(

    df[df['prediction'] == 'Genuine']
)

avg_links = round(

    df['link_count'].mean(),
    2
)

# ---------------------------------
# Metrics Cards
# ---------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Comments",
    total_comments
)

col2.metric(
    "Spam Comments",
    spam_comments
)

col3.metric(
    "Genuine Comments",
    genuine_comments
)

col4.metric(
    "Average Links",
    avg_links
)

st.divider()

# ---------------------------------
# Spam Distribution
# ---------------------------------

chart_df = pd.DataFrame({

    "Category": [

        "Spam/Fake",
        "Genuine"
    ],

    "Count": [

        spam_comments,
        genuine_comments
    ]
})

fig = px.pie(

    chart_df,

    names="Category",

    values="Count",

    hole=0.4,

    title="YouTube Spam Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------
# Emoji Usage Analysis
# ---------------------------------

st.subheader(
    "😀 Emoji Usage Analysis"
)

emoji_fig = px.histogram(

    df,

    x='emoji_count',

    nbins=15,

    title="Emoji Count Distribution"
)

st.plotly_chart(
    emoji_fig,
    use_container_width=True
)

# ---------------------------------
# Link Count Analysis
# ---------------------------------

st.subheader(
    "🔗 Suspicious Link Analysis"
)

link_fig = px.box(

    df,

    y='link_count',

    title="Link Count Distribution"
)

st.plotly_chart(
    link_fig,
    use_container_width=True
)

# ---------------------------------
# Spam Comments Table
# ---------------------------------

st.subheader(
    "🚨 Spam Comments"
)

spam_df = df[
    df['prediction'] == 'Spam/Fake'
]

st.dataframe(
    spam_df[
        [

            'text',

            'link_count',

            'emoji_count',

            'account_age_days',

            'confidence'
        ]
    ],

    use_container_width=True
)

# ---------------------------------
# Download CSV
# ---------------------------------

csv = df.to_csv(index=False)

st.download_button(

    label="⬇ Download YouTube Analytics",

    data=csv,

    file_name="youtube_analytics.csv",

    mime="text/csv"
)