
import json
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def init_session_state():
    defaults = {
        "student_profile": {},
        "assessment_results": {},
        "recommendations": {},
        "chat_history": [],
        "demo_mode": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def load_careers():
    with open(DATA_DIR / "career_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def apply_theme():
    st.markdown("""
    <style>
    :root { --navy:#0b1736; --blue:#2563eb; --purple:#7c3aed; --ink:#16213e; --muted:#64748b; }
    .stApp {
        background:
          radial-gradient(circle at 15% 10%, rgba(124,58,237,.10), transparent 28%),
          radial-gradient(circle at 85% 5%, rgba(37,99,235,.10), transparent 25%),
          #f7f9fc;
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1736 0%, #111f45 100%);
    }
    [data-testid="stSidebar"] * { color: #eef4ff !important; }
    .hero {
        min-height: 430px; border-radius: 30px; margin-bottom: 28px;
        background:
          linear-gradient(90deg, rgba(7,18,45,.96), rgba(20,37,82,.80), rgba(67,38,116,.55)),
          radial-gradient(circle at 80% 30%, rgba(110,231,255,.28), transparent 25%),
          linear-gradient(135deg,#0b1736,#3b2a68);
        box-shadow: 0 25px 70px rgba(11,23,54,.20);
        overflow:hidden; display:flex; align-items:center;
    }
    .hero-overlay { padding: 60px; max-width: 820px; color:white; }
    .eyebrow { letter-spacing:3px; font-size:.78rem; font-weight:700; opacity:.75; }
    .hero h1 { font-size: clamp(3.4rem,8vw,6.5rem); margin:8px 0 0; line-height:.95; font-weight:900; }
    .hero h1 span { color:#9cc8ff; }
    .hero-title { font-size:1.55rem; font-weight:700; margin:18px 0 8px; }
    .hero-copy { font-size:1.02rem; line-height:1.75; max-width:720px; color:#dce7ff; }
    .feature-card, .career-card, .metric-card, .roadmap-card {
        background:rgba(255,255,255,.92); border:1px solid rgba(148,163,184,.18);
        border-radius:20px; padding:22px; box-shadow:0 12px 35px rgba(15,23,42,.07);
        height:100%;
    }
    .feature-icon { font-size:2rem; }
    .feature-card h3 { margin:8px 0 5px; color:var(--navy); }
    .feature-card p { color:var(--muted); line-height:1.6; }
    .metric-card h2 { margin:0; color:var(--navy); }
    .metric-label { color:var(--muted); font-size:.85rem; text-transform:uppercase; letter-spacing:1px; }
    .career-card { border-top:4px solid #2563eb; margin-bottom:18px; }
    .score { font-size:2rem; font-weight:800; color:#2563eb; }
    .pill { display:inline-block; background:#eef2ff; color:#4338ca; padding:5px 10px; border-radius:999px; margin:3px; font-size:.8rem; }
    .stButton > button { border-radius:12px; font-weight:700; }
    .small-muted { color:#64748b; font-size:.85rem; }
    .section-title { color:#0b1736; margin-top:20px; }
    </style>
    """, unsafe_allow_html=True)

def safe_text(value):
    if value is None:
        return ""
    return str(value).strip()

def score_pct(correct, total):
    return round((correct / total) * 100, 1) if total else 0.0
