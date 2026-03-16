import streamlit as st
import plotly.graph_objects as go
from data.simulator import get_base_patients
from engine.news2 import calculate_news2
from engine.rag_classifier import classify_patient_risk

st.title("🩻 Patient Detail & Intelligence")

if 'patients' not in st.session_state:
    st.session_state.patients = get_base_patients()

patients = st.session_state.patients
patient_options = {f"{p['id']} - {p['name']} ({p['status']})": p for p in patients}

selected_key = st.selectbox("Select Patient to Review", list(patient_options.keys()))
p = patient_options[selected_key]

st.markdown("---")

cols = st.columns([2, 1])

with cols[0]:
    st.subheader("Patient Profile")
    st.markdown(f"**ID:** {p['id']} | **Name:** {p['name']} | **Age:** {p['age']}")
    st.markdown(f"**Primary Diagnosis:** {p['diagnosis']}")
    st.markdown(f"**Program Day:** {p['days_in_program']} | **Telemetry Compliance:** {p['telemetry_compliance']}%")
    
    st.markdown("### Current Vitals")
    v_cols = st.columns(4)
    v_cols[0].metric("Heart Rate", f"{p['vitals']['heart_rate']} bpm")
    v_cols[1].metric("SpO2", f"{p['vitals']['spo2']}%")
    v_cols[2].metric("Resp Rate", f"{p['vitals']['respiration_rate']} /min")
    v_cols[3].metric("Systolic BP", f"{p['vitals']['systolic_bp']} mmHg")
    
    st.markdown("### Clinical Notes (Latest)")
    st.info(p['clinical_notes'])

with cols[1]:
    st.subheader("AI Analysis Engine")
    
    # Run scoring
    news2_result = calculate_news2(p['vitals'])
    rag_result = classify_patient_risk(p['clinical_notes'], news2_result)
    
    color_map = {"Red": "#f87171", "Amber": "#fbbf24", "Green": "#4ade80", "Yellow": "#fbbf24"}
    
    st.markdown(f"**NEWS2 Score:** {news2_result['score']}")
    st.markdown(f"**Algorithmic Risk:** <span style='color:{color_map.get(news2_result['color'], '#fff')}'>{news2_result['risk_level']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Recommended Action:** {news2_result['action']}")
    
    st.markdown("---")
    st.markdown("**LLM Synthesis (Notes + Vitals):**")
    st.markdown(f"**Synthesized Risk:** <span style='color:{color_map.get(rag_result['final_color'], '#fff')}'>{rag_result['final_risk']}</span>", unsafe_allow_html=True)
    st.caption(f"**Reasoning:** {rag_result['rag_reasoning']}")
    
    # RAG Gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = rag_result['confidence'] * 100,
        title = {'text': "AI Confidence %"},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "#0D7377"}}
    ))
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)
