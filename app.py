import streamlit as st

st.set_page_config(
    page_title="HaH Intelligence | P10 — Dr. Piyush Sharma",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:          #080F16;
    --surface:     #0F1923;
    --surface2:    #162029;
    --teal:        #00BFA5;
    --teal-dim:    rgba(0,191,165,0.12);
    --teal-border: rgba(0,191,165,0.30);
    --teal-glow:   0 0 24px rgba(0,191,165,0.20);
    --red:         #f87171;
    --amber:       #fbbf24;
    --green:       #4ade80;
    --text:        #FFFFFF;
    --muted:       rgba(255,255,255,0.52);
    --border:      rgba(255,255,255,0.07);
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
[data-testid="stSidebar"] {
    background-color: #060C12 !important;
    border-right: 1px solid var(--border);
}

/* ── Hero ──────────────────────────────────────────────── */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
}
.hero-badge {
    display: inline-block;
    background: var(--teal-dim);
    border: 1px solid var(--teal-border);
    border-radius: 999px;
    padding: 0.35rem 1.1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--teal);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.75rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    line-height: 1.08;
    margin: 0 auto 1rem;
    max-width: 820px;
    background: linear-gradient(135deg, #FFFFFF 30%, var(--teal) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 640px;
    margin: 0 auto 0.75rem;
    line-height: 1.7;
    font-weight: 300;
}
.hero-attribution {
    font-size: 0.88rem;
    color: var(--muted);
    margin-bottom: 2rem;
}
.hero-attribution a {
    color: var(--teal);
    text-decoration: none;
    border-bottom: 1px solid rgba(0,191,165,0.35);
    padding-bottom: 1px;
}
.hero-pills {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}
.pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.38rem 0.95rem;
    font-size: 0.78rem;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.03em;
}
.pill-teal {
    border-color: var(--teal-border);
    color: var(--teal);
    background: var(--teal-dim);
}

/* ── Stats Bar ──────────────────────────────────────────── */
.stats-bar {
    display: flex;
    justify-content: center;
    margin: 2.5rem auto;
    max-width: 760px;
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    background: var(--surface);
}
.stat-item {
    flex: 1;
    text-align: center;
    padding: 1.4rem 0.5rem;
    border-right: 1px solid var(--border);
}
.stat-item:last-child { border-right: none; }
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: var(--teal);
    line-height: 1;
}
.stat-label {
    font-size: 0.68rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.4rem;
}

/* ── Section Header ─────────────────────────────────────── */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.65rem;
    color: var(--text);
    margin: 2.5rem 0 0.4rem;
    line-height: 1.2;
}
.section-sub {
    font-size: 0.88rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
}

/* ── Condition Cards ────────────────────────────────────── */
.condition-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
    gap: 1rem;
    margin: 1.25rem 0 2rem;
}
.condition-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.25rem;
    text-align: center;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
}
.condition-card:hover {
    border-color: var(--teal-border);
    box-shadow: var(--teal-glow);
    transform: translateY(-3px);
}
.condition-icon-wrap {
    font-size: 2.6rem;
    display: block;
    margin-bottom: 0.85rem;
    line-height: 1;
}
.condition-name {
    font-weight: 600;
    font-size: 0.92rem;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.condition-desc {
    font-size: 0.76rem;
    color: var(--muted);
    line-height: 1.5;
}

/* ── Module Cards ───────────────────────────────────────── */
.module-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1rem;
    margin: 1.25rem 0 2rem;
}
.module-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--teal);
    border-radius: 12px;
    padding: 1.5rem;
    transition: box-shadow 0.3s ease, transform 0.2s ease;
}
.module-card:hover {
    box-shadow: var(--teal-glow);
    transform: translateY(-2px);
}
.module-icon { font-size: 1.8rem; margin-bottom: 0.75rem; }
.module-title { font-weight: 600; font-size: 1rem; color: var(--text); margin-bottom: 0.4rem; }
.module-desc  { font-size: 0.81rem; color: var(--muted); line-height: 1.55; }

/* ── How-It-Works ───────────────────────────────────────── */
.hiw-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
}
.how-step {
    display: flex;
    align-items: flex-start;
    gap: 1.1rem;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
}
.how-step:last-child  { border-bottom: none; padding-bottom: 0; }
.how-step:first-child { padding-top: 0; }
.step-num {
    min-width: 2rem; width: 2rem; height: 2rem;
    background: var(--teal-dim);
    border: 1px solid var(--teal-border);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; color: var(--teal);
    flex-shrink: 0; margin-top: 2px;
}
.step-title { font-weight: 600; font-size: 0.93rem; color: var(--text); }
.step-body  { font-size: 0.81rem; color: var(--muted); margin: 0.2rem 0 0; line-height: 1.55; }

