from typing import List, Optional
from ..schemas.match import CandidateMatchResult


def rank_candidates(
    candidates: List[CandidateMatchResult],
    min_score: float = 0.0,
    required_skill_filter: Optional[str] = None
) -> List[CandidateMatchResult]:
    """
    Ranks candidates by overall score descending, calculates cohort
    relative percentiles, and assigns rank position.
    """
    filtered = [c for c in candidates if c.overall_score >= min_score]

    if required_skill_filter:
        skill_clean = required_skill_filter.strip().lower()
        filtered = [
            c for c in filtered
            if any(s.lower() == skill_clean for s in c.matched_required_skills)
        ]

    # Sort descending
    sorted_candidates = sorted(filtered, key=lambda x: x.overall_score, reverse=True)
    n = len(sorted_candidates)

    for i, cand in enumerate(sorted_candidates):
        cand.ranked_position = i + 1
        # Percentile rank
        if n > 1:
            cand.calibrated_percentile = round(((n - 1 - i) / (n - 1)) * 100.0, 1)
        else:
            cand.calibrated_percentile = 100.0

    return sorted_candidates
