
import streamlit as st
import pandas as pd
from backend.utils import apply_theme, init_session_state

apply_theme()
init_session_state()

st.title("Career Comparison")
items = st.session_state.recommendations.get("career_recommendations", [])
if not items:
    st.warning("Generate recommendations first.")
    st.switch_page("pages/3_Results.py")

rows = []
for i, x in enumerate(items[:5]):
    rows.append({
        "Career": x.get("career",""),
        "Compatibility": f'{x.get("compatibility_score",0)}%',
        "Current Skills": "Strong" if i < 2 else "Developing",
        "Skill Gap": "Low" if i == 0 else "Medium",
        "Recommended": "⭐" if i < 2 else ""
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
st.info("The comparison is intended to help exploration; it does not determine which career you must choose.")

if st.button("Open Learning Roadmap", type="primary"):
    st.switch_page("pages/6_Learning_Roadmap.py")
