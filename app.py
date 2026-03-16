import streamlit as st

st.set_page_config(
    page_title="HaH Intelligence | Clinical Desk",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System CSS
st.markdown("""
<style>
    :root {
        --primary: #0D7377;
        --accent: #00BFA5;
        --background: #0F1923;
        --card-bg: rgba(22, 32, 41, 0.7);
        --text: #FFFFFF;
    }
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }
    .stMetric, .css-1r6slb0, .css-12oz5g7 {
        background-color: var(--card-bg);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    [data-testid="stSidebar"] {
        background-color: #121c24;
    }
    .status-Red { color: #f87171; font-weight: bold; }
    .status-Amber { color: #fbbf24; font-weight: bold; }
    .status-Green { color: #4ade80; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🏥 Hospital-at-Home Intelligence Layer")
st.markdown("### Clinical Command Center")
st.markdown("""
Welcome to the continuous monitoring and clinical intelligence layer for the Hospital-at-Home program.

Select a module from the sidebar:
- **Census Monitor:** View the 20-patient cohort and their real-time NEWS2 scores.
- **Patient Detail:** Deep dive into a specific patient's vitals and RAG analysis.
- **Active Alerts:** Review engine-generated clinical escalations.
- **CMS Compliance:** Track Acute Hospital Care at Home waiver requirements.

This system leverages **NEWS2 logic** and simulated **LLM RAG analysis** to detect patient deterioration before acute events occur in the home setting.
""")
