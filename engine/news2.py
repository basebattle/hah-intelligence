def calculate_news2(vitals: dict) -> dict:
    """
    Calculates the National Early Warning Score 2 (NEWS2).
    Requires: respiration_rate, spo2, oxygen_supplement (bool), temperature, systolic_bp, heart_rate, consciousness.
    """
    score = 0
    breakdown = {}

    # Respiration Rate
    rr = vitals.get('respiration_rate')
    if rr is not None:
        if rr <= 8 or rr >= 25: s = 3
        elif rr in (9, 10, 11) or rr in (21, 22, 23, 24): s = 1
        else: s = 0
        score += s
        breakdown['Respiration'] = s

    # SpO2 (Scale 1 - Not specifying Scale 2 for COPD for simplicity)
    spo2 = vitals.get('spo2')
    if spo2 is not None:
        if spo2 <= 91: s = 3
        elif spo2 in (92, 93): s = 2
        elif spo2 in (94, 95): s = 1
        else: s = 0
        score += s
        breakdown['SpO2'] = s

    # Oxygen Supplement
    o2_supp = vitals.get('oxygen_supplement', False)
    if o2_supp:
        score += 2
        breakdown['O2 Supplement'] = 2
    else:
        breakdown['O2 Supplement'] = 0

    # Systolic BP
    sbp = vitals.get('systolic_bp')
    if sbp is not None:
        if sbp <= 90 or sbp >= 220: s = 3
        elif sbp in range(91, 101): s = 2
        elif sbp in range(101, 111): s = 1
        else: s = 0
        score += s
        breakdown['Systolic BP'] = s

    # Heart Rate
    hr = vitals.get('heart_rate')
    if hr is not None:
        if hr <= 40 or hr >= 131: s = 3
        elif hr in range(111, 131): s = 2
        elif hr in range(41, 51) or hr in range(91, 111): s = 1
        else: s = 0
        score += s
        breakdown['Heart Rate'] = s

    # Temperature
    temp = vitals.get('temperature')
    if temp is not None:
        if temp <= 35.0: s = 3
        elif temp >= 39.1: s = 2
        elif (temp >= 35.1 and temp <= 36.0) or (temp >= 38.1 and temp <= 39.0): s = 1
        else: s = 0
        score += s
        breakdown['Temperature'] = s

    # Consciousness (ACVPU: Alert=0, C/V/P/U=3)
    loc = vitals.get('consciousness', 'Alert')
    if loc != 'Alert':
        score += 3
        breakdown['Consciousness'] = 3
    else:
        breakdown['Consciousness'] = 0

    # Risk level determination
    risk = "Low"
    color = "Green"
    action = "Ward-level monitoring (12-hourly)"
    
    if score >= 7 or any(v == 3 for v in breakdown.values()):
        risk = "High"
        color = "Red"
        action = "Emergency Assessment. Transfer to acute care."
    elif score >= 5:
        risk = "Medium"
        color = "Amber"
        action = "Urgent Assessment. Urgent response by clinician."
    elif score >= 1:
        risk = "Low-Medium"
        color = "Yellow"
        action = "Increase monitoring frequency to 4-6 hourly."

    return {
        "score": score,
        "risk_level": risk,
        "color": color,
        "action": action,
        "breakdown": breakdown
    }
