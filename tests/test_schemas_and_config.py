import pytest
from backend.config import settings, ScoringWeights
from backend.schemas.resume import (
    ResumeParsedData,
    SkillItem,
    ExperienceItem,
    EducationItem,
    ProjectItem,
)
from backend.schemas.job import JobDescriptionCreate, JobDescriptionParsed, WeightConfig
from backend.schemas.match import (
    CandidateMatchResult,
    ComponentScore,
    SkillMatchEvidence,
    ScreeningResponse,
)


def test_scoring_weights_validation():
    weights = ScoringWeights(
        required_skills=0.40,
        preferred_skills=0.15,
        semantic_similarity=0.25,
        experience=0.15,
        projects=0.05,
    )
    assert weights.validate_weights() is True

    invalid_weights = ScoringWeights(
        required_skills=0.50,
        preferred_skills=0.50,
        semantic_similarity=0.20,
        experience=0.10,
        projects=0.10,
    )
    assert invalid_weights.validate_weights() is False


def test_resume_schema_instantiation():
    resume = ResumeParsedData(
        resume_id="res-101",
        filename="alice_ml_resume.pdf",
        file_type="pdf",
        candidate_name="Alice Chen",
        skills=[
            SkillItem(canonical_name="Python", raw_name="Python 3.11", category="Programming Languages"),
            SkillItem(canonical_name="PyTorch", raw_name="PyTorch", category="Machine Learning"),
        ],
        total_experience_years=4.5,
        experience=[
            ExperienceItem(
                role="Machine Learning Engineer",
                company="TechCorp",
                duration_years=4.5,
                description="Built recommendation engines using PyTorch and scikit-learn.",
                matched_skills=["Python", "PyTorch", "scikit-learn"],
            )
        ],
        projects=[
            ProjectItem(
                title="Talent Search Engine",
                technologies=["FastAPI", "SentenceTransformers"],
            )
        ],
    )
    assert resume.candidate_name == "Alice Chen"
    assert len(resume.skills) == 2
    assert resume.total_experience_years == 4.5


def test_job_schema_instantiation():
    job = JobDescriptionParsed(
        job_id="job-202",
        title="Senior NLP Engineer",
        company="HCLTech Enterprise",
        raw_text="Looking for an NLP Engineer with Python and PyTorch skills.",
        required_skills=["Python", "PyTorch"],
        preferred_skills=["FastAPI", "Docker"],
        min_experience_years=3.0,
    )
    assert job.title == "Senior NLP Engineer"
    assert "Python" in job.required_skills
    assert job.weights.required_skills == 0.40


def test_match_result_schema():
    match = CandidateMatchResult(
        candidate_id="cand-001",
        candidate_name="Alice Chen",
        resume_id="res-101",
        job_id="job-202",
        overall_score=87.5,
        score_breakdown=[
            ComponentScore(
                name="Required Skills",
                raw_score=1.0,
                weight=0.40,
                weighted_score=0.40,
                explanation="Matched 2/2 required skills: Python, PyTorch",
                evidence=["Proficient in Python 3.11", "Trained models in PyTorch"],
            )
        ],
        matched_required_skills=["Python", "PyTorch"],
        missing_required_skills=[],
        explanation_summary="Strong match with full required skill coverage.",
        recommendation_tier="Strong Match",
    )
    assert match.overall_score == 87.5
    assert match.recommendation_tier == "Strong Match"
