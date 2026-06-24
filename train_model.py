import pandas as pd
import joblib
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from utils.feature_builder import build_features

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv(
    "dataset/spam_dataset.csv"
)

# -----------------------------------
# Build Features
# -----------------------------------

X = build_features(df)

# Labels
y = df['label']

# -----------------------------------
# Feature Scaling
# -----------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(
    scaler,
    "models/scaler.pkl"
)

# -----------------------------------
# Train Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X_scaled,
    y,

    test_size=0.2,

    random_state=42
)

# -----------------------------------
# Neural Network Model
# -----------------------------------

model = tf.keras.Sequential([

    tf.keras.layers.Dense(

        64,

        activation='relu',

        input_shape=(X_train.shape[1],)
    ),

    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(

        32,

        activation='relu'
    ),

    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(

        1,

        activation='sigmoid'
    )
])

# -----------------------------------
# Compile Model
# -----------------------------------

model.compile(

    optimizer='adam',

    loss='binary_crossentropy',

    metrics=['accuracy']
)

# -----------------------------------
# Train Model
# -----------------------------------

history = model.fit(

    X_train,

    y_train,

    validation_data=(X_test, y_test),

    epochs=20,

    batch_size=32
)

# -----------------------------------
# Evaluate
# -----------------------------------

predictions = model.predict(X_test)

predictions = (predictions > 0.5).astype(int)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Model Accuracy: {accuracy:.2f}")

# -----------------------------------
# Save Model
# -----------------------------------

model.save(
    "models/spam_model.h5"
)

print("Model Saved Successfully")