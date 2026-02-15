import streamlit as st
import requests  
import json

# Page Config
st.set_page_config(page_title="MSAS Dashboard", page_icon="🎓")

# path to the LIVE API URL
API_URL = "https://capstone-assignment2-2026.onrender.com/predict"

st.title("🎓 LiftEd Malawi: Early Warning System")
st.markdown("### Identifying Student Dropout Risk in Malawi")
#st.info("Connected to Live Cloud API: Render")
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
    # 1. Prepare Payload for API
    payload = {
        "name": name,
        "age": age,
        "current_standard": std,
        "gender_is_female": 1, 
        "math_score_percent": float(math),
        "distance_to_school_km": float(distance),
        "household_size": int(household),
        "previous_failures": int(failures),
        "has_school_supplies": 1 if supplies == "Yes" else 0
    }

    try:
        # 2. Call the Render API
        with st.spinner('Querying Cloud Model...'):
            response = requests.post(API_URL, json=payload)
            data = response.json()

        if response.status_code == 200:
            # 3. Extract results from the API response
            res = data["risk_assessment"]
            expl = data["explainability"]
            
            st.subheader(f"Risk Profile: {data['student_metadata']['name']}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Probability", res["probability"])
            col2.metric("Status", res["status"])
            col3.metric("Priority", res["priority"])

            # 4. Display Explainability
            if res["status"] == "HIGH RISK":
                st.warning("⚠️ **Primary Risk Drivers Detected:**")
                for driver in expl["primary_risk_drivers"]:
                    st.write(f"- {driver}")
                st.info(f"💡 **Recommendation:** {expl['intervention_hint']}")
            else:
                st.success(" Student is currently stable. Maintain routine monitoring.")
        else:
            st.error(f"API Error: {data.get('detail', 'Unknown error')}")

    except Exception as e:
        st.error(f"Could not connect to API: {e}")