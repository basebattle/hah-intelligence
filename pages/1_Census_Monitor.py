import streamlit as st
import pandas as pd
from data.simulator import get_base_patients, run_simulation
from engine.news2 import calculate_news2

st.title("👥 Active Census Monitor")

# Initialize session state for patients
if 'patients' not in st.session_state:
    st.session_state.patients = get_base_patients()

# Add refresh button to trigger simulation
if st.button("🔄 Refresh Vitals Telemetry"):
    st.session_state.patients = run_simulation(st.session_state.patients)

st.markdown("---")

# Build display dataframe
display_data = []

metrics = {"Red (High Risk)": 0, "Amber (Medium Risk)": 0, "Green (Stable)": 0}

for p in st.session_state.patients:
    score_data = calculate_news2(p['vitals'])
    color = score_data['color']
    
    if color == 'Red': metrics['Red (High Risk)'] += 1
    elif color == 'Amber': metrics['Amber (Medium Risk)'] += 1
    else: metrics['Green (Stable)'] += 1
    
    display_data.append({
        "Patient ID": p['id'],
        "Name": p['name'],
        "Diagnosis": p['diagnosis'],
        "Day": p['days_in_program'],
        "SpO2": p['vitals']['spo2'],
        "Heart Rate": p['vitals']['heart_rate'],
        "NEWS2 Score": score_data['score'],
        "Risk Level": score_data['risk_level']
    })

df = pd.DataFrame(display_data)

# Style function based on risk level
def style_risk(val):
    if val == 'High': return 'color: #f87171; font-weight: bold; background-color: rgba(248,113,113,0.1)'
    if val == 'Medium': return 'color: #fbbf24; font-weight: bold; background-color: rgba(251,191,36,0.1)'
    return 'color: #4ade80'

# Top metrics
cols = st.columns(3)
cols[0].metric("🔴 High Risk (Escalate)", metrics['Red (High Risk)'])
cols[1].metric("🟡 Medium Risk (Review)", metrics['Amber (Medium Risk)'])
cols[2].metric("🟢 Stable (Routine)", metrics['Green (Stable)'])

st.markdown("### Telemetry Data")
st.dataframe(
    df.style.map(style_risk, subset=['Risk Level']),
    use_container_width=True,
    hide_index=True
)
