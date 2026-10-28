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
