import streamlit as st
from predict import predict_spam
from database import save_result

# -----------------------------------
# Page Setup
# -----------------------------------

st.set_page_config(
    page_title="AI Multi-Platform Spam Detector",
    layout="wide"
)

st.title("🛡 AI Fake Review & Spam Detector")

# -----------------------------------
# Platform Selection
# -----------------------------------

platform = st.selectbox(
    "Select Platform",
    [
        "YouTube",
        "Instagram",
        "Email",
        "SMS",
        "Website Review",
        "WhatsApp"
    ]
)

# -----------------------------------
# Default Text Variable
# -----------------------------------

text = ""

# -----------------------------------
# Common Input Dictionary
# -----------------------------------

input_data = {
    'link_count': 0,
    'emoji_count': 0,
    'hashtag_count': 0,
    'follower_ratio': 0,
    'duplicate_score': 0,
    'forward_count': 0,
    'urgent_words': 0,
    'rating': 0,
    'account_age_days': 0
}

# ===================================
# YouTube Inputs
# ===================================

if platform == "YouTube":

    st.subheader("📺 YouTube Comment Detection")

    text = st.text_area("Comment")

    input_data['link_count'] = st.number_input(
        "Link Count",
        min_value=0
    )

    input_data['emoji_count'] = st.number_input(
        "Emoji Count",
        min_value=0
    )

    input_data['account_age_days'] = st.number_input(
        "Channel Age (Days)",
        min_value=0
    )

# ===================================
# Instagram Inputs
# ===================================

elif platform == "Instagram":

    st.subheader("📸 Instagram Fake Detection")

    text = st.text_area("Caption")

    input_data['hashtag_count'] = st.number_input(
        "Hashtag Count",
        min_value=0
    )

    followers = st.number_input(
        "Followers",
        min_value=0
    )

    following = st.number_input(
        "Following",
        min_value=1
    )

    input_data['follower_ratio'] = followers / following

# ===================================
# Email Inputs
# ===================================

elif platform == "Email":

    st.subheader("📧 Email Phishing Detection")

    subject = st.text_input("Email Subject")

    body = st.text_area("Email Body")

    text = subject + " " + body

    input_data['link_count'] = st.number_input(
        "Suspicious Links",
        min_value=0
    )

    input_data['urgent_words'] = st.number_input(
        "Urgent Words Count",
        min_value=0
    )

# ===================================
# SMS Inputs
# ===================================

elif platform == "SMS":

    st.subheader("📱 SMS Scam Detection")

    text = st.text_area("SMS Message")

    input_data['link_count'] = st.number_input(
        "URL Count",
        min_value=0
    )

    input_data['urgent_words'] = st.number_input(
        "Prize/Urgent Keywords",
        min_value=0
    )

# ===================================
# Website Review Inputs
# ===================================

elif platform == "Website Review":

    st.subheader("🌐 Fake Review Detection")

    text = st.text_area("Review")

    input_data['rating'] = st.slider(
        "Rating",
        1,
        5
    )

    input_data['duplicate_score'] = st.slider(
        "Duplicate Review Score",
        0.0,
        1.0
    )

# ===================================
# WhatsApp Inputs
# ===================================

elif platform == "WhatsApp":

    st.subheader("💬 WhatsApp Scam Detection")

    text = st.text_area("WhatsApp Message")

    input_data['forward_count'] = st.number_input(
        "Forward Count",
        min_value=0
    )

    input_data['link_count'] = st.number_input(
        "Suspicious Links",
        min_value=0
    )

# ===================================
# Prediction
# ===================================

if st.button("Detect Spam"):

    if text.strip() == "":

        st.warning("Please enter text")

    else:

        result, confidence = predict_spam(input_data)

        st.subheader(f"Prediction: {result}")

        st.write(f"Confidence Score: {confidence:.2f}")

        save_data = {
            'platform': platform,
            'text': text,
            'prediction': result,
            'confidence': confidence,
            'link_count': input_data['link_count'],
            'emoji_count': input_data['emoji_count'],
            'hashtag_count': input_data['hashtag_count'],
            'follower_ratio': input_data['follower_ratio'],
            'duplicate_score': input_data['duplicate_score'],
            'forward_count': input_data['forward_count'],
            'urgent_words': input_data['urgent_words'],
            'rating': input_data['rating'],
            'account_age_days': input_data['account_age_days']
        }

        save_result(save_data)

        st.success("Prediction Saved Successfully")

        if confidence > 0.8:
            st.error("⚠ High Risk Spam")

        elif confidence > 0.5:
            st.warning("⚠ Medium Risk")

        else:
            st.success("✅ Genuine Content")