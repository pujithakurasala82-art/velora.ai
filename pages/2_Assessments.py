
import streamlit as st
import random
from backend.utils import apply_theme, init_session_state
from backend.assessment_engine import (
    INTEREST_QUESTIONS, APTITUDE_QUESTIONS, WORKSTYLE_QUESTIONS,
    grade_mcq, grade_interest, grade_workstyle
)
from backend.database import save_assessment

apply_theme()
init_session_state()

if not st.session_state.student_profile:
    st.warning("Please complete your profile first.")
    st.switch_page("pages/1_Profile.py")

st.title("Assessments")
st.caption("Complete all sections. Your results will be combined for holistic analysis.")

tab1, tab2, tab3, tab4 = st.tabs(["Interest", "Aptitude", "Technical", "Work & Learning Style"])

with tab1:
    st.subheader("Interest Assessment")
    interest_answers = []
    for i, (q, options, _) in enumerate(INTEREST_QUESTIONS):
        choice = st.radio(q, options, key=f"interest_{i}", index=None)
        interest_answers.append(options.index(choice) if choice else None)
    if st.button("Save Interest Assessment"):
        if any(x is None for x in interest_answers):
            st.error("Please answer every interest question.")
        else:
            scores = grade_interest(interest_answers)
            st.session_state.assessment_results["interest"] = scores
            st.success("Interest assessment saved.")

with tab2:
    st.subheader("Aptitude Assessment")
    aptitude_answers = {}
    for i, q in enumerate(APTITUDE_QUESTIONS):
        choice = st.radio(q["q"], q["options"], key=f"apt_{i}", index=None)
        aptitude_answers[str(i)] = q["options"].index(choice) if choice else None
    if st.button("Save Aptitude Assessment"):
        if any(v is None for v in aptitude_answers.values()):
            st.error("Please answer every aptitude question.")
        else:
            result = grade_mcq(APTITUDE_QUESTIONS, aptitude_answers)
            st.session_state.assessment_results["aptitude"] = result
            if "student_id" in st.session_state:
                save_assessment(st.session_state.student_id, "aptitude", result["correct"], result["total"], aptitude_answers)
            st.success("Aptitude assessment saved.")

with tab3:
    st.subheader("Technical Skills Assessment")
    interests = st.session_state.student_profile.get("interests", [])
    tech_questions = [
        ("Which protocol translates domain names to IP addresses?", ["DNS","HTTP","SSH","FTP"], 0, "Networking"),
        ("Which Linux command lists files?", ["cd","ls","pwd","mkdir"], 1, "Linux"),
        ("What does MFA add to authentication?", ["A second verification factor","Faster login","A backup server","Encryption only"], 0, "Security"),
        ("Which SQL keyword retrieves rows?", ["SELECT","PUSH","FETCHALL","OPEN"], 0, "Databases"),
        ("What is a firewall primarily used for?", ["Filtering network traffic","Editing images","Compiling code","Creating databases"], 0, "Security"),
        ("Which is commonly used for Python package installation?", ["pip","git","ssh","grep"], 0, "Programming"),
        ("What does HTTP primarily support?", ["Web communication","Disk formatting","CPU scheduling","Password hashing"], 0, "Web"),
        ("Which concept separates a cloud network into smaller logical networks?", ["Virtual networking","Compression","Rendering","Caching"], 0, "Cloud"),
    ]
    if "Cybersecurity" in interests:
        st.info("Cybersecurity-focused questions are included because it is one of your selected interests.")
    technical_answers = {}
    for i, (q, options, answer, category) in enumerate(tech_questions):
        choice = st.radio(q, options, key=f"tech_{i}", index=None)
        technical_answers[str(i)] = {"selected": options.index(choice) if choice else None, "answer": answer, "category": category}
    if st.button("Save Technical Assessment"):
        if any(v["selected"] is None for v in technical_answers.values()):
            st.error("Please answer every technical question.")
        else:
            correct = sum(v["selected"] == v["answer"] for v in technical_answers.values())
            result = {"correct": correct, "total": len(technical_answers), "percentage": round(correct/len(technical_answers)*100,1)}
            st.session_state.assessment_results["technical"] = result
            if "student_id" in st.session_state:
                save_assessment(st.session_state.student_id, "technical", correct, len(technical_answers), technical_answers)
            st.success("Technical assessment saved.")

with tab4:
    st.subheader("Work & Learning Style Profile")
    work_answers = []
    for i, (q, options, _) in enumerate(WORKSTYLE_QUESTIONS):
        choice = st.radio(q, options, key=f"work_{i}", index=None)
        work_answers.append(options.index(choice) if choice else None)
    if st.button("Save Work-Style Assessment"):
        if any(x is None for x in work_answers):
            st.error("Please answer every work-style question.")
        else:
            result = grade_workstyle(work_answers)
            st.session_state.assessment_results["workstyle"] = result
            st.success("Work-style profile saved.")

st.divider()
if all(k in st.session_state.assessment_results for k in ["interest","aptitude","technical","workstyle"]):
    st.success("All assessments completed. Continue to Results.")
    if st.button("View Results", type="primary"):
        st.switch_page("pages/3_Results.py")
else:
    missing = [k for k in ["interest","aptitude","technical","workstyle"] if k not in st.session_state.assessment_results]
    st.warning("Still to complete: " + ", ".join(missing))
