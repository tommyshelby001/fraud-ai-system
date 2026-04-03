import numpy as np

def predict(data, scaler, iso, autoencoder=None):
    data_scaled = scaler.transform(data)

    # Isolation Forest prediction
    iso_pred = iso.predict(data_scaled)

    # Simple fraud score (NO tensorflow)
    fraud_score = np.mean(np.abs(data_scaled))

    return iso_pred, float(fraud_score)