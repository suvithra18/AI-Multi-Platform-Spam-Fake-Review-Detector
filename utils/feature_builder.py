import pandas as pd

FEATURE_COLUMNS = [

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

def build_features(df):

    X = df[FEATURE_COLUMNS]

    return X