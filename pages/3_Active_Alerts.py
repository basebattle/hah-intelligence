import streamlit as st
from data.simulator import get_base_patients, CONDITION_ICONS
from engine.alert_generator import generate_alerts

st.set_page_config(page_title="Active Alerts | HaH Intelligence", page_icon="🚨",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg:#080F16; --surface:#0F1923; --surface2:#162029;
    --teal:#00BFA5; --teal-dim:rgba(0,191,165,0.12); --teal-border:rgba(0,191,165,0.30);
    --red:#f87171; --amber:#fbbf24; --green:#4ade80; --blue:#60a5fa;
    --text:#FFFFFF; --muted:rgba(255,255,255,0.52); --border:rgba(255,255,255,0.07);
}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
    background-color:var(--bg) !important; font-family:'DM Sans',sans-serif; color:var(--text);
}
[data-testid="stSidebar"] { background-color:#060C12 !important; border-right:1px solid var(--border); }

.page-header { font-family:'DM Serif Display',serif; font-size:1.9rem; color:var(--text); margin-bottom:0.2rem; }
.page-sub    { font-size:0.88rem; color:var(--muted); margin-bottom:1.5rem; }

.alert-card {
    background:var(--surface); border-radius:14px;
    padding:1.25rem 1.5rem; margin-bottom:0.85rem;
    border-left:4px solid var(--border);
    transition: transform 0.2s ease;
}
.alert-card:hover { transform:translateX(3px); }
.alert-card.critical { border-left-color:var(--red);   background:rgba(248,113,113,0.06); }
.alert-card.high     { border-left-color:var(--amber);  background:rgba(251,191,36,0.06); }
.alert-card.medium   { border-left-color:var(--blue);   background:rgba(96,165,250,0.06); }
.alert-card.low      { border-left-color:var(--green);  background:rgba(74,222,128,0.04); }

.alert-header { display:flex; align-items:center; gap:0.75rem; margin-bottom:0.5rem; }
.alert-badge  {
    display:inline-block; border-radius:999px; padding:0.2rem 0.75rem;
    font-size:0.7rem; font-weight:700; font-family:'JetBrains Mono',monospace;
    letter-spacing:0.06em; text-transform:uppercase;
}
.badge-critical { background:rgba(248,113,113,0.18); color:var(--red);   border:1px solid rgba(248,113,113,0.3); }
.badge-high     { background:rgba(251,191,36,0.18);  color:var(--amber); border:1px solid rgba(251,191,36,0.3); }
.badge-medium   { background:rgba(96,165,250,0.18);  color:var(--blue);  border:1px solid rgba(96,165,250,0.3); }
.badge-low      { background:rgba(74,222,128,0.18);  color:var(--green); border:1px solid rgba(74,222,128,0.3); }

.alert-patient { font-weight:600; font-size:0.95rem; color:var(--text); }
.alert-type    { font-size:0.75rem; color:var(--muted); font-family:'JetBrains Mono',monospace; }
.alert-icon    { font-size:1.5rem; }
.alert-message { font-size:0.84rem; color:var(--muted); line-height:1.55; }

.summary-bar { display:flex; gap:1rem; flex-wrap:wrap; margin:1rem 0 1.75rem; }
.summary-pill {
    display:flex; align-items:center; gap:0.4rem;
    background:var(--surface); border:1px solid var(--border);
    border-radius:999px; padding:0.4rem 1rem;
    font-size:0.82rem; font-family:'JetBrains Mono',monospace;
}

.no-alerts {
    text-align:center; padding:3rem 1rem;
    background:var(--surface); border:1px solid var(--border);
    border-radius:16px; color:var(--muted);
}
.no-alerts-icon { font-size:2.5rem; margin-bottom:0.75rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">🚨 Active Alerts &amp; Escalations</div>
<p class="page-sub">
    Auto-generated clinical escalation queue &nbsp;·&nbsp;
    Ranked by severity &nbsp;·&nbsp; Powered by NEWS2 + RAG engine
</p>
""", unsafe_allow_html=True)

if "patients" not in st.session_state:
    st.session_state.patients = get_base_patients()

all_alerts = []
for p in st.session_state.patients:
    alerts = generate_alerts(p)
    for a in alerts:
        a["_diagnosis"] = p.get("diagnosis", "")
    all_alerts.extend(alerts)

severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
all_alerts.sort(key=lambda x: severity_order.get(x["severity"], 99))

# ── Summary bar ───────────────────────────────────────────────────────────────
counts = {s: 0 for s in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]}
for a in all_alerts:
    counts[a["severity"]] = counts.get(a["severity"], 0) + 1

st.markdown(f"""
<div class="summary-bar">
    <div class="summary-pill"><span style="color:var(--red)">●</span> {counts['CRITICAL']} Critical</div>
    <div class="summary-pill"><span style="color:var(--amber)">●</span> {counts['HIGH']} High</div>
    <div class="summary-pill"><span style="color:#60a5fa">●</span> {counts['MEDIUM']} Medium</div>
    <div class="summary-pill"><span style="color:var(--green)">●</span> {counts['LOW']} Low</div>
    <div class="summary-pill" style="margin-left:auto;">
        <span style="color:var(--muted)">Total</span>
        <span style="color:var(--text); font-weight:600">{len(all_alerts)}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not all_alerts:
    st.markdown("""
<div class="no-alerts">
    <div class="no-alerts-icon">✅</div>
    <div style="font-family:'DM Serif Display',serif; font-size:1.2rem; color:var(--text); margin-bottom:0.4rem;">
        All Clear
    </div>
    <div>No active alerts at this time. All patients within normal parameters.</div>
</div>
""", unsafe_allow_html=True)
else:
    for alert in all_alerts:
        sev   = alert["severity"].lower()
        badge = f"badge-{sev}"
        icon  = CONDITION_ICONS.get(alert.get("_diagnosis", ""), "🏥")

        st.markdown(f"""
<div class="alert-card {sev}">
    <div class="alert-header">
        <span class="alert-icon">{icon}</span>
        <span class="alert-badge {badge}">{alert['severity']}</span>
        <span class="alert-patient">{alert['patient_name']} ({alert['patient_id']})</span>
        <span class="alert-type" style="margin-left:auto;">{alert['type']}</span>
    </div>
    <div class="alert-message">{alert['message']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="font-size:0.73rem; color:rgba(255,255,255,0.25); margin-top:1rem;
          font-family:'JetBrains Mono',monospace;">
    Alerts auto-generated by the RAG classification engine and NEWS2 clinical scoring.
    Refresh vitals in Census Monitor to update.
</p>
""", unsafe_allow_html=True)
