import joblib
import pandas as pd
import tensorflow as tf

from utils.feature_builder import FEATURE_COLUMNS

# -----------------------------------
# Load Model
# -----------------------------------

model = tf.keras.models.load_model(
    "models/spam_model.h5"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

# -----------------------------------
# Prediction Function
# -----------------------------------

def predict_spam(input_data):

    # Convert to DataFrame
    df = pd.DataFrame([input_data])

    # Keep only feature columns
    X = df[FEATURE_COLUMNS]

    # Scale Features
    X_scaled = scaler.transform(X)

    # Predict
    prediction = model.predict(X_scaled)[0][0]

    # Result
    if prediction > 0.5:

        result = "Spam/Fake"

    else:

        result = "Genuine"

    return result, float(prediction)