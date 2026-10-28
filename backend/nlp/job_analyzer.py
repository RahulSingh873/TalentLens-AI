import re
import uuid
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone

from .taxonomy import extract_skills_from_text, normalize_skill
from ..schemas.job import JobDescriptionCreate, JobDescriptionParsed, WeightConfig


# Requirement level boundary markers
REQUIRED_SECTION_PATTERNS = re.compile(
    r"(?:required|mandatory|must\s+have|minimum\s+qualifications|basic\s+qualifications|core\s+requirements):?",
    re.IGNORECASE,
)
PREFERRED_SECTION_PATTERNS = re.compile(
    r"(?:preferred|nice\s+to\s+have|bonus|plus|desired|optional|additional\s+qualifications):?",
    re.IGNORECASE,
)
EXP_REQUIREMENT_PATTERN = re.compile(
    r"\b(\d{1,2})\+?\s*(?:to\s*\d{1,2}\+?\s*)?years?(?:\s+of)?\s+(?:relevant|hands-on|industry|professional)?\s*(?:experience|exp)\b",
    re.IGNORECASE,
)


def extract_experience_requirement(text: str) -> float:
    """Extract required minimum years of experience from job text."""
    matches = EXP_REQUIREMENT_PATTERN.findall(text)
    if matches:
        try:
            return float(matches[0])
        except ValueError:
            pass
    return 2.0  # Reasonable default if unspecified


def analyze_job_description(job_in: JobDescriptionCreate) -> JobDescriptionParsed:
    """
    Parses job description into required skills, preferred skills,
    minimum years, responsibilities, and qualifications.
    """
    text = job_in.raw_text
    lines = text.splitlines()

    # Split into required vs preferred zones if present
    req_lines = []
    pref_lines = []
    resp_lines = []
    qual_lines = []

    current_mode = "general"
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if REQUIRED_SECTION_PATTERNS.search(stripped) and len(stripped.split()) <= 6:
            current_mode = "required"
            continue
        elif PREFERRED_SECTION_PATTERNS.search(stripped) and len(stripped.split()) <= 6:
            current_mode = "preferred"
            continue
        elif re.search(r"\b(?:responsibilities|duties|what\s+you'll\s+do)\b", stripped, re.IGNORECASE) and len(stripped.split()) <= 5:
            current_mode = "responsibilities"
            continue

        if current_mode == "required":
            req_lines.append(stripped)
        elif current_mode == "preferred":
            pref_lines.append(stripped)
        elif current_mode == "responsibilities":
            resp_lines.append(stripped)
        else:
            qual_lines.append(stripped)

    # If explicit skills were supplied by recruiter, prioritize those
    if job_in.required_skills:
        required_skills = list(dict.fromkeys(job_in.required_skills))
    else:
        req_text = "\n".join(req_lines) if req_lines else text
        req_extracted = extract_skills_from_text(req_text)
        required_skills = list(dict.fromkeys([s["canonical_name"] for s in req_extracted]))

    if job_in.preferred_skills:
        preferred_skills = [s for s in job_in.preferred_skills if s not in required_skills]
    else:
        pref_text = "\n".join(pref_lines)
        pref_extracted = extract_skills_from_text(pref_text)
        preferred_skills = [
            s["canonical_name"] for s in pref_extracted
            if s["canonical_name"] not in required_skills
        ]
        preferred_skills = list(dict.fromkeys(preferred_skills))

    # Experience years
    if job_in.min_experience_years is not None:
        min_exp = float(job_in.min_experience_years)
    else:
        min_exp = extract_experience_requirement(text)

    # Weights
    weights = job_in.weights or WeightConfig()

    return JobDescriptionParsed(
        job_id=f"job_{uuid.uuid4().hex[:10]}",
        title=job_in.title,
        company=job_in.company or "Enterprise",
        department=job_in.department or "Engineering",
        raw_text=text,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        min_experience_years=min_exp,
        responsibilities=resp_lines[:8],
        qualifications=qual_lines[:8],
        weights=weights,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
