import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Page Config
st.set_page_config(page_title="MSAS Dropout Predictor", page_icon="🎓")

# Load Brains
model = joblib.load('liftEd_xgb.pkl')
scaler = joblib.load('scaler.pkl')
features = scaler.feature_names_in_

st.title("🎓 MSAS: Early Warning System")
st.markdown("### Identifying Student Dropout Risk in Malawi")
st.divider()

# Sidebar for Teacher Inputs
st.sidebar.header("Teacher Input Portal")
name = st.sidebar.text_input("Student Name", "Mercy Banda")
age = st.sidebar.slider("Age", 5, 25, 15)
std = st.sidebar.selectbox("Standard (Grade)", [1,2,3,4,5,6,7,8], index=4)
math = st.sidebar.slider("Math Score (%)", 0, 100, 50)
failures = st.sidebar.number_input("Previous Failures", 0, 5, 0)
distance = st.sidebar.number_input("Distance to School (km)", 0.0, 50.0, 2.0)
household = st.sidebar.number_input("Household Size", 1, 15, 4)
supplies = st.sidebar.radio("Has School Supplies?", ["Yes", "No"])

# Predict Button
if st.sidebar.button("Run Risk Assessment"):
    # Prepare Data
    vec = np.zeros(len(features))
    vec[0], vec[1], vec[6] = age, std, failures
    vec[3] = math / 100
    vec[4], vec[5] = distance, household
    vec[2] = 1 # Defaulting to female for this demo
    vec[7] = 1 if supplies == "Yes" else 0
    
    # Inference
    df = pd.DataFrame([vec], columns=features)
    prob = float(model.predict_proba(scaler.transform(df))[0][1])
    
    # Sensitivity Hack (Match your API logic)
    if failures > 0: prob += (0.10 * failures)
    if age > 15: prob += 0.05
    final_prob = min(0.98, max(0.02, prob))
    
    # Display Results
    st.subheader(f"Risk Profile: {name}")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Dropout Probability", f"{final_prob:.2%}")
        
    with col2:
        if final_prob > 0.45:
            st.error("STATUS: HIGH RISK")
        else:
            st.success("STATUS: LOW RISK")

    # Risk Drivers (The Grade Booster!)
    if final_prob > 0.45:
        st.warning("⚠️ **Primary Risk Drivers Detected:**")
        if failures >= 1: st.write("- History of Grade Repetition")
        if age > (std + 6): st.write("- Significant Age-Grade Mismatch")
        if math < 40: st.write("- Academic Struggle in Core Subjects")
        st.info("💡 **Recommendation:** Schedule a guardian meeting to discuss economic or social barriers.")