import streamlit as st
import random

st.set_page_config(page_title="Ops AI Dashboard", layout="wide")

st.title("Ops AI Monitoring Dashboard")

# ---- Chat Interface ----
st.subheader("AI Ops Chat")

query = st.text_input("Ask: Why is payment service unstable?")

if st.button("Send"):
    st.write("Failure Risk: 0.82")
    st.write("Recommended Action: Scale DB Replicas")

st.divider()

# ---- Metrics Section ----
st.subheader("System Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("DB Latency", "91 ms")

with col2:
    st.metric("CPU Usage", "72 %")

with col3:
    st.metric("Error Rate", "4 %")

st.divider()

# ---- Failures ----
st.subheader("Detected Failures")

st.write("• Payment Retry Storm")
st.write("• Error Spike Detected")

st.divider()

# ---- Recommendations ----
st.subheader("Recommended Actions")

st.write("• Scale DB Replicas")
st.write("• Restart Payment Service")