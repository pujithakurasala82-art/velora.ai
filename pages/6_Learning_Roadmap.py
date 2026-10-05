
import streamlit as st
from backend.utils import apply_theme, init_session_state

apply_theme()
init_session_state()

st.title("Personalized Learning Roadmap")
items = st.session_state.recommendations.get("career_recommendations", [])
if not items:
    st.warning("Generate recommendations first.")
    st.switch_page("pages/3_Results.py")

career_names = [x.get("career","") for x in items]
selected = st.selectbox("Choose a career path", career_names)
item = next(x for x in items if x.get("career") == selected)

st.markdown(f"## {selected}")
for i, step in enumerate(item.get("learning_roadmap", []), start=1):
    st.markdown(f"""
    <div class="roadmap-card">
      <div class="small-muted">STEP {i}</div>
      <h3>{step}</h3>
      <p>Build this capability through focused study, practice and a small project.</p>
    </div>
    """, unsafe_allow_html=True)
    if i < len(item.get("learning_roadmap", [])):
        st.markdown("↓")
