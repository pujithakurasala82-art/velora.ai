
import streamlit as st
import plotly.graph_objects as go
from backend.utils import apply_theme, init_session_state
from backend.career_engine import deterministic_profile, fallback_recommendations
from backend.gemini_service import analyze_student
from backend.database import save_recommendations

apply_theme()
init_session_state()

st.title("Assessment Results")
results = st.session_state.assessment_results
profile = st.session_state.student_profile

required = ["interest","aptitude","technical","workstyle"]
if not all(k in results for k in required):
    st.warning("Please complete all assessments first.")
    st.switch_page("pages/2_Assessments.py")

apt = results["aptitude"]
tech = results["technical"]
interest = results["interest"]
work = results["workstyle"]

metrics = {
    "Aptitude": apt.get("percentage",0),
    "Technical": tech.get("percentage",0),
    "Cybersecurity Interest": interest.get("Cybersecurity",0),
    "Data Interest": interest.get("Data",0),
    "Software Interest": interest.get("Software",0),
    "Problem Solving": work.get("ProblemSolving",0),
    "Analytical": work.get("Analytical",0),
    "Adaptability": work.get("Adaptability",0),
}

cols = st.columns(4)
for col, (label, value) in zip(cols, list(metrics.items())[:4]):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><h2>{value:.0f}%</h2></div>', unsafe_allow_html=True)

st.subheader("Career Profile")
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=list(metrics.values()), theta=list(metrics.keys()), fill="toself", name="Profile"
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,100])),
    height=450, margin=dict(l=40,r=40,t=40,b=40)
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("AI Career Analysis")
st.caption("Compatibility scores are AI-assisted guidance indicators, not guarantees.")

context = deterministic_profile(profile, results)

if st.button("✨ Analyze with Gemini", type="primary"):
    with st.spinner("VEYLORA AI is analyzing your profile..."):
        try:
            analysis = analyze_student(context)
            st.session_state.recommendations = analysis
            if "student_id" in st.session_state:
                save_recommendations(st.session_state.student_id, analysis.get("career_recommendations", []))
            st.success("AI analysis complete.")
        except Exception as exc:
            st.warning("Gemini analysis was unavailable, so VEYLORA AI created a local fallback analysis for this demo.")
            st.session_state.recommendations = fallback_recommendations(profile, results)

if st.session_state.recommendations:
    analysis = st.session_state.recommendations
    st.markdown(f"### Profile Summary\n{analysis.get('career_summary','')}")
    strengths = analysis.get("student_profile", {}).get("primary_strengths", [])
    areas = analysis.get("student_profile", {}).get("development_areas", [])
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### Your strengths")
        for x in strengths: st.write("•", x)
    with c2:
        st.markdown("#### Development areas")
        for x in areas: st.write("•", x)
    if st.button("Explore Career Recommendations", type="primary"):
        st.switch_page("pages/4_Career_Recommendations.py")
