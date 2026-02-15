# **LiftEd: A hybrid early warning system for student dropout prediction**

## Project Overview
LiftEd is a  machine learning powered decision tool used to predict adolescent dropout in Malawian Primary schools. The project addresses a critical challenge of student dropout in Malawian primary schools by identifying at-risk students before they leave education.  This project utilizes the Longitudinal Study of Schooling Quality and Experience in Malawi (MSAS) student dataset collected over 6 rounds.

Data Source: [Havard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi%3A10.7910%2FDVN%2FV4C81G&version=2.1) (Obtained with permission from the provider)

## key Features
* **Predictive Inference:** Utilizes a high-recall XGBoost model (Recall: 0.76) to minimize "False Negatives" (missing at-risk students).
* **Explainability Layer:** Unlike standard "Black Box" models, MSAS identifies specific risk drivers (e.g., Age-Grade mismatch, academic struggle) to help teachers understand the *why* behind a prediction.
* **Dual-Deployment Architecture:** * **FastAPI Backend:** A production-ready REST API for system integrations.
    * **Streamlit Frontend:** An intuitive, teacher-facing dashboard for manual risk assessment.
* **Data Validation:** Robust Pydantic schema validation to ensure data integrity at the point of entry.

## Tech Stack 
- **language:** Python 3.13
-**ML frameworks**: Scikit-learn, XGBoost
-**API framework**: FastAPI & Uvicorn
-**UI Framework**: Streamlit
-**Data Handling**: Pandas & Numpy
**Model Persistence**: Job lib
**Code Execution**: Google Collab for model training and VS Code for API execution

## Installation and setup 

1. **Clone the Repository:**
   ```
   git clone https://github.com/tamandakaunda-15/Capstone_Assignment2_2026
   cd Capstone_Assignment2_2026
   cd MSAS_Capstone
   ```
2. ** Install Dependencies
   ``` pip install -r requirements```

3. Run the API (FastAPI)
   ```uvicorn main: app --reload ```
Access the interactive docs at: (http://127.0.0.1:8000/docs)[http://127.0.0.1:8000/docs]

4. Run the dashboard Streamlit:

    ``` streamlit run streamlit_app.py```

## Model Performance
Primary model: XGBoost Classifer
Recall: 0.76(Optimized to ensure high sensitivity for intervention)
Feature Engineering: 63 features, including demographic, academic, and socio-economic indicators




