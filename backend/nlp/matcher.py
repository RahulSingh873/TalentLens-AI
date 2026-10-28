from typing import List, Dict, Tuple, Set
from .taxonomy import normalize_skill
from ..schemas.resume import ResumeParsedData, SkillItem
from ..schemas.match import SkillMatchEvidence


def match_skills_against_requirements(
    resume: ResumeParsedData,
    required_skills: List[str],
    preferred_skills: List[str]
) -> Tuple[List[str], List[str], List[str], List[str], List[SkillMatchEvidence]]:
    """
    Performs deterministic, evidence-backed skill matching between
    candidate extracted skills and job requirements.

    Returns:
    (matched_required, missing_required, matched_preferred, missing_preferred, skill_evidences)
    """
    # Build candidate canonical skill lookup with evidence snippets
    candidate_skill_map: Dict[str, SkillItem] = {}
    for skill in resume.skills:
        canonical_key = skill.canonical_name.strip().lower()
        candidate_skill_map[canonical_key] = skill

    matched_required: List[str] = []
    missing_required: List[str] = []
    matched_preferred: List[str] = []
    missing_preferred: List[str] = []
    skill_evidences: List[SkillMatchEvidence] = []

    # Check Required Skills
    for req in required_skills:
        req_norm = normalize_skill(req)
        canonical_name = req_norm["canonical"] if req_norm else req.strip()
        key = canonical_name.lower()

        if key in candidate_skill_map:
            cand_item = candidate_skill_map[key]
            matched_required.append(canonical_name)
            skill_evidences.append(
                SkillMatchEvidence(
                    skill=canonical_name,
                    status="matched",
                    is_required=True,
                    confidence=cand_item.confidence,
                    source_snippet=cand_item.evidence_snippet or f"Mentioned in resume ({cand_item.raw_name})",
                    match_type="exact" if cand_item.raw_name.lower() == canonical_name.lower() else "alias"
                )
            )
        else:
            missing_required.append(canonical_name)
            skill_evidences.append(
                SkillMatchEvidence(
                    skill=canonical_name,
                    status="missing",
                    is_required=True,
                    confidence=0.0,
                    source_snippet=None,
                    match_type="none"
                )
            )

    # Check Preferred Skills
    for pref in preferred_skills:
        pref_norm = normalize_skill(pref)
        canonical_name = pref_norm["canonical"] if pref_norm else pref.strip()
        key = canonical_name.lower()

        if key in candidate_skill_map:
            cand_item = candidate_skill_map[key]
            matched_preferred.append(canonical_name)
            skill_evidences.append(
                SkillMatchEvidence(
                    skill=canonical_name,
                    status="matched",
                    is_required=False,
                    confidence=cand_item.confidence,
                    source_snippet=cand_item.evidence_snippet or f"Mentioned in resume ({cand_item.raw_name})",
                    match_type="exact" if cand_item.raw_name.lower() == canonical_name.lower() else "alias"
                )
            )
        else:
            missing_preferred.append(canonical_name)
            skill_evidences.append(
                SkillMatchEvidence(
                    skill=canonical_name,
                    status="missing",
                    is_required=False,
                    confidence=0.0,
                    source_snippet=None,
                    match_type="none"
                )
            )

    return (
        matched_required,
        missing_required,
        matched_preferred,
        missing_preferred,
        skill_evidences
    )
