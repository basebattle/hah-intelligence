import streamlit as st
import plotly.graph_objects as go
from data.simulator import get_base_patients, CONDITION_ICONS
from engine.news2 import calculate_news2
from engine.rag_classifier import classify_patient_risk

st.set_page_config(page_title="Patient Detail | HaH Intelligence", page_icon="🩻",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg:#080F16; --surface:#0F1923; --surface2:#162029;
    --teal:#00BFA5; --teal-dim:rgba(0,191,165,0.12); --teal-border:rgba(0,191,165,0.30);
    --teal-glow:0 0 24px rgba(0,191,165,0.20);
    --red:#f87171; --amber:#fbbf24; --green:#4ade80;
    --text:#FFFFFF; --muted:rgba(255,255,255,0.52); --border:rgba(255,255,255,0.07);
}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
    background-color:var(--bg) !important; font-family:'DM Sans',sans-serif; color:var(--text);
}
[data-testid="stSidebar"] { background-color:#060C12 !important; border-right:1px solid var(--border); }

.page-header { font-family:'DM Serif Display',serif; font-size:1.9rem; color:var(--text); margin-bottom:0.2rem; }
.page-sub    { font-size:0.88rem; color:var(--muted); margin-bottom:1rem; }

.condition-banner {
    display:flex; align-items:center; gap:1.25rem;
    background:var(--surface); border:1px solid var(--teal-border);
    border-radius:16px; padding:1.4rem 1.75rem; margin:1rem 0 1.5rem;
}
.condition-banner-icon { font-size:3rem; line-height:1; }
.condition-banner-name { font-family:'DM Serif Display',serif; font-size:1.4rem; color:var(--text); }
.condition-banner-meta { font-size:0.82rem; color:var(--muted); margin-top:0.2rem; }

.vital-grid { display:flex; gap:0.75rem; flex-wrap:wrap; margin:0.75rem 0 1.25rem; }
.vital-card { flex:1; min-width:110px; background:var(--surface2); border:1px solid var(--border);
              border-radius:12px; padding:1rem 0.75rem; text-align:center; }
.vital-val   { font-family:'DM Serif Display',serif; font-size:1.6rem; color:var(--teal); line-height:1; }
.vital-label { font-size:0.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; margin-top:0.3rem; }

.ai-panel { background:var(--surface); border:1px solid var(--teal-border); border-radius:16px; padding:1.5rem; }
.ai-title { font-family:'DM Serif Display',serif; font-size:1.15rem; color:var(--text); margin-bottom:1rem; }
.ai-row   { display:flex; justify-content:space-between; align-items:center;
            padding:0.6rem 0; border-bottom:1px solid var(--border); font-size:0.85rem; }
.ai-row:last-of-type { border-bottom:none; }
.ai-key   { color:var(--muted); }
.ai-val   { font-weight:600; font-family:'JetBrains Mono',monospace; font-size:0.82rem; }

.news2-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:0.6rem; margin:0.75rem 0; }
.news2-item { background:var(--surface2); border:1px solid var(--border); border-radius:10px; padding:0.75rem; text-align:center; }
.news2-score  { font-family:'JetBrains Mono',monospace; font-size:1.4rem; color:var(--teal); line-height:1; }
.news2-param  { font-size:0.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.06em; margin-top:0.25rem; }

.notes-card { background:var(--surface2); border:1px solid var(--border); border-left:3px solid var(--teal);
              border-radius:12px; padding:1.25rem; font-size:0.84rem; color:var(--muted); line-height:1.65; }

