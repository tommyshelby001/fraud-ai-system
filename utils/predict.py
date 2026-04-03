import numpy as np

def predict(data, scaler, iso, autoencoder):
    data_scaled = scaler.transform(data)

    iso_pred = iso.predict(data_scaled)

    recon = autoencoder.predict(data_scaled)
    loss = np.mean((data_scaled - recon) ** 2)

    return iso_pred, float(loss)