/* ── Portfolio Card ─────────────────────────────────────── */
.portfolio-card {
    background: var(--surface);
    border: 1px solid var(--teal-border);
    border-radius: 16px;
    padding: 1.75rem;
    text-align: center;
}
.btn-teal {
    display: inline-block;
    background: var(--teal);
    color: #000 !important;
    padding: 0.55rem 1.4rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    text-decoration: none !important;
    letter-spacing: 0.02em;
}

/* ── Footer ─────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 2.5rem 1rem;
    border-top: 1px solid var(--border);
    margin-top: 4rem;
    color: var(--muted);
    font-size: 0.82rem;
}
.footer a { color: var(--teal); text-decoration: none; }
.footer-quote {
    font-family: 'DM Serif Display', serif;
    font-style: italic;
    font-size: 0.92rem;
    color: rgba(255,255,255,0.28);
    margin-top: 1rem;
    line-height: 1.5;
}

/* ── Animations ─────────────────────────────────────────── */
@keyframes heartbeat {
    0%,100% { transform: scale(1); }
    14%     { transform: scale(1.22); }
    28%     { transform: scale(1); }
    42%     { transform: scale(1.14); }
    56%     { transform: scale(1); }
}
@keyframes breathe {
    0%,100% { transform: scale(1); }
    50%     { transform: scaleX(1.10) scaleY(1.14); }
}
@keyframes kidney-rock {
    0%,100% { transform: rotate(-6deg) scale(1); }
    50%     { transform: rotate(6deg) scale(1.09); }
}
@keyframes glow-pulse {
    0%,100% { opacity: 0.65; transform: scale(1); }
    50%     { opacity: 1;    transform: scale(1.12); }
}
@keyframes drop-bounce {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-5px); }
}
@keyframes temp-throb {
    0%,100% { filter: hue-rotate(0deg); }
    50%     { filter: hue-rotate(30deg) brightness(1.2); }
}

.anim-heart  { animation: heartbeat   1.3s ease-in-out infinite; display:inline-block; }
.anim-lung   { animation: breathe     2.2s ease-in-out infinite; display:inline-block; }
.anim-kidney { animation: kidney-rock 2.4s ease-in-out infinite; display:inline-block; }
.anim-glow   { animation: glow-pulse  1.8s ease-in-out infinite; display:inline-block; }
.anim-drop   { animation: drop-bounce 1.6s ease-in-out infinite; display:inline-block; }
.anim-temp   { animation: temp-throb  2.0s ease-in-out infinite; display:inline-block; }

/* Streamlit overrides */
[data-testid="stMarkdownContainer"] > p { color: var(--muted); }
.stButton > button {
    background: var(--teal-dim) !important;
    border: 1px solid var(--teal-border) !important;
    color: var(--teal) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover { background: rgba(0,191,165,0.22) !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">P10 &nbsp;·&nbsp; Clinical AI Portfolio &nbsp;·&nbsp; Dr. Piyush Sharma</div>

    <h1 class="hero-title">Hospital-at-Home<br>Intelligence Layer</h1>

    <p class="hero-subtitle">
        A real-time clinical monitoring system for the CMS Acute Hospital Care at Home programme —
        combining <strong style="color:#fff;">NEWS2 physiological scoring</strong> with
        <strong style="color:#fff;">LLM-driven RAG analysis</strong> to detect patient
        deterioration before it escalates to an emergency.
    </p>

    <p class="hero-attribution">
        Built by&nbsp;
        <a href="https://hc-portfolio-zeta.vercel.app/" target="_blank">Dr. Piyush Sharma (PT, MHA)</a>
        &nbsp;·&nbsp; Senior Healthcare Consultant
        &nbsp;·&nbsp; Clinical Informatics &amp; Agentic AI
    </p>

    <div class="hero-pills">
        <span class="pill pill-teal">NEWS2 Scoring Engine</span>
        <span class="pill pill-teal">LLM RAG Analysis</span>
        <span class="pill pill-teal">CMS AHCaH Compliant</span>
        <span class="pill">20-Patient Live Cohort</span>
        <span class="pill">Real-Time Telemetry</span>
        <span class="pill">Auto Escalation Alerts</span>
    </div>
</div>

<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-num">20</div>
        <div class="stat-label">Active Patients</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">7</div>
        <div class="stat-label">Conditions Tracked</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">NEWS2</div>
        <div class="stat-label">Scoring Standard</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">4</div>
        <div class="stat-label">Clinical Modules</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">CMS</div>
        <div class="stat-label">AHCaH Waiver</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.07); margin:0.5rem 0 2rem;"></div>',
            unsafe_allow_html=True)

