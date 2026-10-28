from typing import List, Dict
from ..schemas.resume import ResumeParsedData
from ..schemas.job import JobDescriptionParsed
from ..ml.scorer import calculate_candidate_match


def recommend_jobs_for_candidate(
    resume: ResumeParsedData,
    open_jobs: List[JobDescriptionParsed],
    top_k: int = 5
) -> List[Dict]:
    """
    Ranks open job opportunities for a candidate using content-based
    multi-attribute utility matching.
    """
    matches = []
    for job in open_jobs:
        result = calculate_candidate_match(resume, job)
        matches.append({
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "department": job.department,
            "match_score": result.overall_score,
            "tier": result.recommendation_tier,
            "matched_skills": result.matched_required_skills,
            "missing_skills": result.missing_required_skills,
            "explanation": result.explanation_summary,
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches[:top_k]


def recommend_candidates_for_job(
    job: JobDescriptionParsed,
    resumes: List[ResumeParsedData],
    top_k: int = 10
) -> List[Dict]:
    """
    Ranks candidates for a given job description using content-based scoring.
    """
    results = []
    for resume in resumes:
        match_res = calculate_candidate_match(resume, job)
        results.append({
            "candidate_id": match_res.candidate_id,
            "candidate_name": match_res.candidate_name,
            "resume_id": resume.resume_id,
            "match_score": match_res.overall_score,
            "tier": match_res.recommendation_tier,
            "matched_required": match_res.matched_required_skills,
            "missing_required": match_res.missing_required_skills,
            "experience_years": resume.total_experience_years,
            "explanation": match_res.explanation_summary,
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:top_k]
