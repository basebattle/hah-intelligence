import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.title("📋 CMS Waiver Compliance")

st.markdown("""
The **Acute Hospital Care at Home** program requires strict adherence to CMS waiver protocols. 
This dashboard tracks automated compliance checks for the active census.
""")

st.markdown("---")

@st.cache_data
def load_waiver_data():
    file_path = Path(__file__).parent.parent / "data" / "cms_waiver_checklist.json"
    with open(file_path, "r") as f:
        return json.load(f)

waivers = load_waiver_data()

metrics = {"met": 0, "at_risk": 0, "failed": 0}
for w in waivers:
    if w['status'] == 'met': metrics['met'] += 1
    elif w['status'] == 'at_risk': metrics['at_risk'] += 1
    else: metrics['failed'] += 1

cols = st.columns(3)
cols[0].metric("✅ Compliant Protocols", metrics['met'])
cols[1].metric("⚠️ At Risk", metrics['at_risk'])
cols[2].metric("❌ Failed (Immediate Action)", metrics['failed'])

st.markdown("### Protocol Status")

for w in waivers:
    with st.expander(f"{w['id']}: {w['category']} ({w['weight']}) - Status: {w['status'].upper()}"):
        st.write(f"**Requirement:** {w['requirement']}")
        st.write(f"**Audit Notes:** {w['notes']}")
        if w['status'] != 'met':
            st.error("Remediation required to maintain CMS waiver standing.")
