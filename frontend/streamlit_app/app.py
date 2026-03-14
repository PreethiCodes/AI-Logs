import streamlit as st
import pandas as pd
import random
import plotly.express as px

st.set_page_config(page_title="Ops AI Dashboard", layout="wide")

st.title("⚙️ Ops AI Monitoring Dashboard")

st.markdown("---")

# -----------------------------
# AI Failure Risk Indicator
# -----------------------------

st.subheader("AI Failure Prediction")

risk = round(random.uniform(0.6, 0.9), 2)

col1, col2 = st.columns(2)

with col1:
    st.metric("Failure Probability", risk)

with col2:
    if risk > 0.8:
        st.error("HIGH RISK ⚠️")
    elif risk > 0.6:
        st.warning("MEDIUM RISK")
    else:
        st.success("LOW RISK")

st.markdown("---")

# -----------------------------
# System Metrics
# -----------------------------

st.subheader("System Metrics")

c1, c2, c3 = st.columns(3)

c1.metric("DB Latency", f"{random.randint(80,120)} ms", "+5 ms")
c2.metric("CPU Usage", f"{random.randint(60,90)} %", "+2 %")
c3.metric("Error Rate", f"{random.randint(1,5)} %", "-1 %")

st.markdown("---")

# -----------------------------
# Latency Chart
# -----------------------------

st.subheader("Latency Trend")

data = pd.DataFrame({
    "time": range(20),
    "latency": [random.randint(70,120) for _ in range(20)]
})

fig = px.line(data, x="time", y="latency", title="DB Latency Over Time")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# Detected Failures
# -----------------------------

st.subheader("Detected Failures")

st.error("Payment Retry Storm")
st.warning("Latency Spike Detected")

st.markdown("---")

# -----------------------------
# Recommendations
# -----------------------------

st.subheader("Recommended Actions")

st.success("Scale DB Replicas")
st.success("Restart Payment Service")

st.markdown("---")

# -----------------------------
# AI Ops Chat
# -----------------------------

st.subheader("AI Ops Chat")

query = st.text_input("Ask something about system health")

if st.button("Analyze"):
    st.write("Root Cause: Payment DB overload")
    st.write("Suggested Fix: Increase DB replicas")