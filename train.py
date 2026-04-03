import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Features & target
X = df.drop("Class", axis=1)

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, "model/scaler.pkl")

# -------------------------------
# Isolation Forest
# -------------------------------
iso = IsolationForest(contamination=0.001)
iso.fit(X_scaled)
joblib.dump(iso, "model/isolation.pkl")

# -------------------------------
# Autoencoder
# -------------------------------
input_dim = X_scaled.shape[1]

input_layer = Input(shape=(input_dim,))
encoder = Dense(16, activation="relu")(input_layer)
encoder = Dense(8, activation="relu")(encoder)
decoder = Dense(16, activation="relu")(encoder)
decoder = Dense(input_dim, activation="linear")(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)
autoencoder.compile(optimizer="adam", loss="mse")

autoencoder.fit(
    X_scaled,
    X_scaled,
    epochs=5,
    batch_size=256,
    shuffle=True
)

# Save in new format (FIX 🔥)
autoencoder.save("model/autoencoder.keras")

print("🔥 Model training complete")