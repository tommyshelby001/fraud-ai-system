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

# 🔥 DARK THEME
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
[data-testid="stSidebar"] {
    background: #020617;
}
h1, h2, h3 {color: #38bdf8;}
.stButton>button {
    background: linear-gradient(90deg,#06b6d4,#3b82f6);
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOGIN
# -------------------------------
if not auth():
    st.stop()

# -------------------------------
# SIDEBAR (EXTRA)
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ System Status")
st.sidebar.success("🟢 Model Active")
st.sidebar.markdown("### 🤖 Version")
st.sidebar.info("Fraud AI v1.0")

# 🌐 LIVE LINK (NEW)
st.sidebar.markdown("🌐 Live App: https://your-link.streamlit.app")

# -------------------------------
# LOAD MODELS
# -------------------------------
scaler = joblib.load("model/scaler.pkl")
iso = joblib.load("model/isolation.pkl")

# -------------------------------
# ORIGINAL UI STYLE
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

# HERO
st.markdown("""
<div style='padding:15px;border-radius:12px;
background:linear-gradient(90deg,#0ea5e9,#1e3a8a);
text-align:center;color:white'>
<h3>🚀 AI Fraud Detection Dashboard</h3>
<p>Real-time • Smart • Secure</p>
</div>
""", unsafe_allow_html=True)

st.caption("⚡ Intelligent + Explainable Fraud Detection Engine")

# -------------------------------
# RANDOM DATA
# -------------------------------
if st.button("🎲 Auto Generate Test Data"):
    st.session_state["rand"] = [random.uniform(-2,2) for _ in range(5)] + \
                               [random.uniform(10,1000), random.uniform(0,50000)]

# -------------------------------
# INPUTS
# -------------------------------
st.markdown("### 📥 Enter Transaction Details")

vals = st.session_state.get("rand", [0]*7)

col1, col2 = st.columns(2, gap="large")

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
# ANALYZE
# -------------------------------
if st.button("🚀 Analyze"):

    data = np.array(inputs).reshape(1, -1)

    iso_pred, fraud_score = predict(data, scaler, iso, None)

    deviation = np.std(data)

    st.subheader(f"📊 Fraud Score: {fraud_score:.6f}")
    st.write(f"📈 Behavior Deviation: {deviation:.4f}")

    # PREMIUM CARD
    st.markdown(f"""
    <div style='padding:15px;border-radius:10px;
    background:#0f172a;border:1px solid #38bdf8'>
    <h4>📊 Fraud Score: {fraud_score:.6f}</h4>
    <p>📈 Deviation: {deviation:.4f}</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(int(fraud_score * 100), 100))

    if iso_pred[0] == -1 or fraud_score > 0.1 or deviation > 2:
        st.error("🚨 HIGH RISK FRAUD")
    elif fraud_score > 0.05:
        st.warning("⚠️ MEDIUM RISK")
    else:
        st.success("✅ SAFE TRANSACTION")

    # GRAPH
    fig, ax = plt.subplots()
    ax.bar(["Fraud Score"], [fraud_score])
    ax.set_title("Fraud Score Visualization")
    st.pyplot(fig)

    # AI REASONING
    st.subheader("🧠 AI Reasoning")

    if deviation > 2:
        st.write("High deviation detected from normal behavior.")
    elif fraud_score > 0.05:
        st.write("Model found anomaly in transaction pattern.")
    else:
        st.write("Transaction looks normal.")

    # SHAP
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

    # HISTORY
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
        st.pyplot(fig2)

    # LIVE GRAPH
    if "simple_history" not in st.session_state:
        st.session_state["simple_history"] = []

    st.session_state["simple_history"].append(fraud_score)

    if len(st.session_state["simple_history"]) > 1:
        st.subheader("📊 Live Fraud Score Graph")
        st.line_chart(st.session_state["simple_history"])

    # CONFIDENCE
    confidence = min(fraud_score * 100, 100)
    st.write(f"🧠 Confidence Score: {confidence:.2f}%")

    # FRAUD TYPE
    st.subheader("🎯 Fraud Type Analysis")

    if amount > 5000:
        st.write("💡 Type: High Amount Fraud")
    elif deviation > 2:
        st.write("💡 Type: Behavioral Fraud")
    elif fraud_score > 0.05:
        st.write("💡 Type: Pattern Anomaly")
    else:
        st.write("💡 Type: Normal Transaction")

    # ALERT
    if fraud_score > 0.1:
        st.warning("🔔 ALERT: Suspicious Transaction Detected!")

    # REPORT
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