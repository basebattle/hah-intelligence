import random

# ── Condition → Icon mapping (imported by all pages) ─────────────────────────
CONDITION_ICONS = {
    "CHF Exacerbation":       "🫀",
    "Heart Failure":          "🫀",
    "COPD Exacerbation":      "🫁",
    "Pneumonia":              "🫁",
    "Cellulitis":             "🦠",
    "Sepsis":                 "🦠",
    "UTI":                    "💧",
    "Urosepsis":              "💧",
    "Diabetic Ketoacidosis":  "🫘",
    "Chronic Kidney Disease": "🫘",
    "Post-Surgical":          "🌡️",
}

_PATIENT_NAMES = [
    "Margaret T.", "James W.",    "Dorothy H.", "Robert K.",  "Helen B.",
    "William F.",  "Betty M.",    "Charles A.", "Frances L.", "Thomas P.",
    "Ruth N.",     "George S.",   "Virginia C.","Harold D.",  "Evelyn R.",
    "Arthur J.",   "Mildred O.",  "Walter E.",  "Louise G.",  "Raymond V.",
]

_DIAGNOSES = [
    "CHF Exacerbation",
    "COPD Exacerbation",
    "Pneumonia",
    "Cellulitis",
    "UTI",
    "Diabetic Ketoacidosis",
    "Chronic Kidney Disease",
    "Sepsis",
    "Post-Surgical",
]

_CLINICAL_NOTES = {
    "CHF Exacerbation":
        "Patient reports progressive bilateral ankle oedema and orthopnoea. "
        "3-pillow orthopnoea overnight. Weight gain 2.3 kg over 3 days. "
        "JVP elevated; basal crepitations on auscultation.",
    "COPD Exacerbation":
        "Increased sputum production — purulent and yellow-green. Audible wheeze "
        "at rest. Patient using rescue inhaler 6–8× daily vs usual 2×. Reports "
        "significant increase in dyspnoea on minimal exertion.",
    "Pneumonia":
        "Productive cough with rusty sputum. Dullness to percussion right base. "
        "Patient febrile with rigors overnight. Appetite markedly reduced. "
        "O₂ requirement 2L NC to maintain SpO₂ ≥94%.",
    "Cellulitis":
        "Erythema and warmth extending proximally from right lower leg wound. "
        "Margins marked yesterday now spread ~2 cm. Throbbing pain increasing. "
        "No lymphangitis visible. Afebrile this morning.",
    "UTI":
        "Dysuria and frequency for 2 days. Cloudy, malodorous urine. "
        "Suprapubic tenderness on palpation. New agitation today — possible "
        "baseline confusion. Urine dip positive nitrites and leucocytes.",
    "Diabetic Ketoacidosis":
        "Patient reports nausea, vomiting, and abdominal pain since this morning. "
        "Fruity breath odour noted by carer. BGL 18.4 mmol/L on home monitor. "
        "Missed 2 insulin doses this week.",
    "Chronic Kidney Disease":
        "eGFR trending down over past 3 programme days. Patient reporting fatigue "
        "and mild peripheral oedema. Dietary non-compliance flagged by dietitian. "
        "Fluid restriction poorly adhered to per carer report.",
    "Sepsis":
        "Carer reports sudden deterioration over 4 hours. Patient confused and "
        "pyrexial. Source unclear — possible respiratory or urinary origin. "
        "HR elevated from baseline 72 to 118. Last fluid intake unknown.",
    "Post-Surgical":
        "Day 5 post right-knee arthroplasty. Wound site erythematous with slight "
        "serous ooze from inferior margin. Low-grade temp today vs afebrile yesterday. "
        "Full weight-bearing achieved in physio session.",
}

