# 🛡 AI Multi-Platform Spam & Fake Review Detector

## 📌 Project Overview

The AI Multi-Platform Spam & Fake Review Detector is a Machine Learning-based web application developed using Streamlit.
It detects spam, phishing, fake reviews, and scam messages across multiple online platforms such as YouTube, Instagram, Email, SMS, Website Reviews, and WhatsApp.

The system analyzes various behavioral and textual features to classify content as either genuine or spam.

---

# 🚀 Features

* ✅ YouTube Spam Detection
* ✅ Instagram Fake Content Detection
* ✅ Email Phishing Detection
* ✅ SMS Scam Detection
* ✅ Website Fake Review Detection
* ✅ WhatsApp Scam Detection
* ✅ Confidence Score Prediction
* ✅ Risk Level Classification
* ✅ SQLite Database Storage
* ✅ Interactive Streamlit Dashboard

---

# 🧠 Technologies Used

| Technology   | Purpose              |
| ------------ | -------------------- |
| Python       | Backend Development  |
| Streamlit    | Web Application      |
| Pandas       | Data Processing      |
| Scikit-learn | Machine Learning     |
| SQLite       | Database Storage     |
| Joblib       | Model Saving/Loading |

---

# 📂 Project Structure

```bash
AI-Spam-Detector/
│
├── app.py
├── predict.py
├── database.py
├── train_model.py
├── spam_dataset.csv
├── model.pkl
├── requirements.txt
└── README.md
```

---

# ⚙ Installation Steps

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI-Spam-Detector.git
```

## 2️⃣ Open Project Folder

```bash
cd AI-Spam-Detector
```

## 3️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Application

```bash
streamlit run app.py
```

After running the command, the application will open in your browser.

---

# 📊 Dataset Features

| Feature          | Description                  |
| ---------------- | ---------------------------- |
| platform         | Social platform type         |
| text             | User message/review          |
| link_count       | Number of links              |
| emoji_count      | Number of emojis             |
| hashtag_count    | Number of hashtags           |
| follower_ratio   | Followers vs following ratio |
| duplicate_score  | Similarity score             |
| forward_count    | Message forward count        |
| urgent_words     | Scam-related keywords        |
| rating           | User review rating           |
| account_age_days | Account age                  |
| label            | Spam or Genuine              |

---

# 🧪 Machine Learning Workflow

1. Data Collection
2. Data Preprocessing
3. Feature Engineering
4. Model Training
5. Prediction
6. Database Storage
7. Result Visualization

---

# 💾 Database Functionality

The application stores:

* Platform Name
* Input Text
* Prediction Result
* Confidence Score
* Feature Values

using SQLite database for future analysis.

---


# 🔮 Future Enhancements

* NLP Sentiment Analysis
* Deep Learning Integration
* Real-Time Spam API
* Advanced Dashboard Analytics
* PDF Report Generation
* User Authentication System

---

# 📸 Screenshots

## Home Page

Add screenshot here

## Prediction Result

Add screenshot here

---

# 👩‍💻 Author

