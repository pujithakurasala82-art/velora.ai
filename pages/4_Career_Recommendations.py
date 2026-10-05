
import streamlit as st
from backend.utils import apply_theme, init_session_state

apply_theme()
init_session_state()

st.title("Career Recommendations")
analysis = st.session_state.recommendations

if not analysis:
    st.warning("Please generate your AI analysis on the Results page first.")
    st.switch_page("pages/3_Results.py")

st.caption("These are AI-assisted compatibility indicators, not guarantees.")
for idx, item in enumerate(analysis.get("career_recommendations", [])[:5], start=1):
    st.markdown(f"""
    <div class="career-card">
      <div style="display:flex;justify-content:space-between;gap:20px;align-items:center;">
        <div><span class="small-muted">PATH {idx}</span><h2>{item.get("career","Career")}</h2></div>
        <div class="score">{item.get("compatibility_score",0)}%</div>
      </div>
      <p><b>Why this path?</b> {item.get("why_suitable","")}</p>
    </div>
    """, unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("**Your strengths**")
        for x in item.get("student_strengths",[]): st.write("•", x)
    with c2:
        st.markdown("**Skills to develop**")
        for x in item.get("skill_gaps",[]): st.write("•", x)
    with c3:
        st.markdown("**Core skills**")
        for x in item.get("required_skills",[]): st.write("•", x)
    with st.expander("View roadmap and opportunities"):
        st.markdown("**Learning roadmap**")
        for step in item.get("learning_roadmap",[]): st.write("→", step)
        st.markdown("**Future opportunities**")
        for role in item.get("future_opportunities",[]): st.write("•", role)
        st.markdown("**Alternative roles**")
        for role in item.get("alternative_roles",[]): st.write("•", role)
    st.divider()

if st.button("Compare Careers", type="primary"):
    st.switch_page("pages/5_Career_Comparison.py")
