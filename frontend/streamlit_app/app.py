import os
import random

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


st.set_page_config(page_title="Ops AI Dashboard", layout="wide")

st.title("⚙️ Ops AI Monitoring Dashboard")

st.caption(
    "Backed by FastAPI, Groq-powered AI, and simulated logs/metrics from the backend."
)

st.markdown("---")


@st.cache_data(ttl=10.0)
def fetch_status_overview():
    try:
        resp = requests.get(f"{BACKEND_URL}/status/overview", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        st.error(f"Failed to fetch status overview: {exc}")
        return None


@st.cache_data(ttl=10.0)
def fetch_service_status(service_name: str):
    try:
        resp = requests.get(
            f"{BACKEND_URL}/status/service/{service_name}", timeout=5
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        st.error(f"Failed to fetch status for {service_name}: {exc}")
        return None


def call_chat_api(query: str):
    try:
        resp = requests.post(
            f"{BACKEND_URL}/chat",
            json={"query": query},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        st.error(f"Chat request failed: {exc}")
        return None


# -----------------------------
# AI Failure Risk Indicator
# -----------------------------

st.subheader("AI Failure Prediction")

overview = fetch_status_overview()
total_failures = overview["failures"]["total"] if overview else 0

if total_failures > 5:
    risk = 0.9
elif total_failures > 0:
    risk = 0.7
else:
    risk = 0.2

risk = round(risk + random.uniform(-0.05, 0.05), 2)

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

st.subheader("System Metrics (last 15 min)")

services = overview["services"] if overview else {}

if not services:
    st.info("No metrics available yet. Waiting for simulator to generate data.")
else:
    c1, c2, c3 = st.columns(3)

    avg_cpu = sum(s["avg_cpu"] for s in services.values()) / len(services)
    avg_mem = sum(s["avg_memory"] for s in services.values()) / len(services)
    avg_lat = sum(s["avg_latency"] for s in services.values()) / len(services)

    c1.metric("Cluster CPU", f"{avg_cpu:.1f} %")
    c2.metric("Cluster Memory", f"{avg_mem:.1f} %")
    c3.metric("Avg Latency", f"{avg_lat:.1f} ms")

st.markdown("---")

# -----------------------------
# Latency Chart
# -----------------------------

st.subheader("Latency Trend by Service")

if services:
    rows = []
    for svc_name, stats in services.items():
        count = max(int(stats["count"]), 1)
        base = stats["avg_latency"]
        for i in range(count):
            jitter = random.uniform(-0.15, 0.15) * base
            rows.append(
                {
                    "service": svc_name,
                    "time": i,
                    "latency": max(0, base + jitter),
                }
            )

    df = pd.DataFrame(rows)
    fig = px.line(
        df,
        x="time",
        y="latency",
        color="service",
        labels={"time": "Sample", "latency": "Latency (ms)"},
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Latency trend will appear once metrics are available.")

st.markdown("---")

# -----------------------------
# Detected Failures & Recommendations
# -----------------------------

st.subheader("Detected Failures & Recommendations")

failures_by_service = overview["failures"]["by_service"] if overview else {}

if not failures_by_service:
    st.success("No failures detected in the recent monitoring window.")
else:
    for service, failures in failures_by_service.items():
        with st.expander(f"{service}  -  {len(failures)} issues", expanded=True):
            for f in failures:
                st.markdown(
                    f"**Category:** `{f['category']}`  \n"
                    f"**Reason:** {f['reason']}  \n"
                    f"**Priority:** {f.get('priority', 'N/A')}"
                )
                recs = f.get("recommendations")
                if recs:
                    st.markdown("**Recommendations:**")
                    for rec in recs:
                        st.markdown(f"- {rec}")
                st.markdown("---")

st.markdown("---")

# -----------------------------
# AI Ops Chat
# -----------------------------

st.subheader("AI Ops Chat")

default_question = "Is anything broken right now? What should I investigate first?"
query = st.text_input("Ask something about system health", value=default_question)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col_send, col_clear = st.columns([3, 1])

with col_send:
    send_clicked = st.button("Ask AI", use_container_width=True)
with col_clear:
    clear_clicked = st.button("Clear History", use_container_width=True)

if clear_clicked:
    st.session_state.chat_history = []

if send_clicked and query.strip():
    st.session_state.chat_history.append(("user", query))
    result = call_chat_api(query)
    if result:
        answer = result.get("answer", "No answer returned from backend.")
        st.session_state.chat_history.append(("assistant", answer))

if st.session_state.chat_history:
    for role, text in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**AI:** {text}")