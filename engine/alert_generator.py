import uuid
from datetime import datetime

def generate_alerts(patient: dict) -> list:
    """
    Generates actionable alerts based on patient state.
    """
    alerts = []
    
    if patient.get('status') == 'Escalated':
        alerts.append({
            "id": str(uuid.uuid4()),
            "patient_id": patient['id'],
            "patient_name": patient['name'],
            "type": "Clinical Escalation",
            "severity": "CRITICAL",
            "message": "Patient requires immediate transfer to acute care (NEWS2 or Note analysis indicates severe deterioration).",
            "timestamp": datetime.now().isoformat()
        })
    elif patient.get('status') == 'At_Risk':
        alerts.append({
            "id": str(uuid.uuid4()),
            "patient_id": patient['id'],
            "patient_name": patient['name'],
            "type": "Clinical Warning",
            "severity": "HIGH",
            "message": "Patient is at risk. Urgent clinician telehealth or dispatch required.",
            "timestamp": datetime.now().isoformat()
        })

    # Add operational alerts
    if patient.get('telemetry_compliance', 100) < 80:
        alerts.append({
            "id": str(uuid.uuid4()),
            "patient_id": patient['id'],
            "patient_name": patient['name'],
            "type": "Operational",
            "severity": "MEDIUM",
            "message": "Telemetry compliance dropped below 80%. Check device connection.",
            "timestamp": datetime.now().isoformat()
        })

    return alerts
