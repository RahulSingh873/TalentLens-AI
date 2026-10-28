from typing import List, Tuple
from ..schemas.resume import ResumeParsedData
from ..schemas.job import JobDescriptionParsed, WeightConfig
from ..schemas.match import (
    CandidateMatchResult,
    ComponentScore,
    SkillMatchEvidence,
)
from ..nlp.matcher import match_skills_against_requirements
from ..nlp.embeddings import embedding_engine


def calculate_candidate_match(
    resume: ResumeParsedData,
    job: JobDescriptionParsed,
    custom_weights: WeightConfig = None
) -> CandidateMatchResult:
    """
    Computes explainable, multi-criteria match score between candidate and job posting.
    """
    weights = custom_weights or job.weights or WeightConfig()

    # 1. Skill Matching
    (
        matched_req,
        missing_req,
        matched_pref,
        missing_pref,
        skill_evidences,
    ) = match_skills_against_requirements(resume, job.required_skills, job.preferred_skills)

    # phi_1: Required skills coverage
    total_req_count = len(job.required_skills)
    if total_req_count > 0:
        raw_req_score = len(matched_req) / total_req_count
        req_explanation = f"Matched {len(matched_req)} of {total_req_count} required skills ({round(raw_req_score * 100, 1)}%)"
    else:
        raw_req_score = 1.0
        req_explanation = "No mandatory skills specified in job criteria."

    req_evidence = [
        f"{ev.skill}: {ev.source_snippet}"
        for ev in skill_evidences
        if ev.is_required and ev.status == "matched"
    ]

    # phi_2: Preferred skills coverage
    total_pref_count = len(job.preferred_skills)
    if total_pref_count > 0:
        raw_pref_score = len(matched_pref) / total_pref_count
        pref_explanation = f"Matched {len(matched_pref)} of {total_pref_count} preferred skills ({round(raw_pref_score * 100, 1)}%)"
    else:
        raw_pref_score = 1.0
        pref_explanation = "No preferred skills specified; awarded baseline neutral credit."

    pref_evidence = [
        f"{ev.skill}: {ev.source_snippet}"
        for ev in skill_evidences
        if not ev.is_required and ev.status == "matched"
    ]

    # phi_3: Semantic similarity
    # Compare candidate summary/text against job description text
    cand_semantic_text = f"{resume.summary or ''} {' '.join([e.description for e in resume.experience])} {' '.join([p.description for p in resume.projects])}"
    if not cand_semantic_text.strip():
        cand_semantic_text = resume.raw_text

    sim_score, model_name = embedding_engine.compute_similarity(cand_semantic_text, job.raw_text)
    raw_sem_score = sim_score
    sem_explanation = f"Contextual semantic cosine similarity is {round(raw_sem_score * 100, 1)}% via {model_name}"
    sem_evidence = [
        f"Semantic Model: {model_name}",
        f"Analyzed {resume.word_count} words across candidate experience and projects.",
    ]

    # phi_4: Experience tenure alignment
    req_exp = job.min_experience_years
    found_exp = resume.total_experience_years
    if req_exp > 0:
        raw_exp_score = min(1.0, found_exp / req_exp)
        exp_explanation = f"Candidate has {found_exp} years of relevant experience vs {req_exp} years required ({round(raw_exp_score * 100, 1)}% of requirement met)"
    else:
        raw_exp_score = 1.0
        exp_explanation = f"No minimum experience tenure required; candidate has {found_exp} years documented."

    exp_evidence = [
        f"{e.role} ({e.duration_years} yrs): {e.snippet}"
        for e in resume.experience[:3]
        if e.snippet
    ]

    # phi_5: Project evidence
    num_projects = len(resume.projects)
    if num_projects > 0:
        proj_tech_matches = sum(
            1 for p in resume.projects
            if any(t in job.required_skills or t in job.preferred_skills for t in p.technologies)
        )
        tech_ratio = proj_tech_matches / max(1, num_projects)
        raw_proj_score = min(1.0, (num_projects / 2.0)) * (0.5 + 0.5 * tech_ratio)
        proj_explanation = f"Evaluated {num_projects} technical projects; {proj_tech_matches} directly apply relevant target technologies."
    else:
        raw_proj_score = 0.2  # Minimal fallback
        proj_explanation = "No structured project portfolio found in resume; minor score impact."

    proj_evidence = [
        f"{p.title}: {p.snippet} [Tech: {', '.join(p.technologies)}]"
        for p in resume.projects[:3]
        if p.snippet
    ]

    # Compute weighted scores
    breakdown = [
        ComponentScore(
            name="Required Skills",
            raw_score=round(raw_req_score, 4),
            weight=weights.required_skills,
            weighted_score=round(raw_req_score * weights.required_skills, 4),
            explanation=req_explanation,
            evidence=req_evidence[:5],
        ),
        ComponentScore(
            name="Preferred Skills",
            raw_score=round(raw_pref_score, 4),
            weight=weights.preferred_skills,
            weighted_score=round(raw_pref_score * weights.preferred_skills, 4),
            explanation=pref_explanation,
            evidence=pref_evidence[:5],
        ),
        ComponentScore(
            name="Semantic Similarity",
            raw_score=round(raw_sem_score, 4),
            weight=weights.semantic_similarity,
            weighted_score=round(raw_sem_score * weights.semantic_similarity, 4),
            explanation=sem_explanation,
            evidence=sem_evidence,
        ),
        ComponentScore(
            name="Experience Tenure",
            raw_score=round(raw_exp_score, 4),
            weight=weights.experience,
            weighted_score=round(raw_exp_score * weights.experience, 4),
            explanation=exp_explanation,
            evidence=exp_evidence[:3],
        ),
        ComponentScore(
            name="Project Portfolio",
            raw_score=round(raw_proj_score, 4),
            weight=weights.projects,
            weighted_score=round(raw_proj_score * weights.projects, 4),
            explanation=proj_explanation,
            evidence=proj_evidence[:3],
        ),
    ]

    # Composite overall score
    composite_sum = sum(c.weighted_score for c in breakdown)
    overall_score = round(min(100.0, max(0.0, composite_sum * 100.0)), 1)

    # Recommendation tier
    if overall_score >= 80.0:
        tier = "Strong Match"
    elif overall_score >= 65.0:
        tier = "Potential Match"
    elif overall_score >= 50.0:
        tier = "Borderline / Needs Review"
    else:
        tier = "Low Alignment"

    # Limitations & Uncertainties audit
    limitations = [
        "Uncalibrated match score indicates role-criteria alignment, not an absolute probability of on-the-job success.",
        "Missing skills reflect absence of evidence in the submitted text, not definitive proof of candidate inability.",
    ]
    if missing_req:
        limitations.append(f"Requires human verification for unmentioned mandatory skills: {', '.join(missing_req)}.")
    if found_exp < req_exp:
        limitations.append(f"Documented experience ({found_exp} yrs) is below requested minimum ({req_exp} yrs).")

    explanation_summary = (
        f"{tier} with overall match score of {overall_score}%. "
        f"Candidate satisfies {len(matched_req)}/{len(job.required_skills)} required skills "
        f"and has {found_exp} years documented experience. {req_explanation}."
    )

    return CandidateMatchResult(
        candidate_id=f"cand_{resume.resume_id.split('_')[-1]}",
        candidate_name=resume.candidate_name,
        resume_id=resume.resume_id,
        job_id=job.job_id,
        overall_score=overall_score,
        score_breakdown=breakdown,
        matched_required_skills=matched_req,
        missing_required_skills=missing_req,
        matched_preferred_skills=matched_pref,
        missing_preferred_skills=missing_pref,
        skill_evidences=skill_evidences,
        experience_years_found=found_exp,
        experience_years_required=req_exp,
        experience_evidence=exp_evidence,
        project_evidence=proj_evidence,
        explanation_summary=explanation_summary,
        limitations_and_uncertainties=limitations,
        recommendation_tier=tier,
    )
