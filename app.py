import streamlit as st
import numpy as np
import joblib
import random
import matplotlib.pyplot as plt

from utils.auth import auth
from utils.predict import predict
from utils.explain import explain_model

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Fraud AI System", layout="wide")

# -------------------------------
# LOGIN
# -------------------------------
if not auth():
    st.stop()

# -------------------------------
# LOAD MODELS (ONLY SKLEARN ✅)
# -------------------------------
scaler = joblib.load("model/scaler.pkl")
iso = joblib.load("model/isolation.pkl")

# -------------------------------
# UI STYLE 🔥
# -------------------------------
st.markdown("""
<style>
h1, h2, h3 {color: #00ADB5;}
.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("💳 AI Fraud Detection System")
st.caption("⚡ Intelligent + Explainable Fraud Detection Engine")

# -------------------------------
# RANDOM DATA 🎲
# -------------------------------
if st.button("🎲 Auto Generate Test Data"):
    st.session_state["rand"] = [random.uniform(-2,2) for _ in range(5)] + \
                               [random.uniform(10,1000), random.uniform(0,50000)]

# -------------------------------
# INPUTS
# -------------------------------
vals = st.session_state.get("rand", [0]*7)

col1, col2 = st.columns(2)

with col1:
    v1 = st.number_input("V1", value=float(vals[0]))
    v2 = st.number_input("V2", value=float(vals[1]))
    v3 = st.number_input("V3", value=float(vals[2]))

with col2:
    v4 = st.number_input("V4", value=float(vals[3]))
    v5 = st.number_input("V5", value=float(vals[4]))

amount = st.number_input("Amount", value=float(vals[5]))
time = st.number_input("Time", value=float(vals[6]))

inputs = [v1,v2,v3,v4,v5] + [0]*23 + [amount,time]

# -------------------------------
# ANALYZE 🔥
# -------------------------------
if st.button("🚀 Analyze"):

    data = np.array(inputs).reshape(1, -1)

    # ❌ No autoencoder
    iso_pred, fraud_score = predict(data, scaler, iso, None)

    deviation = np.std(data)

    st.subheader(f"📊 Fraud Score: {fraud_score:.6f}")
    st.write(f"📈 Behavior Deviation: {deviation:.4f}")

    st.progress(min(int(fraud_score * 100), 100))

    if iso_pred[0] == -1 or fraud_score > 0.1 or deviation > 2:
        st.error("🚨 HIGH RISK FRAUD")
    elif fraud_score > 0.05:
        st.warning("⚠️ MEDIUM RISK")
    else:
        st.success("✅ SAFE TRANSACTION")

    # -------------------------------
    # GRAPH 📊
    # -------------------------------
    fig, ax = plt.subplots()
    ax.bar(["Fraud Score"], [fraud_score])
    ax.set_title("Fraud Score Visualization")
    st.pyplot(fig)

    # -------------------------------
    # AI REASONING
    # -------------------------------
    st.subheader("🧠 AI Reasoning")

    if deviation > 2:
        st.write("High deviation detected from normal behavior.")
    elif fraud_score > 0.05:
        st.write("Model found anomaly in transaction pattern.")
    else:
        st.write("Transaction looks normal.")

    # -------------------------------
    # SHAP (SAFE MODE)
    # -------------------------------
    st.subheader("🔍 Explainable AI")

    try:
        shap_values = explain_model(None, data)

        if shap_values is not None:
            import shap
            shap.summary_plot(shap_values, data, show=False)
            st.pyplot(plt.gcf())
        else:
            st.warning("SHAP not available.")
    except:
        st.warning("SHAP disabled.")

    # -------------------------------
    # HISTORY
    # -------------------------------
    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.session_state["history"].append({
        "score": fraud_score,
        "deviation": deviation
    })

    history = st.session_state.get("history", [])

    if len(history) > 1:
        scores = [h["score"] for h in history]

        fig2, ax2 = plt.subplots()
        ax2.plot(scores, marker='o')
        ax2.set_title("📈 Fraud Score Trend")
        ax2.set_xlabel("Transaction")
        ax2.set_ylabel("Score")

        st.pyplot(fig2)

    # -------------------------------
    # CONFIDENCE
    # -------------------------------
    confidence = min(fraud_score * 100, 100)
    st.write(f"🧠 Confidence Score: {confidence:.2f}%")

    # -------------------------------
    # FRAUD TYPE
    # -------------------------------
    st.subheader("🎯 Fraud Type Analysis")

    if amount > 5000:
        st.write("💡 Type: High Amount Fraud")
    elif deviation > 2:
        st.write("💡 Type: Behavioral Fraud")
    elif fraud_score > 0.05:
        st.write("💡 Type: Pattern Anomaly")
    else:
        st.write("💡 Type: Normal Transaction")

    # -------------------------------
    # ALERT
    # -------------------------------
    if fraud_score > 0.1:
        st.warning("🔔 ALERT: Suspicious Transaction Detected!")

    # -------------------------------
    # DOWNLOAD REPORT
    # -------------------------------
    report = f"""
Fraud Detection Report
----------------------
Fraud Score: {fraud_score:.6f}
Deviation: {deviation:.4f}
Confidence: {confidence:.2f}%

Result:
{"FRAUD" if fraud_score > 0.1 else "SAFE"}
"""

    st.download_button(
        label="📄 Download Report",
        data=report,
        file_name="fraud_report.txt",
        mime="text/plain"
    )