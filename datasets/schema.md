# TalentLens AI — Dataset Schema and Data Governance

## 1. Provenance and Synthetic Data Disclosure

All benchmark candidate records, job descriptions, and recruiter interaction logs provided in this repository are **documented synthetic records**. They were generated to establish rigorous algorithmic baselines without compromising private candidate records or violating GDPR / PII regulations.

> [!IMPORTANT]
> Synthetic demonstration labels must never be cited as empirical proof of real-world hiring effectiveness. Real-world deployment requires permissioned human-in-the-loop validation, legal compliance auditing, and continuous algorithmic bias monitoring.

---

## 2. Dataset Entities

### Resume Record Schema (`datasets/synthetic_resumes.json`)
```json
{
  "resume_id": "string (UUID)",
  "candidate_name": "string (Anonymized)",
  "skills": [
    {
      "canonical_name": "string",
      "category": "string",
      "confidence": "float [0.0, 1.0]",
      "evidence_snippet": "string"
    }
  ],
  "total_experience_years": "float",
  "education": [
    {
      "degree": "string",
      "field_of_study": "string",
      "graduation_year": "integer"
    }
  ],
  "projects": [
    {
      "title": "string",
      "technologies": ["string"]
    }
  ],
  "label_suitability": "integer (1: Qualified, 0: Not Qualified)"
}
```

### Job Description Schema (`datasets/synthetic_jobs.json`)
```json
{
  "job_id": "string",
  "title": "string",
  "department": "string",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "min_experience_years": "float"
}
```

---

## 3. Evaluation & Benchmark CSV Dataset (`datasets/talentlens_evaluation_dataset.csv`)

This dataset contains 50 paired candidate-job screening records across 5 engineering domains (Machine Learning/NLP, Full-Stack Cloud, Data Platform, Cloud DevOps, Cybersecurity).

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `pair_id` | string | Unique screening pair identifier | `TL_PAIR_001` |
| `candidate_id` | string | Anonymized candidate ID | `CAND_002` |
| `candidate_name` | string | Synthetic candidate full name | `Alice Chen` |
| `total_experience_years` | float | Candidate verified professional tenure | `6.0` |
| `education_level` | string | Highest degree attained | `Master of Science` |
| `degree_major` | string | Academic field of study | `Computer Science` |
| `extracted_skills` | string | Semicolon-separated canonical skill tags | `Python; PyTorch; Transformers` |
| `resume_summary` | string | Free-text professional summary | `Senior Machine Learning Engineer...` |
| `job_id` | string | Target job opening ID | `JOB_ML_01` |
| `job_title` | string | Target role title | `Machine Learning / NLP Engineer` |
| `job_department` | string | Hiring department | `Artificial Intelligence & Data` |
| `job_required_skills` | string | Semicolon-separated mandatory skills | `Python; PyTorch; NLP; Transformers` |
| `job_preferred_skills` | string | Semicolon-separated preferred skills | `Docker; AWS; MLOps; FastAPI` |
| `job_min_experience_years` | float | Minimum required experience | `3.0` |
| `required_skill_overlap_count` | integer | Number of matching required skills | `4` |
| `required_skill_coverage_ratio` | float | Fraction of required skills met [0.0 - 1.0] | `1.0` |
| `preferred_skill_overlap_count` | integer | Number of matching preferred skills | `3` |
| `preferred_skill_coverage_ratio` | float | Fraction of preferred skills met [0.0 - 1.0] | `0.75` |
| `semantic_similarity_score` | float | Dense Sentence Transformer cosine similarity | `0.882` |
| `experience_fit_ratio` | float | Experience ratio clamped to 1.0 | `1.0` |
| `overall_match_score` | float | 5-dimension MCDA composite score (0 - 100) | `92.8` |
| `match_tier` | string | Categorical classification | `Strong Match` |
| `ground_truth_relevance` | integer | Supervised binary suitability label (1: Yes, 0: No) | `1` |
| `ranking_relevance_grade` | integer | IR Graded Relevance (2: High, 1: Partial, 0: Irrelevant) | `2` |
| `evaluation_split` | string | Evaluation partition (`train` vs `test`) | `train` |

