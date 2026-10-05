
from backend.utils import load_careers

def deterministic_profile(profile, results):
    aptitude = results.get("aptitude", {})
    interest = results.get("interest", {})
    workstyle = results.get("workstyle", {})
    technical = results.get("technical", {})
    return {
        "profile": profile,
        "aptitude": aptitude,
        "interest": interest,
        "workstyle": workstyle,
        "technical": technical,
    }

def fallback_recommendations(profile, results):
    interests = results.get("interest", {})
    aptitude = results.get("aptitude", {}).get("percentage", 0)
    technical = results.get("technical", {}).get("percentage", 0)
    logical = results.get("aptitude", {}).get("categories", {}).get("Logical", 0)
    quantitative = results.get("aptitude", {}).get("categories", {}).get("Quantitative", 0)

    scores = {
        "Cybersecurity Analyst": 55 + interests.get("Cybersecurity",0)*.25 + logical*.12 + technical*.10,
        "Data Analyst": 55 + interests.get("Data",0)*.25 + quantitative*.12 + aptitude*.08,
        "Software Developer": 55 + interests.get("Software",0)*.25 + logical*.10 + technical*.10,
        "Cloud / Network Engineer": 50 + interests.get("Cybersecurity",0)*.18 + technical*.12 + logical*.08,
        "AI / ML Engineer": 48 + interests.get("Data",0)*.18 + quantitative*.12 + technical*.10,
    }
    ranked = sorted(scores.items(), key=lambda x:x[1], reverse=True)[:5]
    data = load_careers()
    output = []
    for career, score in ranked:
        base = next((x for x in data if x["career"] == career), data[0])
        output.append({
            "career": career,
            "compatibility_score": int(max(50, min(97, round(score)))),
            "why_suitable": base["why_suitable"],
            "required_skills": base["required_skills"],
            "student_strengths": ["Assessment participation", "Problem-solving mindset"],
            "skill_gaps": base["skill_gaps"],
            "learning_roadmap": base["learning_roadmap"],
            "future_opportunities": base["future_opportunities"],
            "alternative_roles": base["alternative_roles"],
        })
    return {
        "career_summary": "Demo/fallback analysis based on assessment scores and declared interests.",
        "student_profile": {
            "learning_style": "Practical and exploratory",
            "primary_strengths": ["Problem solving", "Curiosity"],
            "development_areas": ["Communication", "Hands-on practice"],
        },
        "career_recommendations": output,
        "recommended_next_steps": ["Review your top three pathways", "Choose one skill to build this month", "Complete a small project"],
        "general_guidance": "Use these recommendations as guidance rather than a guaranteed prediction.",
    }
