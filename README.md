
# VEYLORA AI

**Discover Your Strengths. Explore Your Future.**

VEYLORA AI is a Streamlit + Python + Google Gemini career guidance application for students.

## Features

- Student profile
- Interest assessment
- Aptitude assessment
- Technical assessment
- Work & learning style profile
- Plotly performance dashboard
- Gemini-powered structured career analysis
- Top five career pathways
- Skill-gap analysis
- Career comparison
- Personalized learning roadmap
- AI Career Counselor
- SQLite storage
- Local fallback/demo mode when Gemini is unavailable
- Custom professional UI

## Architecture

Student -> Streamlit -> Python assessment engine -> Gemini AI -> recommendations -> roadmap -> counselor

Python handles deterministic assessment scoring. Gemini handles personalized reasoning, explanations and roadmap generation.

## Installation

Use Python 3.11+.

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Run:

```bash
streamlit run app.py
```

Then open the local Streamlit URL.

## Images

The application works without image files by using a premium gradient hero background. To add photography, place files in `assets/` and extend the hero CSS in `backend/utils.py`.

Use properly licensed images if you add external photography.

## Demo/fallback mode

If `GEMINI_API_KEY` is missing or the API call fails, the Results page creates a local fallback analysis so the core hackathon demo can still run. The fallback is clearly presented as a demo/local analysis.

## Security

Never commit `.env` or API keys. `.gitignore` already excludes `.env`.

## Gemini API

This project uses the official `google-genai` SDK and structured output through Pydantic. The model can be changed with `GEMINI_MODEL` in `.env`.
