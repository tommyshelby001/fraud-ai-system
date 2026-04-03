import shap
import numpy as np

def explain_model(autoencoder, sample):
    try:
        background = np.zeros((1, sample.shape[1]))
        explainer = shap.KernelExplainer(autoencoder.predict, background)
        shap_values = explainer.shap_values(sample)
        return shap_values
    except:
        return None