
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from backend.models import CareerAnalysis

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """
You are VEYLORA AI, an expert educational career guidance assistant.
Analyze the student's supplied profile and assessment results holistically.
Recommend approximately five career pathways that appear compatible with the
student's current interests, demonstrated skills and assessment performance.

Rules:
- Recommendations are guidance, never guarantees.
- Do not use gender, ethnicity, religion, disability, socioeconomic status, or
  other protected/sensitive traits to determine suitability.
- Do not diagnose personality or mental health conditions.
- Do not invent test scores or labor-market statistics.
- Explain recommendations using only supplied evidence plus general career knowledge.
- Consider multiple pathways and rank them.
- Suggest realistic skill gaps and learning steps.
- Return only data matching the requested structured schema.
"""

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def analyze_student(context):
    client = get_client()
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = SYSTEM_PROMPT + "\n\nStudent data:\n" + json.dumps(context, ensure_ascii=False, indent=2)
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CareerAnalysis,
            temperature=0.4,
        ),
    )
    if getattr(response, "parsed", None):
        return response.parsed.model_dump()
    return CareerAnalysis.model_validate_json(response.text).model_dump()

def counselor_reply(context, question, history):
    client = get_client()
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    compact = {
        "student": context.get("profile", {}),
        "assessment_results": context.get("results", {}),
        "recommendations": context.get("recommendations", {}),
    }
    prompt = f"""
You are the VEYLORA AI career counselor.
Use the student's context below to answer the current question.
Be concise, encouraging and practical. Do not make deterministic claims.
If the question asks for a plan, provide clear steps.

STUDENT CONTEXT:
{json.dumps(compact, ensure_ascii=False, indent=2)}

RECENT CHAT:
{json.dumps(history[-6:], ensure_ascii=False)}

QUESTION:
{question}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.5),
    )
    return response.text
