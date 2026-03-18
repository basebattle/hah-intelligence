# Hospital-at-Home Intelligence Layer

**P10 · Clinical AI Portfolio · Dr. Piyush Sharma (PT, MHA)**

A clinical command center for Hospital-at-Home programmes, applying NEWS2 risk scoring and RAG-based AI synthesis to a simulated 20-patient remote monitoring census. Includes full CMS Acute Hospital Care at Home waiver compliance tracking.

Live: **https://hah-intelligence.streamlit.app**

---

## What It Does

| Module | Function |
|---|---|
| **Census Monitor** | 20-patient telemetry grid · NEWS2 risk stratification · Red/Amber/Green triage |
| **Patient Detail** | Per-patient vitals · NEWS2 parameter breakdown · AI Analysis Engine (RAG + confidence gauge) |
| **Active Alerts** | Auto-generated escalation queue · Sorted by severity · NEWS2 + RAG-driven |
| **CMS Compliance** | 10 AHCaH waiver conditions tracked · Met/At-Risk/Failed status · 42 CFR §412.65 |

---

## Architecture

```
P10-HaH-Intelligence/
├── app.py                     # Landing page — hero, stats, condition grid, module guide
├── pages/
│   ├── 1_Census_Monitor.py    # 20-patient telemetry table with NEWS2 risk cards
│   ├── 2_Patient_Detail.py    # Deep-dive per patient — vitals, NEWS2 breakdown, AI panel
│   ├── 3_Active_Alerts.py     # Escalation queue auto-generated from census
│   └── 4_CMS_Compliance.py    # Waiver protocol tracker (JSON-backed)
├── engine/
│   ├── news2.py               # NEWS2 scoring: 7 vitals → score → Red/Amber/Green + action
│   ├── rag_classifier.py      # RAG risk synthesis combining NEWS2 + clinical notes
│   └── alert_generator.py     # Alert generation engine: severity triage + message templating
├── data/
│   ├── simulator.py           # 20-patient in-memory generator · CONDITION_ICONS · run_simulation()
│   └── cms_waiver_checklist.json  # 10 AHCaH waiver items with status/notes/weight
├── .streamlit/
│   └── config.toml            # Theme: #080F16 bg · #00BFA5 teal · DM Sans font
└── requirements.txt           # streamlit>=1.41.0 · plotly>=5.24.0 · pandas>=2.2.0
```

---

## Clinical Data Model

### Patient Record
Each of the 20 simulated patients carries:
- Demographics: name, age, days in programme, telemetry compliance %
- Diagnosis (9 conditions — see below)
- Vitals: heart_rate, spo2, respiration_rate, systolic_bp, temperature, oxygen_supplement, consciousness (ACVPU)
- Clinical notes (condition-specific, stable or escalated variant)

### Supported Diagnoses

| Diagnosis | Icon | Category |
|---|---|---|
| CHF Exacerbation / Heart Failure | 🫀 | Cardiac |
| COPD Exacerbation | 🫁 | Respiratory |
| Pneumonia | 🫁 | Respiratory |
| Cellulitis | 🦠 | Infectious |
| Sepsis | 🦠 | Infectious |
| UTI / Urosepsis | 💧 | Urological |
| Diabetic Ketoacidosis | 🫘 | Metabolic |
| Chronic Kidney Disease | 🫘 | Renal |
| Post-Surgical | 🌡️ | Surgical |

### NEWS2 Scoring

Seven parameters scored 0–3 each, composite 0–20:

| Score | Risk | Colour | Action |
|---|---|---|---|
| 0 | Low | Green | Routine monitoring |
| 1–4 | Low-Medium | Yellow | Assess + increased monitoring |
| 5–6 | Medium | Amber | Urgent clinical review |
| ≥7 or any single param 3 | High | Red | Emergency escalation |

### CMS AHCaH Waiver (42 CFR §412.65)
Ten conditions of participation tracked, each rated Met / At-Risk / Failed with audit notes and compliance weight.

---

## Tech Stack

| Component | Technology |
|---|---|
| App framework | Streamlit ≥1.41.0 |
| Charts / gauge | Plotly ≥5.24.0 |
| Data manipulation | Pandas ≥2.2.0 |
| Fonts | DM Serif Display · DM Sans · JetBrains Mono (Google Fonts) |
| Hosting | Streamlit Community Cloud |
| Python | 3.12 |

---

## Running Locally

```bash
git clone https://github.com/basebattle/hah-intelligence.git
cd hah-intelligence
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`.

---

## Deployment

Hosted on **Streamlit Community Cloud** (`https://hah-intelligence.streamlit.app`).
Auto-redeploys on every push to `main`.

```
Repository:  basebattle/hah-intelligence
Branch:      main
Main file:   app.py
```

---

## Portfolio Context

This is **Project 10** in the clinical AI portfolio of Dr. Piyush Sharma (PT, MHA).
Portfolio: https://hc-portfolio-zeta.vercel.app

The project demonstrates the clinical intelligence layer required for CMS Hospital-at-Home programme operations — specifically the gap between raw RPM device data and actionable clinical triage.

---

*CMS Acute Hospital Care at Home Waiver · 42 CFR §412.65 · Automated compliance monitoring*
