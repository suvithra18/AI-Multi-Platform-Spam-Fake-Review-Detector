from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

vectorizer = TfidfVectorizer(max_features=5000)

def fit_vectorizer(texts):

    X = vectorizer.fit_transform(texts)

    joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

    return X

def transform_text(texts):

    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

    return vectorizer.transform(texts)