@keyframes heartbeat  { 0%,100%{transform:scale(1)} 14%{transform:scale(1.22)} 28%{transform:scale(1)} 42%{transform:scale(1.14)} 56%{transform:scale(1)} }
@keyframes breathe    { 0%,100%{transform:scale(1)} 50%{transform:scaleX(1.10) scaleY(1.14)} }
@keyframes kidney-rock{ 0%,100%{transform:rotate(-6deg) scale(1)} 50%{transform:rotate(6deg) scale(1.09)} }
@keyframes glow-pulse { 0%,100%{opacity:.65;transform:scale(1)} 50%{opacity:1;transform:scale(1.12)} }
@keyframes drop-bounce{ 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
</style>
""", unsafe_allow_html=True)

ICON_ANIM = {
    "🫀": "heartbeat 1.3s ease-in-out infinite",
    "🫁": "breathe 2.2s ease-in-out infinite",
    "🫘": "kidney-rock 2.4s ease-in-out infinite",
    "🦠": "glow-pulse 1.8s ease-in-out infinite",
    "💧": "drop-bounce 1.6s ease-in-out infinite",
    "🌡️": "glow-pulse 2.0s ease-in-out infinite",
    "🏥": "glow-pulse 2.0s ease-in-out infinite",
}

COLOR_MAP = {
    "Red": "#f87171", "Amber": "#fbbf24", "Yellow": "#fbbf24",
    "Green": "#4ade80", "High": "#f87171", "Medium": "#fbbf24",
    "Low-Medium": "#a3e635", "Low": "#4ade80",
}

st.markdown("""
<div class="page-header">🩻 Patient Detail &amp; Intelligence</div>
<p class="page-sub">Select a patient to view full vitals, NEWS2 breakdown, and AI risk synthesis.</p>
""", unsafe_allow_html=True)

if "patients" not in st.session_state:
    st.session_state.patients = get_base_patients()

patients = st.session_state.patients
options  = {f"{p['id']} — {p['name']}  ({p['diagnosis']})": p for p in patients}
selected = st.selectbox("Select Patient", list(options.keys()), label_visibility="collapsed")
p        = options[selected]

icon      = CONDITION_ICONS.get(p["diagnosis"], "🏥")
anim      = ICON_ANIM.get(icon, "glow-pulse 2s ease-in-out infinite")
news2_res = calculate_news2(p["vitals"])
rag_res   = classify_patient_risk(p["clinical_notes"], news2_res)

risk_color = COLOR_MAP.get(news2_res["color"], "#fff")
rag_color  = COLOR_MAP.get(rag_res.get("final_color", "Green"), "#4ade80")

# ── Condition banner ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="condition-banner">
    <div class="condition-banner-icon">
        <span style="animation:{anim}; display:inline-block;">{icon}</span>
    </div>
    <div>
        <div class="condition-banner-name">{p['diagnosis']}</div>
        <div class="condition-banner-meta">
            {p['name']} &nbsp;·&nbsp; Age {p['age']}
            &nbsp;·&nbsp; Programme Day {p['days_in_program']}
            &nbsp;·&nbsp; Telemetry {p['telemetry_compliance']}% compliant
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown("#### Current Vitals")
    v = p["vitals"]
    st.markdown(f"""
<div class="vital-grid">
    <div class="vital-card">
        <div class="vital-val">{v['heart_rate']}</div>
        <div class="vital-label">Heart Rate<br>bpm</div>
    </div>
    <div class="vital-card">
        <div class="vital-val">{v['spo2']}</div>
        <div class="vital-label">SpO₂<br>%</div>
    </div>
    <div class="vital-card">
        <div class="vital-val">{v['respiration_rate']}</div>
        <div class="vital-label">Resp Rate<br>/min</div>
    </div>
    <div class="vital-card">
        <div class="vital-val">{v['systolic_bp']}</div>
        <div class="vital-label">Systolic BP<br>mmHg</div>
    </div>
    <div class="vital-card">
        <div class="vital-val">{v['temperature']}</div>
        <div class="vital-label">Temp<br>°C</div>
    </div>
    <div class="vital-card">
        <div class="vital-val" style="font-size:0.9rem; padding-top:0.3rem;">
            {"On O₂" if v['oxygen_supplement'] else "Room Air"}
        </div>
        <div class="vital-label">O₂ Supply</div>
    </div>
    <div class="vital-card">
        <div class="vital-val" style="font-size:0.9rem; padding-top:0.3rem;">{v['consciousness']}</div>
        <div class="vital-label">Consciousness<br>ACVPU</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("#### NEWS2 Parameter Breakdown")
    bd   = news2_res["breakdown"]
    html = '<div class="news2-grid">'
    for param, val in bd.items():
        col = "#f87171" if val == 3 else "#fbbf24" if val in (1, 2) else "#4ade80"
        html += f"""<div class="news2-item">
            <div class="news2-score" style="color:{col}">{val}</div>
            <div class="news2-param">{param}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    st.markdown("#### Latest Clinical Notes")
    st.markdown(f'<div class="notes-card">{p["clinical_notes"]}</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
<div class="ai-panel">
    <div class="ai-title">🤖 AI Analysis Engine</div>

    <div class="ai-row">
        <span class="ai-key">NEWS2 Score</span>
        <span class="ai-val" style="color:{risk_color}; font-size:1.1rem;">{news2_res['score']}</span>
    </div>
    <div class="ai-row">
        <span class="ai-key">Algorithmic Risk</span>
        <span class="ai-val" style="color:{risk_color};">{news2_res['risk_level']}</span>
    </div>
    <div class="ai-row">
        <span class="ai-key">Recommended Action</span>
        <span class="ai-val" style="color:var(--muted); font-family:'DM Sans',sans-serif;
              font-size:0.77rem; text-align:right; max-width:55%;">{news2_res['action']}</span>
    </div>

    <div style="border-top:1px solid var(--border); margin:0.75rem 0; padding-top:0.75rem;">
        <div style="font-size:0.7rem; color:var(--teal); font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em; margin-bottom:0.5rem;">LLM RAG SYNTHESIS</div>
        <div class="ai-row">
            <span class="ai-key">Synthesised Risk</span>
            <span class="ai-val" style="color:{rag_color};">{rag_res.get('final_risk','—')}</span>
        </div>
        <div class="ai-row">
            <span class="ai-key">Confidence</span>
            <span class="ai-val" style="color:var(--teal);">{int(rag_res.get('confidence',0)*100)}%</span>
        </div>
    </div>

    <div style="font-size:0.77rem; color:var(--muted); line-height:1.55; margin-top:0.5rem;
                background:rgba(255,255,255,0.03); border-radius:8px; padding:0.75rem;">
        <strong style="color:var(--text);">Reasoning:</strong><br>
        {rag_res.get('rag_reasoning','—')}
    </div>
</div>
""", unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rag_res.get("confidence", 0) * 100,
        title={"text": "AI Confidence %", "font": {"color": "white", "size": 13}},
        number={"suffix": "%", "font": {"color": "#00BFA5", "size": 28}},
        gauge={
            "axis":        {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.3)"},
            "bar":         {"color": "#00BFA5", "thickness": 0.25},
            "bgcolor":     "#0F1923",
            "bordercolor": "rgba(255,255,255,0.08)",
            "steps": [
                {"range": [0,  40], "color": "rgba(248,113,113,0.12)"},
                {"range": [40, 70], "color": "rgba(251,191,36,0.12)"},
                {"range": [70,100], "color": "rgba(74,222,128,0.12)"},
            ],
        },
    ))
    fig.update_layout(
        height=215, margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font={"color": "white"},
    )
    st.plotly_chart(fig, use_container_width=True)
