
import streamlit as st
from backend.utils import apply_theme, init_session_state
from backend.chatbot import ask

apply_theme()
init_session_state()

st.title("AI Career Counselor")
st.caption("Ask questions about your assessment profile, career options and learning plan.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask VEYLORA AI a career question...")
if question:
    st.session_state.chat_history.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)

    context = {
        "profile": st.session_state.student_profile,
        "results": st.session_state.assessment_results,
        "recommendations": st.session_state.recommendations,
    }
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask(context, question, st.session_state.chat_history)
            st.markdown(answer)
        st.session_state.chat_history.append({"role":"assistant","content":answer})
    except Exception:
        fallback = (
            "The Gemini counselor is unavailable right now. "
            "Please check GEMINI_API_KEY and your internet connection. "
            "You can still use the assessment and local demo features."
        )
        with st.chat_message("assistant"):
            st.warning(fallback)
        st.session_state.chat_history.append({"role":"assistant","content":fallback})
