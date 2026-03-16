import streamlit as st
import pandas as pd
from data.simulator import get_base_patients
from engine.alert_generator import generate_alerts

st.title("🚨 Active Alerts & Escalations")

if 'patients' not in st.session_state:
    st.session_state.patients = get_base_patients()

st.markdown("---")

all_alerts = []
for p in st.session_state.patients:
    alerts = generate_alerts(p)
    all_alerts.extend(alerts)

if not all_alerts:
    st.success("✅ No active alerts at this time.")
else:
    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_alerts.sort(key=lambda x: severity_order.get(x['severity'], 99))
    
    st.markdown(f"### {len(all_alerts)} Active Alerts")
    
    for alert in all_alerts:
        if alert['severity'] == "CRITICAL":
            st.error(f"**[{alert['type']}] {alert['patient_name']} ({alert['patient_id']})**\n\n{alert['message']}")
        elif alert['severity'] == "HIGH":
            st.warning(f"**[{alert['type']}] {alert['patient_name']} ({alert['patient_id']})**\n\n{alert['message']}")
        else:
            st.info(f"**[{alert['type']}] {alert['patient_name']} ({alert['patient_id']})**\n\n{alert['message']}")

st.markdown("---")
st.caption("Alerts are auto-generated based on the RAG classification engine and NEWS2 clinical scoring.")