_STABLE_NOTES = {
    "CHF Exacerbation":       "Stable — weight steady, no new oedema. Tolerating diuretic well.",
    "COPD Exacerbation":      "Stable — SpO₂ 97% room air. Sputum reducing, wheeze resolving.",
    "Pneumonia":              "Stable — afebrile 24 h. Cough productive but improving on antibiotics.",
    "Cellulitis":             "Stable — erythema margins receding. Wound clean, afebrile.",
    "UTI":                    "Stable — dysuria resolving on antibiotics. Urine clearing.",
    "Diabetic Ketoacidosis":  "Stable — glucose 7.2 mmol/L. Insulin compliance restored.",
    "Chronic Kidney Disease": "Stable — eGFR holding. Fluid restriction adhered to today.",
    "Sepsis":                 "Stable — afebrile 12 h. Source identified and being treated.",
    "Post-Surgical":          "Stable — wound clean and dry. Physio goals on track.",
}


def get_base_patients():
    """Generate a fresh 20-patient cohort in memory (12 Green, 5 Amber, 3 Red)."""
    statuses = ["Stable"] * 12 + ["At_Risk"] * 5 + ["Escalated"] * 3
    random.shuffle(statuses)

    names_pool = _PATIENT_NAMES.copy()
    random.shuffle(names_pool)

    patients = []
    for i, status in enumerate(statuses):
        diagnosis = random.choice(_DIAGNOSES)

        if status == "Stable":
            vitals = {
                "respiration_rate":  random.randint(12, 18),
                "spo2":              random.randint(96, 100),
                "oxygen_supplement": False,
                "systolic_bp":       random.randint(112, 138),
                "heart_rate":        random.randint(62, 88),
                "temperature":       round(random.uniform(36.2, 37.4), 1),
                "consciousness":     "Alert",
            }
            notes = _STABLE_NOTES[diagnosis]

        elif status == "At_Risk":
            vitals = {
                "respiration_rate":  random.randint(21, 24),
                "spo2":              random.randint(92, 95),
                "oxygen_supplement": random.choice([True, False]),
                "systolic_bp":       random.randint(92, 102),
                "heart_rate":        random.randint(92, 110),
                "temperature":       round(random.uniform(37.6, 38.6), 1),
                "consciousness":     "Alert",
            }
            notes = _CLINICAL_NOTES[diagnosis]

        else:  # Escalated
            vitals = {
                "respiration_rate":  random.randint(25, 32),
                "spo2":              random.randint(85, 91),
                "oxygen_supplement": True,
                "systolic_bp":       random.randint(78, 91),
                "heart_rate":        random.randint(112, 138),
                "temperature":       round(random.uniform(38.7, 39.6), 1),
                "consciousness":     random.choice(["Alert", "Voice", "Pain"]),
            }
            notes = _CLINICAL_NOTES[diagnosis]

        patients.append({
            "id":                   f"HAH-{1000 + i}",
            "name":                 names_pool[i],
            "age":                  random.randint(56, 84),
            "diagnosis":            diagnosis,
            "status":               status,
            "days_in_program":      random.randint(1, 14),
            "vitals":               vitals,
            "telemetry_compliance": (random.randint(72, 100)
                                     if status != "Escalated"
                                     else random.randint(91, 100)),
            "clinical_notes":       notes,
        })

    return patients


def run_simulation(patients=None):
    """Fuzz vitals slightly to simulate live streaming data."""
    if not patients:
        patients = get_base_patients()
    for p in patients:
        if random.random() < 0.25:
            p["vitals"]["heart_rate"]  = max(40, p["vitals"]["heart_rate"]  + random.randint(-6, 6))
            p["vitals"]["systolic_bp"] = max(70, p["vitals"]["systolic_bp"] + random.randint(-6, 6))
        if random.random() < 0.12:
            p["vitals"]["spo2"] = max(82, min(100, p["vitals"]["spo2"] + random.randint(-2, 2)))
        if random.random() < 0.10:
            p["vitals"]["respiration_rate"] = max(8, p["vitals"]["respiration_rate"] + random.randint(-2, 2))
    return patients
