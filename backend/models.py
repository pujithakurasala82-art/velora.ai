
from pydantic import BaseModel, Field
from typing import List

class CareerRecommendation(BaseModel):
    career: str
    compatibility_score: int = Field(ge=0, le=100)
    why_suitable: str
    required_skills: List[str]
    student_strengths: List[str]
    skill_gaps: List[str]
    learning_roadmap: List[str]
    future_opportunities: List[str]
    alternative_roles: List[str]

class StudentProfileAI(BaseModel):
    learning_style: str
    primary_strengths: List[str]
    development_areas: List[str]

class CareerAnalysis(BaseModel):
    career_summary: str
    student_profile: StudentProfileAI
    career_recommendations: List[CareerRecommendation]
    recommended_next_steps: List[str]
    general_guidance: str
