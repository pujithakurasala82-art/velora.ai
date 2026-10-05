
import streamlit as st
from backend.utils import apply_theme, init_session_state
apply_theme()
init_session_state()

st.title("About VEYLORA AI")
st.markdown("""
### What is VEYLORA AI?

VEYLORA AI is a student-focused career exploration platform that combines
structured assessments, deterministic Python scoring and Generative AI analysis.

### Technology stack

- Streamlit — frontend
- Python — application and scoring backend
- Google Gemini — generative career analysis and counselor
- SQLite — local data storage
- Plotly — visual analytics
- Pydantic — structured AI output validation

### Responsible use

Career recommendations are AI-assisted suggestions based on the information and
assessment results provided. They should be used as one input when making
educational and career decisions.
""")
