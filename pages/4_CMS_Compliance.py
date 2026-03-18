import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="CMS Compliance | HaH Intelligence", page_icon="📋",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg:#080F16; --surface:#0F1923; --surface2:#162029;
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

.summary-cards { display:flex; gap:1rem; flex-wrap:wrap; margin:1.25rem 0 1.75rem; }
.summary-card  { flex:1; min-width:140px; background:var(--surface); border:1px solid var(--border);
                 border-radius:14px; padding:1.25rem 1rem; text-align:center; }
.summary-card.met    { border-top:3px solid var(--green); }
.summary-card.at-risk{ border-top:3px solid var(--amber); }
.summary-card.failed { border-top:3px solid var(--red); }
.summary-num  { font-family:'DM Serif Display',serif; font-size:2.4rem; line-height:1; }
.summary-num.met    { color:var(--green); }
.summary-num.at-risk{ color:var(--amber); }
.summary-num.failed { color:var(--red); }
.summary-label{ font-size:0.72rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; margin-top:0.4rem; }

.protocol-card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:14px; padding:1.25rem 1.5rem; margin-bottom:0.75rem;
    border-left:4px solid var(--border);
    display:flex; gap:1rem; align-items:flex-start;
}
.protocol-card.met     { border-left-color:var(--green); }
.protocol-card.at-risk { border-left-color:var(--amber); background:rgba(251,191,36,0.04); }
.protocol-card.failed  { border-left-color:var(--red);   background:rgba(248,113,113,0.06); }

.protocol-status-icon { font-size:1.4rem; min-width:1.4rem; margin-top:1px; }
.protocol-id     { font-family:'JetBrains Mono',monospace; font-size:0.72rem;
                   color:var(--teal); letter-spacing:0.06em; margin-bottom:0.2rem; }
.protocol-title  { font-weight:600; font-size:0.92rem; color:var(--text); margin-bottom:0.3rem; }
.protocol-req    { font-size:0.82rem; color:var(--muted); line-height:1.5; margin-bottom:0.4rem; }
.protocol-notes  { font-size:0.78rem; color:rgba(255,255,255,0.35); font-style:italic; }

.badge { display:inline-block; border-radius:999px; padding:0.2rem 0.65rem;
         font-size:0.68rem; font-weight:700; font-family:'JetBrains Mono',monospace; letter-spacing:0.06em; }
.badge-met     { background:rgba(74,222,128,0.15); color:var(--green); border:1px solid rgba(74,222,128,0.3); }
.badge-at-risk { background:rgba(251,191,36,0.15); color:var(--amber); border:1px solid rgba(251,191,36,0.3); }
.badge-failed  { background:rgba(248,113,113,0.15); color:var(--red);  border:1px solid rgba(248,113,113,0.3); }

.remediation {
    margin-top:0.5rem; padding:0.6rem 0.85rem;
    background:rgba(248,113,113,0.08); border-radius:8px;
    font-size:0.78rem; color:var(--red);
}
</style>
""", unsafe_allow_html=True)

st.html("""
<div class="page-header">📋 CMS Waiver Compliance</div>
<p class="page-sub">
    Acute Hospital Care at Home &nbsp;·&nbsp; Real-time protocol tracking
    &nbsp;·&nbsp; 10 core AHCaH waiver requirements
</p>
""")

st.html("""
<div style="background:var(--surface2); border:1px solid var(--teal-border); border-radius:12px;
            padding:1rem 1.25rem; margin-bottom:1.5rem; font-size:0.83rem; color:var(--muted); line-height:1.6;">
    The <strong style="color:var(--text);">CMS Acute Hospital Care at Home</strong> programme requires strict
    adherence to waiver protocols for each enrolled patient. This dashboard tracks automated compliance
    checks across all active census members. Any <strong style="color:var(--amber);">At-Risk</strong> or
    <strong style="color:var(--red);">Failed</strong> items require immediate remediation to maintain
    programme standing.
</div>
""")


@st.cache_data
def load_waiver_data():
    file_path = Path(__file__).parent.parent / "data" / "cms_waiver_checklist.json"
    with open(file_path, "r") as f:
        return json.load(f)


waivers = load_waiver_data()

counts = {"met": 0, "at_risk": 0, "failed": 0}
for w in waivers:
    s = w["status"]
    if s in counts:
        counts[s] += 1

# ── Summary cards ─────────────────────────────────────────────────────────────
total   = len(waivers)
pct_met = int(counts["met"] / total * 100) if total else 0

st.html(f"""
<div class="summary-cards">
    <div class="summary-card met">
        <div class="summary-num met">{counts['met']}</div>
        <div class="summary-label">✅ Compliant Protocols</div>
    </div>
    <div class="summary-card at-risk">
        <div class="summary-num at-risk">{counts['at_risk']}</div>
        <div class="summary-label">⚠️ At Risk — Monitor</div>
    </div>
    <div class="summary-card failed">
        <div class="summary-num failed">{counts['failed']}</div>
        <div class="summary-label">❌ Failed — Act Now</div>
    </div>
    <div class="summary-card" style="border-top:3px solid var(--teal);">
        <div class="summary-num" style="color:var(--teal);">{pct_met}%</div>
        <div class="summary-label">Overall Compliance</div>
    </div>
</div>
""")

# ── Protocol list ─────────────────────────────────────────────────────────────
st.markdown("### Protocol Status")

STATUS_ICON  = {"met": "✅", "at_risk": "⚠️", "failed": "❌"}
STATUS_CLASS = {"met": "met", "at_risk": "at-risk", "failed": "failed"}
STATUS_LABEL = {"met": "MET", "at_risk": "AT RISK", "failed": "FAILED"}

for w in waivers:
    s      = w["status"]
    cls    = STATUS_CLASS.get(s, "met")
    icon   = STATUS_ICON.get(s, "✅")
    badge  = f'<span class="badge badge-{cls}">{STATUS_LABEL.get(s,"—")}</span>'
    rem    = ('<div class="remediation">⚠️ Immediate remediation required to maintain CMS waiver standing.</div>'
              if s != "met" else "")

    st.html(f"""
<div class="protocol-card {cls}">
    <div class="protocol-status-icon">{icon}</div>
    <div style="flex:1;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.3rem; flex-wrap:wrap;">
            <span class="protocol-id">{w['id']}</span>
            <span class="protocol-title">{w['category']}</span>
            <span style="margin-left:auto;">{badge}</span>
            <span style="font-size:0.7rem; color:var(--muted); font-family:'JetBrains Mono',monospace;">
                {w.get('weight','—')}
            </span>
        </div>
        <div class="protocol-req">{w['requirement']}</div>
        <div class="protocol-notes">Audit: {w['notes']}</div>
        {rem}
    </div>
</div>
""")

st.html("""
<p style="font-size:0.73rem; color:rgba(255,255,255,0.25); margin-top:1rem;
          font-family:'JetBrains Mono',monospace;">
    CMS Acute Hospital Care at Home Waiver &nbsp;·&nbsp; 42 CFR §412.65
    &nbsp;·&nbsp; Automated compliance monitoring
</p>
""")
