import streamlit as st
import pandas as pd
from data.simulator import get_base_patients, run_simulation, CONDITION_ICONS
from engine.news2 import calculate_news2

st.set_page_config(page_title="Census Monitor | HaH Intelligence", page_icon="👥",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg:#080F16; --surface:#0F1923;
    --teal:#00BFA5; --teal-dim:rgba(0,191,165,0.12); --teal-border:rgba(0,191,165,0.30);
    --red:#f87171; --amber:#fbbf24; --green:#4ade80;
    --text:#FFFFFF; --muted:rgba(255,255,255,0.52); --border:rgba(255,255,255,0.07);
}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
    background-color:var(--bg) !important; font-family:'DM Sans',sans-serif; color:var(--text);
}
[data-testid="stSidebar"] { background-color:#060C12 !important; border-right:1px solid var(--border); }

.page-header { font-family:'DM Serif Display',serif; font-size:1.9rem; color:var(--text); margin-bottom:0.2rem; }
.page-sub    { font-size:0.88rem; color:var(--muted); margin-bottom:1.5rem; }

.risk-cards  { display:flex; gap:1rem; margin:1.25rem 0 1.5rem; flex-wrap:wrap; }
.risk-card   { flex:1; min-width:150px; background:var(--surface); border:1px solid var(--border);
               border-radius:14px; padding:1.25rem 1rem; text-align:center; }
.risk-card.red   { border-top:3px solid var(--red); }
.risk-card.amber { border-top:3px solid var(--amber); }
.risk-card.green { border-top:3px solid var(--green); }
.risk-num         { font-family:'DM Serif Display',serif; font-size:2.2rem; line-height:1; }
.risk-num.red    { color:var(--red); }
.risk-num.amber  { color:var(--amber); }
.risk-num.green  { color:var(--green); }
.risk-label      { font-size:0.72rem; color:var(--muted); text-transform:uppercase;
                   letter-spacing:0.08em; margin-top:0.4rem; }
.divider { border-top:1px solid var(--border); margin:1rem 0 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">👥 Active Census Monitor</div>
<p class="page-sub">
    Live 20-patient cohort &nbsp;·&nbsp; NEWS2 risk stratification &nbsp;·&nbsp;
    Real-time telemetry &nbsp;·&nbsp; <em>Refresh to simulate new vitals</em>
</p>""", unsafe_allow_html=True)

if "patients" not in st.session_state:
    st.session_state.patients = get_base_patients()

col_btn, _ = st.columns([1, 5])
with col_btn:
    if st.button("🔄 Refresh Vitals Telemetry"):
        st.session_state.patients = run_simulation(st.session_state.patients)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Build dataframe ───────────────────────────────────────────────────────────
display_data = []
metrics = {"Red": 0, "Amber": 0, "Green": 0}

for p in st.session_state.patients:
    sd = calculate_news2(p["vitals"])
    color = sd["color"]

    if color == "Red":                  metrics["Red"]   += 1
    elif color in ("Amber", "Yellow"):  metrics["Amber"] += 1
    else:                               metrics["Green"] += 1

    icon = CONDITION_ICONS.get(p["diagnosis"], "🏥")
    display_data.append({
        " ":           icon,
        "ID":          p["id"],
        "Name":        p["name"],
        "Age":         p["age"],
        "Diagnosis":   p["diagnosis"],
        "Day":         p["days_in_program"],
        "HR":          p["vitals"]["heart_rate"],
        "SpO₂%":       p["vitals"]["spo2"],
        "RR":          p["vitals"]["respiration_rate"],
        "Temp":        p["vitals"]["temperature"],
        "O₂":          "✓" if p["vitals"]["oxygen_supplement"] else "—",
        "NEWS2":       sd["score"],
        "Risk":        sd["risk_level"],
        "Action":      sd["action"],
    })

df = pd.DataFrame(display_data)

# ── Risk cards ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="risk-cards">
    <div class="risk-card red">
        <div class="risk-num red">{metrics['Red']}</div>
        <div class="risk-label">🔴 High Risk — Escalate</div>
    </div>
    <div class="risk-card amber">
        <div class="risk-num amber">{metrics['Amber']}</div>
        <div class="risk-label">🟡 Medium — Urgent Review</div>
    </div>
    <div class="risk-card green">
        <div class="risk-num green">{metrics['Green']}</div>
        <div class="risk-label">🟢 Stable — Routine</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Row styler ────────────────────────────────────────────────────────────────
risk_col  = df.columns.get_loc("Risk")
news2_col = df.columns.get_loc("NEWS2")

def style_row(row):
    risk = row.iloc[risk_col]
    if risk == "High":
        bg, fg = "rgba(248,113,113,0.07)", "#f87171"
    elif risk == "Medium":
        bg, fg = "rgba(251,191,36,0.07)", "#fbbf24"
    else:
        bg, fg = "", "#4ade80"

    styles = [f"background-color:{bg}" if bg else ""] * len(row)
    styles[risk_col]  = f"color:{fg}; font-weight:700"
    styles[news2_col] = f"color:{fg}; font-weight:700; font-family:monospace"
    return styles

st.markdown("### Telemetry Grid")
st.dataframe(
    df.style.apply(style_row, axis=1),
    use_container_width=True,
    hide_index=True,
    height=620,
)

st.markdown("""
<p style="font-size:0.73rem; color:rgba(255,255,255,0.28); margin-top:0.4rem;
          font-family:'JetBrains Mono',monospace;">
NEWS2 ≥7 or single parameter 3 → RED &nbsp;·&nbsp; 5–6 → AMBER &nbsp;·&nbsp;
1–4 → YELLOW &nbsp;·&nbsp; 0 → GREEN
</p>""", unsafe_allow_html=True)
