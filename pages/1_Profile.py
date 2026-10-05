
import streamlit as st
from backend.utils import apply_theme, init_session_state
from backend.database import save_student

apply_theme()
init_session_state()

st.title("Student Profile")
st.caption("Your information is used to personalize career guidance.")

with st.form("profile_form"):
    name = st.text_input("Full name *")
    age = st.number_input("Age", min_value=13, max_value=100, value=18)
    education = st.selectbox("Education level", ["School", "Diploma", "Undergraduate", "Postgraduate"])
    degree = st.text_input("Degree / Program", placeholder="B.Tech")
    branch = st.text_input("Branch / Specialization", placeholder="CSE, EDS, ECE...")
    year = st.selectbox("Current year", ["1st Year","2nd Year","3rd Year","4th Year","Completed"])
    cgpa = st.number_input("CGPA / Percentage", min_value=0.0, max_value=100.0, value=8.0, step=0.1)
    subjects = st.text_input("Favorite / strong subjects", placeholder="Math, Python, Networks")
    difficult = st.text_input("Subjects you find difficult", placeholder="Keep this optional")
    skills = st.text_area("Technical skills", placeholder="Python, Linux, SQL...")
    programming = st.text_input("Programming languages", placeholder="Python, Java...")
    certifications = st.text_input("Certifications", placeholder="Optional")
    hobbies = st.text_input("Hobbies", placeholder="Reading, coding, design...")
    interests = st.multiselect(
        "Career interests",
        ["Technology","Cybersecurity","Data","Artificial Intelligence","Software Development",
         "Cloud","Networking","Design","Business","Finance","Research","Communication","Management",
         "Entrepreneurship","Education","Engineering"]
    )
    environment = st.selectbox("Preferred work environment", ["Individual focus","Team-based","Mixed","Not sure"])
    goals = st.text_area("Career goals", placeholder="What would you like to achieve?")
    location = st.text_input("Preferred location", placeholder="Optional")
    higher_studies = st.selectbox("Interested in higher studies?", ["Yes","No","Not sure"])
    confusion = st.text_area("What are you currently confused about?")

    submitted = st.form_submit_button("Save Profile & Continue", type="primary", use_container_width=True)

if submitted:
    if not name.strip():
        st.error("Please enter your name.")
    else:
        profile = {
            "name": name.strip(), "age": age, "education": education, "degree": degree,
            "branch": branch, "year": year, "cgpa": cgpa, "subjects": subjects,
            "difficult_subjects": difficult, "skills": skills, "programming": programming,
            "certifications": certifications, "hobbies": hobbies, "interests": interests,
            "environment": environment, "goals": goals, "preferred_location": location,
            "higher_studies": higher_studies, "career_confusion": confusion,
        }
        st.session_state.student_profile = profile
        st.session_state.student_id = save_student(profile)
        st.success("Profile saved.")
        st.switch_page("pages/2_Assessments.py")