# ── CONDITIONS ────────────────────────────────────────────────────────────────
st.markdown("""
<h2 class="section-header">Monitored Conditions</h2>
<p class="section-sub">Each condition triggers a specialised clinical protocol, risk weighting, and escalation threshold.</p>

<div class="condition-grid">

    <div class="condition-card">
        <span class="condition-icon-wrap"><span class="anim-heart">🫀</span></span>
        <div class="condition-name">Heart Failure / CHF</div>
        <div class="condition-desc">CHF exacerbation monitoring via heart rate, systolic BP, and fluid retention markers</div>
    </div>

    <div class="condition-card">
        <span class="condition-icon-wrap"><span class="anim-lung">🫁</span></span>
        <div class="condition-name">COPD / Pneumonia</div>
        <div class="condition-desc">Respiratory deterioration via SpO₂ trending, respiratory rate, and supplemental O₂ requirement</div>
    </div>

    <div class="condition-card">
        <span class="condition-icon-wrap"><span class="anim-kidney">🫘</span></span>
        <div class="condition-name">Diabetic / CKD</div>
        <div class="condition-desc">DKA onset detection and chronic kidney disease decompensation flags via haemodynamic markers</div>
    </div>

    <div class="condition-card">
        <span class="condition-icon-wrap"><span class="anim-glow">🦠</span></span>
        <div class="condition-name">Cellulitis / Sepsis</div>
        <div class="condition-desc">Infection cascade early warning — temperature spike, tachycardia, and consciousness change</div>
    </div>

    <div class="condition-card">
        <span class="condition-icon-wrap"><span class="anim-drop">💧</span></span>
        <div class="condition-name">UTI / Urosepsis</div>
        <div class="condition-desc">Urological infection progression with automatic urosepsis escalation triggers</div>
    </div>

    <div class="condition-card">
        <span class="condition-icon-wrap"><span class="anim-temp">🌡️</span></span>
        <div class="condition-name">Post-Surgical</div>
        <div class="condition-desc">Post-operative monitoring, fever surveillance, and early wound complication flags</div>
    </div>

</div>
""", unsafe_allow_html=True)

