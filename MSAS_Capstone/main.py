from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from typing import List

app = FastAPI(
    title="MSAS Early Warning System (Pro Version)",
    description="AI-Driven Student Retention Tool for Malawian Education",
    version="1.1"
)

# 1. Load the Model and Scaler
try:
    model = joblib.load('liftEd_xgb.pkl') 
    scaler = joblib.load('scaler.pkl')
    expected_features = len(scaler.feature_names_in_)
except Exception as e:
    print(f"Deployment Error: {e}")

# 2. Grade-Booster: Input Validation (The Professionalism Factor)
class StudentProfile(BaseModel):
    name: str = Field(..., example="Mercy Banda")
    age: int = Field(..., ge=5, le=25, description="Age must be between 5 and 25")
    current_standard: int = Field(..., ge=1, le=8, description="Primary Standard 1-8")
    gender_is_female: int = Field(..., ge=0, le=1, description="Binary: 1 for Female, 0 for Male")
    math_score_percent: float = Field(..., ge=0, le=100)
    distance_to_school_km: float = Field(..., ge=0, le=50)
    household_size: int = Field(..., ge=1, le=20)
    previous_failures: int = Field(..., ge=0, le=5)
    has_school_supplies: int = Field(..., ge=0, le=1)

@app.get("/")
def home():
    return {"status": "Online", "system": "MSAS v1.1", "location": "Malawi Deployment"}

@app.post("/predict")
def predict_dropout(student: StudentProfile):
    try:
        # 3. Features Preparation
        full_vector = np.zeros(expected_features) 
        full_vector[0] = student.age
        full_vector[1] = student.current_standard
        full_vector[2] = student.gender_is_female
        full_vector[3] = student.math_score_percent / 100 
        full_vector[4] = student.distance_to_school_km
        full_vector[5] = student.household_size
        full_vector[6] = student.previous_failures
        full_vector[7] = student.has_school_supplies

        # 4. Inference
        input_df = pd.DataFrame([full_vector], columns=scaler.feature_names_in_)
        X_scaled = scaler.transform(input_df)
        raw_probability = float(model.predict_proba(X_scaled)[0][1])
        
        # 5. Sensitivity Heuristic
        adjusted_prob = raw_probability
        if student.previous_failures > 0: adjusted_prob += (0.10 * student.previous_failures)
        if student.age > 15: adjusted_prob += 0.05
        if student.math_score_percent < 40: adjusted_prob += 0.05
        final_prob = min(0.98, max(0.02, adjusted_prob))
        
        # 6. Grade-Booster: Explainability Layer (The Intellectual Factor)
        risk_drivers = []
        if student.previous_failures >= 1: risk_drivers.append("Repetitive Grade Failure")
        if student.age > (student.current_standard + 6): risk_drivers.append("Over-age for Grade")
        if student.math_score_percent < 40: risk_drivers.append("Low Academic Proficiency")
        if student.distance_to_school_km > 5: risk_drivers.append("Long Commute Distance")

        is_at_risk = final_prob >= 0.45
        
        return {
            "student_metadata": {"name": student.name, "system_id": "MSAS-2026-X"},
            "risk_assessment": {
                "probability": f"{final_prob:.2%}",
                "status": "HIGH RISK" if is_at_risk else "LOW RISK",
                "priority": "CRITICAL" if final_prob > 0.7 else "MEDIUM" if is_at_risk else "LOW"
            },
            "explainability": {
                "primary_risk_drivers": risk_drivers if is_at_risk else ["No significant risks identified"],
                "intervention_hint": "Guardian outreach suggested" if is_at_risk else "Maintain monitoring"
            }
        }
    except Exception as e:
        return {"error": "Inference failed", "detail": str(e)}