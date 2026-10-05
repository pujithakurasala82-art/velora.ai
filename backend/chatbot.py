
from backend.gemini_service import counselor_reply

def ask(context, question, history):
    return counselor_reply(context, question, history)
