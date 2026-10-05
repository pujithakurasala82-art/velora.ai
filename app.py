
import streamlit as st
from backend.utils import apply_theme, init_session_state

st.set_page_config(
    page_title="VEYLORA AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_session_state()

st.markdown("""
<div class="hero">
  <div class="hero-overlay">
    <div class="eyebrow">AI-POWERED CAREER GUIDANCE</div>
    <h1>VEYLORA <span>AI</span></h1>
    <p class="hero-title">Discover Your Strengths. Explore Your Future.</p>
    <p class="hero-copy">
      A personalized career guidance platform that combines structured assessments
      with Google Gemini to help students explore multiple career pathways,
      understand skill gaps, and build practical learning roadmaps.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 01 · Build your profile")
    st.write("Tell VEYLORA AI about your education, interests, skills and goals.")
with c2:
    st.markdown("### 02 · Take assessments")
    st.write("Complete interest, aptitude, technical and work-style assessments.")
with c3:
    st.markdown("### 03 · Explore your future")
    st.write("Get multiple AI-assisted career paths, skill gaps and learning roadmaps.")

st.markdown("## Why VEYLORA AI?")
a, b, c, d = st.columns(4)
cards = [
    ("🧠", "Holistic analysis", "Combines several assessment dimensions instead of relying on one score."),
    ("🧭", "Multiple pathways", "Explore a ranked set of career options rather than a single answer."),
    ("📈", "Skill-gap insights", "See what you already demonstrate and what you can develop next."),
    ("💬", "AI counselor", "Ask follow-up questions using your profile and assessment context."),
]
for col, (icon, title, body) in zip((a,b,c,d), cards):
    with col:
        st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

st.markdown("## Start your journey")
if st.button("✨ Start Assessment", type="primary", use_container_width=True):
    st.switch_page("pages/1_Profile.py")

st.info("Career recommendations are AI-assisted guidance, not guarantees or psychological diagnoses. Use them as one input when making education and career decisions.")
