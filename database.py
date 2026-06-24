import sqlite3
import os

# -----------------------------------
# Create Database Folder
# -----------------------------------

os.makedirs(
    "database",
    exist_ok=True
)

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect(

    "database/spam_results.db",

    check_same_thread=False
)

cursor = conn.cursor()

# -----------------------------------
# Create Table
# -----------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS results (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    platform TEXT,

    text TEXT,

    prediction TEXT,

    confidence REAL,

    link_count INTEGER,

    emoji_count INTEGER,

    hashtag_count INTEGER,

    follower_ratio REAL,

    duplicate_score REAL,

    forward_count INTEGER,

    urgent_words INTEGER,

    rating INTEGER,

    account_age_days INTEGER
)

""")

conn.commit()

print("Database & Table Created Successfully")

# -----------------------------------
# Save Result Function
# -----------------------------------

def save_result(data):

    cursor.execute("""

    INSERT INTO results (

        platform,
        text,
        prediction,
        confidence,

        link_count,
        emoji_count,
        hashtag_count,
        follower_ratio,
        duplicate_score,
        forward_count,
        urgent_words,
        rating,
        account_age_days

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data['platform'],
        data['text'],
        data['prediction'],
        data['confidence'],

        data['link_count'],
        data['emoji_count'],
        data['hashtag_count'],
        data['follower_ratio'],
        data['duplicate_score'],
        data['forward_count'],
        data['urgent_words'],
        data['rating'],
        data['account_age_days']
    ))

    conn.commit()

    print("Data Saved Successfully")