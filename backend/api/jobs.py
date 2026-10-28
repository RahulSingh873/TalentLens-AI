from typing import List
from fastapi import APIRouter, HTTPException
from ..schemas.job import JobDescriptionCreate, JobDescriptionParsed
from ..nlp.job_analyzer import analyze_job_description
from ..services.storage import store

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("", response_model=JobDescriptionParsed)
def create_job(payload: JobDescriptionCreate):
    """Creates, analyzes, and segments a new job posting into criteria."""
    parsed_job = analyze_job_description(payload)
    store.jobs[parsed_job.job_id] = parsed_job
    return parsed_job


@router.get("", response_model=List[JobDescriptionParsed])
def list_jobs():
    """Returns all active job postings."""
    return list(store.jobs.values())


@router.get("/{job_id}", response_model=JobDescriptionParsed)
def get_job(job_id: str):
    """Retrieves structured requirements for a job posting."""
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return store.jobs[job_id]


@router.put("/{job_id}", response_model=JobDescriptionParsed)
def update_job(job_id: str, payload: JobDescriptionCreate):
    """Allows recruiters to edit and confirm job requirements and weights."""
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job posting not found")

    updated_job = analyze_job_description(payload)
    updated_job.job_id = job_id  # Retain original job ID
    store.jobs[job_id] = updated_job
    return updated_job


@router.delete("/{job_id}")
def delete_job(job_id: str):
    """Deletes a job posting."""
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job posting not found")
    del store.jobs[job_id]
    return {"message": "Job deleted successfully", "job_id": job_id}