# ── MODULES ───────────────────────────────────────────────────────────────────
st.markdown("""
<h2 class="section-header">System Modules</h2>
<p class="section-sub">Navigate using the sidebar — each module serves a distinct clinical function.</p>

<div class="module-grid">

    <div class="module-card">
        <div class="module-icon">👥</div>
        <div class="module-title">Census Monitor</div>
        <div class="module-desc">
            Live 20-patient cohort with condition icons, NEWS2 scores, and one-click
            telemetry refresh. Red / Amber / Green risk stratification at a glance.
        </div>
    </div>

    <div class="module-card">
        <div class="module-icon">🩻</div>
        <div class="module-title">Patient Detail</div>
        <div class="module-desc">
            Drill into any patient — full vitals panel, AI confidence gauge,
            LLM-synthesised risk reasoning, and clinical notes.
        </div>
    </div>

    <div class="module-card">
        <div class="module-icon">🚨</div>
        <div class="module-title">Active Alerts</div>
        <div class="module-desc">
            Auto-generated escalation queue ranked CRITICAL → HIGH → MEDIUM.
            Each alert carries a one-line action summary and patient context.
        </div>
    </div>

    <div class="module-card">
        <div class="module-icon">📋</div>
        <div class="module-title">CMS Compliance</div>
        <div class="module-desc">
            Real-time AHCaH waiver protocol tracking. Met / At-Risk / Failed
            per requirement, with audit notes and remediation guidance.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.07); margin:0.5rem 0 2.5rem;"></div>',
            unsafe_allow_html=True)

# ── HOW IT WORKS + PORTFOLIO ──────────────────────────────────────────────────
col_hiw, col_portfolio = st.columns([3, 2], gap="large")

with col_hiw:
    st.markdown("""
<h2 class="section-header">How It Works</h2>
<p class="section-sub">Four layers of clinical intelligence operating in concert.</p>

<div class="hiw-wrap">
    <div class="how-step">
        <div class="step-num">01</div>
        <div>
            <div class="step-title">Telemetry Ingestion</div>
            <p class="step-body">Wearable vitals — HR, SpO₂, RR, systolic BP, temperature, consciousness level — stream continuously from each home patient. Hit <em>Refresh Vitals</em> in Census Monitor to pull the latest read.</p>
        </div>
    </div>
    <div class="how-step">
        <div class="step-num">02</div>
        <div>
            <div class="step-title">NEWS2 Algorithmic Scoring</div>
            <p class="step-body">Each vital is scored against the validated National Early Warning Score 2 rubric. A composite 0–20 score determines the Red / Amber / Green risk tier and mandates the appropriate clinical action pathway.</p>
        </div>
    </div>
    <div class="how-step">
        <div class="step-num">03</div>
        <div>
            <div class="step-title">LLM RAG Synthesis</div>
            <p class="step-body">Clinical notes are processed through a Retrieval-Augmented Generation pipeline that cross-references the NEWS2 result against structured clinical knowledge, producing a synthesised risk classification with a confidence score.</p>
        </div>
    </div>
    <div class="how-step">
        <div class="step-num">04</div>
        <div>
            <div class="step-title">Escalation &amp; Compliance</div>
            <p class="step-body">The alert engine converts Red / High-risk findings into ranked escalation actions. CMS AHCaH compliance is checked in real time against 10 core waiver requirements.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with col_portfolio:
    st.markdown("""
<h2 class="section-header">About This Project</h2>
<p class="section-sub">Part of a 10-project production portfolio.</p>

<div class="portfolio-card">
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:var(--teal);
                letter-spacing:0.1em; margin-bottom:1rem;">P10 OF 10</div>
    <div style="font-family:'DM Serif Display',serif; font-size:1.2rem; color:var(--text); margin-bottom:0.25rem;">
        Dr. Piyush Sharma</div>
    <div style="font-family:'DM Serif Display',serif; font-style:italic; font-size:0.95rem;
                color:var(--muted); margin-bottom:0.85rem;">PT, MHA</div>
    <div style="margin:0.5rem 0 1rem; display:flex; gap:0.4rem; justify-content:center; flex-wrap:wrap;">
        <span class="pill pill-teal" style="font-size:0.7rem;">Clinical Informatics</span>
        <span class="pill pill-teal" style="font-size:0.7rem;">Agentic AI</span>
    </div>
    <p style="font-size:0.8rem; color:var(--muted); line-height:1.55; margin-bottom:1.25rem;">
        Senior Healthcare Consultant at the intersection of clinical AI and US payer-provider
        operations. 10 production systems. $2.8M projected annual impact.
    </p>
    <div style="border-top:1px solid var(--border); padding-top:1rem; margin-bottom:1.25rem; text-align:left;">
        <div style="font-size:0.75rem; color:var(--muted); line-height:2.0;">
            <div>🏥 &nbsp;Clinical systems &amp; physiotherapy background</div>
            <div>📊 &nbsp;Strategy consulting — global Health &amp; Life Sciences</div>
            <div>🤖 &nbsp;FHIR · CDS Hooks · LangGraph · MCP</div>
            <div>🇺🇸 &nbsp;US payer-provider operations expertise</div>
        </div>
    </div>
    <a class="btn-teal" href="https://hc-portfolio-zeta.vercel.app/" target="_blank">
        View Full Portfolio →
    </a>
</div>

<div style="background:var(--surface); border:1px solid var(--border); border-radius:12px;
            padding:1.25rem; margin-top:1rem;">
    <div style="font-size:0.7rem; color:var(--teal); font-family:'JetBrains Mono',monospace;
                letter-spacing:0.08em; margin-bottom:0.75rem;">TECH STACK</div>
    <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
        <span class="pill pill-teal" style="font-size:0.7rem;">Python 3.12</span>
        <span class="pill pill-teal" style="font-size:0.7rem;">Streamlit</span>
        <span class="pill" style="font-size:0.7rem;">NEWS2 Engine</span>
        <span class="pill" style="font-size:0.7rem;">RAG Classifier</span>
        <span class="pill" style="font-size:0.7rem;">Plotly</span>
        <span class="pill pill-teal" style="font-size:0.7rem;">Streamlit Cloud</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <strong style="color:var(--text);">HaH Intelligence Layer</strong>
    &nbsp;·&nbsp; P10 of 10
    &nbsp;·&nbsp; Built by
    <a href="https://hc-portfolio-zeta.vercel.app/" target="_blank">Dr. Piyush Sharma (PT, MHA)</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/basebattle" target="_blank">GitHub</a>
    &nbsp;·&nbsp;
    <a href="mailto:career.sharmapiyush@gmail.com">Contact</a>
    <div class="footer-quote">
        "I am not a developer who learned healthcare. I am a clinician who learned to build."
    </div>
</div>
""", unsafe_allow_html=True)
