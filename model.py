import streamlit as st
import pandas as pd
import joblib

# ==============================
# PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="Employee Performance Prediction",
    page_icon="",
    layout="centered",
)

# ==============================
# LOAD MODEL
# ==============================
model = joblib.load("best_random_forest_model.joblib")

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
.main {
    background-color: #F8F5F2;
}

.title {
    text-align:center;
    color:#2F243A;
    font-size:60px;
    font-weight:900;
}

.subtitle {
    text-align:center;
    color:#6D4C85;
    font-size:40px;
    font-weight:700;
}

.description {
    text-align:center;
    color:#4A4A4A;
    font-size:20px;
    margin-bottom: 28px;
}

.stButton>button {
    background-color:#2F243A;
    color:white;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:18px;
}

.result-box {
    padding:20px;
    border-radius:10px;
    text-align:center;
    font-size:25px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown(
    '<h1 style="text-align:center; color:#2F243A; font-size:120px; font-weight:900; margin-bottom: 12px;">Employee Performance Prediction System</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<h2 style="text-align:center; color:#6D4C85; font-size:80px; font-weight:700; margin-top: 0; margin-bottom: 12px;">INX Future Inc. - HR Analytics Dashboard</h2>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; color:#4A4A4A; font-size:54px; margin-bottom: 36px; line-height:1.2;">Use this dashboard to predict employee performance ratings and gain HR insights from employee and career attributes.</p>',
    unsafe_allow_html=True
)

st.divider()

# ==============================
# MAPPINGS
# ==============================

education_map = {
    "College": 0,
    "Bachelor": 1,
    "Master": 2,
    "Doctor": 3
}

environment_map = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Very High": 3
}

job_satisfaction_map = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Very High": 3
}

worklife_map = {
    "Bad": 0,
    "Good": 1,
    "Better": 2,
    "Best": 3
}

department_map = {
    "Sales": 0,
    "Development": 1,
    "Research & Development": 2,
    "Human Resources": 3,
    "Finance": 4,
    "Data Science": 5
}

job_role_map = {
    "Sales Executive": 0,
    "Developer": 1,
    "Manager": 2,
    "Research Scientist": 3,
    "HR": 4,
    "Finance Executive": 5,
    "Data Scientist": 6
}

# ==============================
# INPUT SECTION
# ==============================

st.subheader("Employee Information")

col1, col2 = st.columns(2)

with col1:

    department = st.selectbox(
        "Department",
        list(department_map.keys())
    )

    education = st.selectbox(
        "Education Level",
        ["College","Bachelor","Master","Doctor"]
    )

    environment = st.selectbox(
        "Environment Satisfaction",
        ["Low","Medium","High","Very High"]
    )

    job_satisfaction = st.selectbox(
        "Job Satisfaction",
        ["Low","Medium","High","Very High"]
    )

with col2:

    job_role = st.selectbox(
        "Job Role",
        list(job_role_map.keys())
    )

    worklife = st.selectbox(
        "Work Life Balance",
        ["Bad","Good","Better","Best"]
    )

    salary_hike = st.number_input(
        "Last Salary Hike (%)",
        min_value=0,
        max_value=30,
        value=15
    )

    job_level = st.selectbox(
        "Job Level",
        [1, 2, 3, 4, 5]
    )

# ==============================
# EXPERIENCE SECTION
# ==============================

st.subheader("Career Information")

c1, c2 = st.columns(2)

with c1:

    years_promotion = st.number_input(
        "Years Since Last Promotion",
        min_value=0,
        max_value=40,
        value=1
    )

    years_role = st.number_input(
        "Years in Current Role",
        min_value=0,
        max_value=40,
        value=3
    )

with c2:

    years_company = st.number_input(
        "Years at Current Company",
        min_value=0,
        max_value=40,
        value=5
    )

    years_manager = st.number_input(
        "Years with Current Manager",
        min_value=0,
        max_value=40,
        value=3
    )

    total_experience = st.number_input(
        "Total Work Experience (Years)",
        min_value=0,
        max_value=50,
        value=5
    )

    distance_from_home = st.number_input(
        "Distance from Home (km)",
        min_value=0,
        max_value=100,
        value=10
    )

st.divider()

# ==============================
# PREDICT BUTTON
# ==============================

if st.button("Predict Employee Performance"):

    # Create input dataframe
    input_data = pd.DataFrame({

        "EmpEnvironmentSatisfaction":[environment_map[environment]],
        "EmpLastSalaryHikePercent":[salary_hike],
        "YearsSinceLastPromotion":[years_promotion],
        "ExperienceYearsInCurrentRole":[years_role],
        "YearsWithCurrManager":[years_manager],
        "EmpWorkLifeBalance":[worklife_map[worklife]],
        "ExperienceYearsAtThisCompany":[years_company],
        "EmpJobLevel":[job_level],
        "TotalWorkExperienceInYears":[total_experience],
        "DistanceFromHome":[distance_from_home]
    })

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data).max()*100
    except:
        probability = None

    st.divider()

    if prediction == 0:

        st.error("Performance Rating: GOOD")

    elif prediction == 1:

        st.warning("Performance Rating: EXCELLENT")

    else:

        st.success("Performance Rating: OUTSTANDING")

    if probability:

        st.metric(
            label="Prediction Confidence",
            value=f"{probability:.2f}%"
        )

    st.subheader("Employee Summary")

    st.write(f"**Department:** {department}")
    st.write(f"**Job Role:** {job_role}")
    st.write(f"**Education:** {education}")
    st.write(f"**Environment Satisfaction:** {environment}")
    st.write(f"**Job Satisfaction:** {job_satisfaction}")
    st.write(f"**Work Life Balance:** {worklife}")