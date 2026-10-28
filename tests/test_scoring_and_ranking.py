from backend.services.storage import store
from backend.ml.scorer import calculate_candidate_match
from backend.ml.ranking import rank_candidates


def test_calculate_candidate_match_explainability():
    resume = store.resumes["res_alice_chen"]
    job = store.jobs["job_senior_nlp_engineer"]

    result = calculate_candidate_match(resume, job)

    assert result.candidate_name == "Alice Chen"
    assert result.overall_score >= 70.0
    assert result.recommendation_tier in ["Strong Match", "Potential Match"]

    # Verify score breakdown has exactly 5 explainable components
    assert len(result.score_breakdown) == 5
    component_names = [c.name for c in result.score_breakdown]
    assert "Required Skills" in component_names
    assert "Preferred Skills" in component_names
    assert "Semantic Similarity" in component_names
    assert "Experience Tenure" in component_names
    assert "Project Portfolio" in component_names

    # Check evidence citations
    assert len(result.skill_evidences) > 0
    assert any(ev.skill == "PyTorch" and ev.status == "matched" for ev in result.skill_evidences)
    assert len(result.limitations_and_uncertainties) > 0


def test_ranking_and_percentiles():
    job = store.jobs["job_senior_nlp_engineer"]
    candidates = [
        calculate_candidate_match(r, job)
        for r in store.resumes.values()
    ]

    ranked = rank_candidates(candidates)

    # Must be sorted descending
    for i in range(len(ranked) - 1):
        assert ranked[i].overall_score >= ranked[i + 1].overall_score
        assert ranked[i].ranked_position == i + 1

    # Check top candidate
    assert ranked[0].calibrated_percentile == 100.0
