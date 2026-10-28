from typing import List, Dict
from ..schemas.resume import ResumeParsedData
from ..schemas.recommendation import RoleRecommendation

# Predefined standard role skill profiles for career trajectory recommendations
TARGET_ROLE_PROFILES: Dict[str, Dict] = {
    "Machine Learning Engineer": {
        "core_skills": ["Python", "PyTorch", "scikit-learn", "Docker", "SQL"],
        "bonus_skills": ["MLOps", "Transformers", "Kubernetes", "AWS"],
        "description": "Designs, builds, and deploys predictive statistical models and machine learning pipelines."
    },
    "NLP / LLM Research Engineer": {
        "core_skills": ["Python", "Transformers", "Natural Language Processing", "PyTorch", "Large Language Models"],
        "bonus_skills": ["Deep Learning", "Docker", "FastAPI"],
        "description": "Specializes in language representation, vector search, LLM fine-tuning, and retrieval augmented generation."
    },
    "Backend Cloud Engineer": {
        "core_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs"],
        "bonus_skills": ["AWS", "Kubernetes", "Redis", "CI/CD"],
        "description": "Architects resilient microservices, high-throughput database interactions, and secure cloud endpoints."
    },
    "Data Scientist": {
        "core_skills": ["Python", "Pandas", "NumPy", "SQL", "scikit-learn"],
        "bonus_skills": ["R", "Deep Learning", "Apache Spark"],
        "description": "Derives statistical business insights, hypothesizes predictive features, and presents data storytelling."
    },
    "MLOps & Platform Engineer": {
        "core_skills": ["Docker", "Kubernetes", "MLOps", "CI/CD", "Linux", "Python"],
        "bonus_skills": ["AWS", "Azure", "Google Cloud", "Apache Kafka"],
        "description": "Automates continuous model delivery, container orchestration, feature stores, and drift monitoring."
    },
    "Full-Stack AI Developer": {
        "core_skills": ["Python", "FastAPI", "React", "TypeScript", "PostgreSQL"],
        "bonus_skills": ["Docker", "Node.js", "Large Language Models"],
        "description": "Bridges machine learning APIs with modern responsive web interfaces and cloud databases."
    },
}


def recommend_roles_for_candidate(resume: ResumeParsedData) -> List[RoleRecommendation]:
    """
    Analyzes candidate's extracted skills and projects to recommend
    aligned career roles and identify specific upskilling gaps.
    """
    candidate_skills = {s.canonical_name.lower(): s.canonical_name for s in resume.skills}
    recommendations = []

    for role_title, profile in TARGET_ROLE_PROFILES.items():
        core = profile["core_skills"]
        bonus = profile["bonus_skills"]

        core_matches = [s for s in core if s.lower() in candidate_skills]
        bonus_matches = [s for s in bonus if s.lower() in candidate_skills]
        missing_core = [s for s in core if s.lower() not in candidate_skills]

        # Scoring: 70% weight on core, 30% on bonus
        core_ratio = len(core_matches) / max(1, len(core))
        bonus_ratio = len(bonus_matches) / max(1, len(bonus))
        match_score = round((core_ratio * 70.0) + (bonus_ratio * 30.0), 1)

        justification = (
            f"You possess {len(core_matches)} of {len(core)} core competencies ({', '.join(core_matches) or 'None yet'}). "
            f"Acquiring {', '.join(missing_core[:3]) or 'further advanced tools'} will bring you to 100% readiness for this position."
        )

        recommendations.append(
            RoleRecommendation(
                role_title=role_title,
                match_percentage=match_score,
                overlapping_skills=core_matches + bonus_matches,
                recommended_growth_skills=missing_core,
                justification=justification,
            )
        )

    # Sort descending by match percentage
    recommendations.sort(key=lambda r: r.match_percentage, reverse=True)
    return recommendations
