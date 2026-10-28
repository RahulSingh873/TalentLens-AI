from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..schemas.match import (
    MatchRequest,
    ScreeningResponse,
    CandidateMatchResult,
)
from ..ml.scorer import calculate_candidate_match
from ..ml.ranking import rank_candidates
from ..services.storage import store

router = APIRouter(prefix="/api/match", tags=["Screening & Matching"])


class CompareRequest(BaseModel):
    job_id: str
    candidate_ids: List[str]


@router.post("/screen", response_model=ScreeningResponse)
def screen_candidates(payload: MatchRequest):
    """
    Screens candidate resumes against a target job posting,
    calculates explainable component scores, ranks candidates, and derives percentiles.
    """
    job_id = payload.job_id
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job description not found")

    job = store.jobs[job_id]

    # Candidate subset or all
    if payload.resume_ids:
        candidate_resumes = [store.resumes[rid] for rid in payload.resume_ids if rid in store.resumes]
    else:
        candidate_resumes = list(store.resumes.values())

    if not candidate_resumes:
        return ScreeningResponse(
            job_id=job.job_id,
            job_title=job.title,
            total_evaluated=0,
            weights=payload.weights or job.weights,
            candidates=[],
        )

    # Compute matches
    match_results: List[CandidateMatchResult] = []
    if job_id not in store.match_results:
        store.match_results[job_id] = {}

    for resume in candidate_resumes:
        res = calculate_candidate_match(resume, job, custom_weights=payload.weights)
        match_results.append(res)
        store.match_results[job_id][res.candidate_id] = res

    # Rank & Calibrate
    ranked = rank_candidates(match_results)

    return ScreeningResponse(
        job_id=job.job_id,
        job_title=job.title,
        total_evaluated=len(ranked),
        weights=payload.weights or job.weights,
        candidates=ranked,
    )


@router.get("/candidate/{job_id}/{candidate_id}", response_model=CandidateMatchResult)
def get_candidate_analysis(job_id: str, candidate_id: str):
    """Retrieves full transparent scoring and evidence citations for a specific candidate."""
    if job_id in store.match_results and candidate_id in store.match_results[job_id]:
        return store.match_results[job_id][candidate_id]

    # Recompute if needed
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    # Locate resume by candidate_id
    resume = None
    for r in store.resumes.values():
        if f"cand_{r.resume_id.split('_')[-1]}" == candidate_id:
            resume = r
            break

    if not resume:
        raise HTTPException(status_code=404, detail="Candidate not found")

    res = calculate_candidate_match(resume, store.jobs[job_id])
    if job_id not in store.match_results:
        store.match_results[job_id] = {}
    store.match_results[job_id][candidate_id] = res
    return res


@router.post("/compare")
def compare_candidates(payload: CompareRequest):
    """Compares 2 to 4 candidates side-by-side against a job's requirements."""
    job_id = payload.job_id
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = store.jobs[job_id]
    candidates_analysis = []

    for cid in payload.candidate_ids:
        # Check cache or find resume
        res = None
        if job_id in store.match_results and cid in store.match_results[job_id]:
            res = store.match_results[job_id][cid]
        else:
            for r in store.resumes.values():
                if f"cand_{r.resume_id.split('_')[-1]}" == cid:
                    res = calculate_candidate_match(r, job)
                    break
        if res:
            candidates_analysis.append(res)

    if not candidates_analysis:
        raise HTTPException(status_code=400, detail="No matching candidates found for comparison")

    # Union of all required and preferred skills
    all_skills = list(dict.fromkeys(job.required_skills + job.preferred_skills))

    comparison_grid = []
    for skill in all_skills:
        is_req = skill in job.required_skills
        row = {
            "skill": skill,
            "is_required": is_req,
            "candidate_evaluations": {}
        }
        for cand in candidates_analysis:
            matched = any(ev.skill.lower() == skill.lower() and ev.status == "matched" for ev in cand.skill_evidences)
            snippet = next(
                (ev.source_snippet for ev in cand.skill_evidences if ev.skill.lower() == skill.lower() and ev.status == "matched"),
                None
            )
            row["candidate_evaluations"][cand.candidate_name] = {
                "matched": matched,
                "snippet": snippet
            }
        comparison_grid.append(row)

    return {
        "job_id": job.job_id,
        "job_title": job.title,
        "candidates": [
            {
                "candidate_id": c.candidate_id,
                "candidate_name": c.candidate_name,
                "overall_score": c.overall_score,
                "recommendation_tier": c.recommendation_tier,
                "experience_years": c.experience_years_found,
                "matched_required_count": len(c.matched_required_skills),
                "total_required_count": len(job.required_skills),
            }
            for c in candidates_analysis
        ],
        "skill_comparison_grid": comparison_grid,
    }
