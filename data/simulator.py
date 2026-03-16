import json
import random
from pathlib import Path

def get_base_patients():
    data_file = Path(__file__).parent / 'patients.json'
    if not data_file.exists():
        # Generate 20 patients (12 Green, 5 Amber, 3 Red)
        patients = []
        statuses = ['Stable'] * 12 + ['At_Risk'] * 5 + ['Escalated'] * 3
        
        for i, status in enumerate(statuses):
            # Base vitals dependent on status
            if status == 'Stable':
                vitals = {
                    "respiration_rate": random.randint(12, 20),
                    "spo2": random.randint(96, 100),
                    "oxygen_supplement": False,
                    "systolic_bp": random.randint(110, 140),
                    "heart_rate": random.randint(60, 90),
                    "temperature": round(random.uniform(36.1, 37.5), 1),
                    "consciousness": "Alert"
                }
            elif status == 'At_Risk':
                vitals = {
                    "respiration_rate": random.randint(21, 24),
                    "spo2": random.randint(92, 95),
                    "oxygen_supplement": random.choice([True, False]),
                    "systolic_bp": random.randint(91, 100),
                    "heart_rate": random.randint(91, 110),
                    "temperature": round(random.uniform(37.6, 38.5), 1),
                    "consciousness": "Alert"
                }
            else:
                vitals = {
                    "respiration_rate": random.randint(25, 30),
                    "spo2": random.randint(85, 91),
                    "oxygen_supplement": True,
                    "systolic_bp": random.randint(80, 90),
                    "heart_rate": random.randint(111, 135),
                    "temperature": round(random.uniform(38.6, 39.5), 1),
                    "consciousness": random.choice(["Alert", "Voice", "Pain"])
                }
                
            patient = {
                "id": f"HAH-{1000 + i}",
                "name": f"Patient {i+1}",
                "age": random.randint(55, 85),
                "diagnosis": random.choice(["CHF Exacerbation", "COPD Exacerbation", "Cellulitis", "Pneumonia", "UTI"]),
                "status": status,
                "admit_date": f"2026-10-{random.randint(1, 15):02d}",
                "days_in_program": random.randint(1, 14),
                "vitals": vitals,
                "telemetry_compliance": random.randint(70, 100) if status != 'Escalated' else random.randint(90, 100),
                "clinical_notes": "Patient reports feeling okay." if status == 'Stable' else "Patient reports increased fatigue and shortness of breath."
            }
            patients.append(patient)
            
        with open(data_file, 'w') as f:
            json.dump(patients, f, indent=2)
            
        return patients
        
    with open(data_file, 'r') as f:
        return json.load(f)

def run_simulation(patients=None):
    """Slightly fuzzes vitals to simulate streaming data."""
    if not patients:
        patients = get_base_patients()
        
    for p in patients:
        # 10% chance to slightly alter a vital
        if random.random() < 0.1:
            p['vitals']['heart_rate'] += random.randint(-5, 5)
            p['vitals']['systolic_bp'] += random.randint(-5, 5)
            
    return patients
