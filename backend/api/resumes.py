import os
import shutil
import tempfile
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel

from ..schemas.resume import ResumeParsedData
from ..nlp.parser import parse_resume, extract_raw_text
from ..services.storage import store

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])


class TextResumeInput(BaseModel):
    filename: Optional[str] = "candidate_resume.txt"
    raw_text: str


@router.post("/upload", response_model=ResumeParsedData)
async def upload_resume(file: UploadFile = File(...)):
    """Uploads and parses a PDF, DOCX, or TXT resume."""
    filename = file.filename or "uploaded_resume.pdf"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in [".pdf", ".docx", ".doc", ".txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Supported formats: .pdf, .docx, .txt"
        )

    # Save to a temporary file for parsing
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        parsed_resume = parse_resume(tmp_path, filename=filename)
        store.resumes[parsed_resume.resume_id] = parsed_resume
        return parsed_resume
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post("/parse-text", response_model=ResumeParsedData)
def parse_text_resume(payload: TextResumeInput):
    """Parses plain text resume content."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
        tmp.write(payload.raw_text)
        tmp_path = tmp.name

    try:
        parsed_resume = parse_resume(tmp_path, filename=payload.filename)
        store.resumes[parsed_resume.resume_id] = parsed_resume
        return parsed_resume
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.get("", response_model=List[ResumeParsedData])
def list_resumes():
    """Lists all stored parsed candidate resumes."""
    return list(store.resumes.values())


@router.get("/{resume_id}", response_model=ResumeParsedData)
def get_resume(resume_id: str):
    """Retrieves full parsed structured information for a specific resume."""
    if resume_id not in store.resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    return store.resumes[resume_id]


@router.delete("/{resume_id}")
def delete_resume(resume_id: str):
    """Deletes a resume from the active pool."""
    if resume_id not in store.resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    del store.resumes[resume_id]
    return {"message": "Resume deleted successfully", "resume_id": resume_id}
