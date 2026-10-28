import os
import json
from typing import Dict, List, Optional
from ..schemas.resume import (
    ResumeParsedData,
    SkillItem,
    ExperienceItem,
    EducationItem,
    ProjectItem,
)
from ..schemas.job import JobDescriptionParsed, WeightConfig
from ..schemas.match import CandidateMatchResult


class DataStore:
    """
    Thread-safe repository managing stored Resumes, Job Descriptions,
    and Screening Evaluations with realistic demonstration records preloaded.
    """

    def __init__(self):
        self.resumes: Dict[str, ResumeParsedData] = {}
        self.jobs: Dict[str, JobDescriptionParsed] = {}
        self.match_results: Dict[str, Dict[str, CandidateMatchResult]] = {}  # job_id -> {resume_id: result}
        self._seed_default_data()

    def _seed_default_data(self):
        # Seed 4 realistic, diverse benchmark resumes
        resumes_data = [
            ResumeParsedData(
                resume_id="res_alice_chen",
                filename="alice_chen_ml_lead.pdf",
                file_type="pdf",
                candidate_name="Alice Chen",
                email="alice.chen@example.com",
                phone="+1 (555) 234-5678",
                word_count=420,
                raw_text="Alice Chen. Senior Machine Learning Engineer with 5+ years building deep learning systems in Python and PyTorch. Expertise in Transformers, Natural Language Processing, MLOps, Docker, and AWS. Previously at TechCorp.",
                total_experience_years=5.5,
                skills=[
                    SkillItem(canonical_name="Python", raw_name="Python", category="Programming Languages", confidence=1.0, evidence_snippet="Built production pipelines in Python for NLP models."),
                    SkillItem(canonical_name="PyTorch", raw_name="PyTorch", category="Machine Learning & AI", confidence=1.0, evidence_snippet="Trained custom BERT and RoBERTa architectures in PyTorch."),
                    SkillItem(canonical_name="Natural Language Processing", raw_name="NLP", category="Machine Learning & AI", confidence=1.0, evidence_snippet="5+ years building deep learning systems and NLP pipelines."),
                    SkillItem(canonical_name="Transformers", raw_name="Transformers", category="Machine Learning & AI", confidence=1.0, evidence_snippet="Fine-tuned Hugging Face Transformers for domain-specific NER."),
                    SkillItem(canonical_name="Docker", raw_name="Docker", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Containerized microservices using Docker for AWS deployment."),
                    SkillItem(canonical_name="AWS", raw_name="AWS", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Deployed scalable inference endpoints on AWS SageMaker and EC2."),
                    SkillItem(canonical_name="MLOps", raw_name="MLOps", category="Machine Learning & AI", confidence=1.0, evidence_snippet="Implemented automated CI/CD and MLOps tracking with MLflow."),
                    SkillItem(canonical_name="SQL", raw_name="SQL", category="Databases & Query Languages", confidence=1.0, evidence_snippet="Queried feature sets using PostgreSQL and BigQuery."),
                ],
                experience=[
                    ExperienceItem(
                        role="Lead Machine Learning Engineer",
                        company="TechCorp AI Labs",
                        start_date="2021",
                        end_date="Present",
                        duration_years=3.5,
                        description="Led an NLP engineering team developing semantic search and retrieval systems.",
                        matched_skills=["Python", "PyTorch", "Transformers", "AWS", "Docker"],
                        snippet="Led an NLP engineering team developing semantic search and retrieval systems.",
                    ),
                    ExperienceItem(
                        role="Machine Learning Specialist",
                        company="DataInnovate Inc",
                        start_date="2019",
                        end_date="2021",
                        duration_years=2.0,
                        description="Developed classification algorithms and automated data pipelines.",
                        matched_skills=["Python", "scikit-learn", "SQL"],
                        snippet="Developed classification algorithms and automated data pipelines.",
                    ),
                ],
                education=[
                    EducationItem(
                        degree="Master of Science",
                        institution="Carnegie Mellon University",
                        field_of_study="Computer Science & Machine Learning",
                        graduation_year=2019,
                        snippet="M.S. in Computer Science & Machine Learning, Carnegie Mellon University (2019).",
                    )
                ],
                projects=[
                    ProjectItem(
                        title="Neural Talent Search Engine",
                        description="Engineered dense embedding search pipeline using SentenceTransformers and FastAPI.",
                        technologies=["Python", "FastAPI", "Transformers", "Docker"],
                        snippet="Engineered dense embedding search pipeline using SentenceTransformers and FastAPI.",
                    )
                ],
                certifications=[],
                summary="Senior ML Engineer with extensive production experience in NLP, Transformers, and MLOps infrastructure.",
            ),
            ResumeParsedData(
                resume_id="res_bob_martinez",
                filename="bob_martinez_fullstack.pdf",
                file_type="pdf",
                candidate_name="Bob Martinez",
                email="bob.m@example.com",
                phone="+1 (555) 876-5432",
                word_count=380,
                raw_text="Bob Martinez. Full Stack Software Engineer with 4 years experience in Python, FastAPI, React, TypeScript, PostgreSQL, and Docker. Passionate about building interactive AI dashboards.",
                total_experience_years=4.0,
                skills=[
                    SkillItem(canonical_name="Python", raw_name="Python", category="Programming Languages", confidence=1.0, evidence_snippet="Built REST APIs using Python and FastAPI."),
                    SkillItem(canonical_name="FastAPI", raw_name="FastAPI", category="Backend Engineering", confidence=1.0, evidence_snippet="Designed high-performance async endpoints in FastAPI."),
                    SkillItem(canonical_name="React", raw_name="React", category="Frontend Engineering", confidence=1.0, evidence_snippet="Developed dynamic candidate management UI in React."),
                    SkillItem(canonical_name="TypeScript", raw_name="TypeScript", category="Programming Languages", confidence=1.0, evidence_snippet="Authored type-safe frontend modules in TypeScript."),
                    SkillItem(canonical_name="PostgreSQL", raw_name="PostgreSQL", category="Databases & Storage", confidence=1.0, evidence_snippet="Optimized indexing for PostgreSQL database schemas."),
                    SkillItem(canonical_name="Docker", raw_name="Docker", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Containerized frontend and backend services with Docker Compose."),
                    SkillItem(canonical_name="Git", raw_name="Git", category="Tools & Version Control", confidence=1.0, evidence_snippet="Managed collaborative release workflows via Git."),
                ],
                experience=[
                    ExperienceItem(
                        role="Full Stack Engineer",
                        company="WebScale Solutions",
                        start_date="2022",
                        end_date="Present",
                        duration_years=2.5,
                        description="Developed interactive cloud dashboards and backend services using FastAPI and React.",
                        matched_skills=["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
                        snippet="Developed interactive cloud dashboards and backend services using FastAPI and React.",
                    ),
                    ExperienceItem(
                        role="Junior Web Developer",
                        company="AppStudio LLC",
                        start_date="2020",
                        end_date="2022",
                        duration_years=1.5,
                        description="Assisted in REST API integration and database migration.",
                        matched_skills=["Python", "JavaScript", "SQL"],
                        snippet="Assisted in REST API integration and database migration.",
                    ),
                ],
                education=[
                    EducationItem(
                        degree="Bachelor of Science",
                        institution="University of Washington",
                        field_of_study="Computer Science",
                        graduation_year=2020,
                        snippet="B.S. in Computer Science, University of Washington (2020).",
                    )
                ],
                projects=[
                    ProjectItem(
                        title="AI Talent Screener Web Portal",
                        description="Full-stack portal built with FastAPI backend and React frontend.",
                        technologies=["FastAPI", "React", "PostgreSQL", "Docker"],
                        snippet="Full-stack portal built with FastAPI backend and React frontend.",
                    )
                ],
                certifications=[],
                summary="Full-stack engineer with deep expertise in Python FastAPI, React, and cloud containerization.",
            ),
            ResumeParsedData(
                resume_id="res_carol_danvers",
                filename="carol_danvers_data_scientist.pdf",
                file_type="pdf",
                candidate_name="Carol Danvers",
                email="carol.d@example.com",
                phone="+1 (555) 345-6789",
                word_count=350,
                raw_text="Carol Danvers. Data Scientist with 3 years experience in Python, Pandas, NumPy, scikit-learn, SQL, and data visualization. Built statistical models and predictive churn algorithms.",
                total_experience_years=3.0,
                skills=[
                    SkillItem(canonical_name="Python", raw_name="Python", category="Programming Languages", confidence=1.0, evidence_snippet="Primary language for exploratory data analysis."),
                    SkillItem(canonical_name="Pandas", raw_name="Pandas", category="Data Science & Analytics", confidence=1.0, evidence_snippet="Data wrangling and feature engineering using Pandas."),
                    SkillItem(canonical_name="NumPy", raw_name="NumPy", category="Data Science & Analytics", confidence=1.0, evidence_snippet="Array computations and matrix transformations with NumPy."),
                    SkillItem(canonical_name="scikit-learn", raw_name="scikit-learn", category="Machine Learning & AI", confidence=1.0, evidence_snippet="Trained supervised classifiers and regressors using scikit-learn."),
                    SkillItem(canonical_name="SQL", raw_name="SQL", category="Databases & Query Languages", confidence=1.0, evidence_snippet="Extracted tabular metrics from PostgreSQL data warehouses."),
                ],
                experience=[
                    ExperienceItem(
                        role="Data Scientist",
                        company="Insight Analytics",
                        start_date="2021",
                        end_date="Present",
                        duration_years=3.0,
                        description="Designed classification models and retention prediction algorithms.",
                        matched_skills=["Python", "scikit-learn", "Pandas", "SQL"],
                        snippet="Designed classification models and retention prediction algorithms.",
                    )
                ],
                education=[
                    EducationItem(
                        degree="Bachelor of Science",
                        institution="UC Berkeley",
                        field_of_study="Statistics & Applied Mathematics",
                        graduation_year=2021,
                        snippet="B.S. in Statistics, UC Berkeley (2021).",
                    )
                ],
                projects=[
                    ProjectItem(
                        title="Customer Churn Predictor",
                        description="Trained gradient boosting models with scikit-learn achieving 88% ROC-AUC.",
                        technologies=["Python", "scikit-learn", "Pandas"],
                        snippet="Trained gradient boosting models with scikit-learn achieving 88% ROC-AUC.",
                    )
                ],
                certifications=[],
                summary="Data scientist focused on predictive modeling, exploratory analysis, and statistical validation.",
            ),
            ResumeParsedData(
                resume_id="res_david_kim",
                filename="david_kim_devops.docx",
                file_type="docx",
                candidate_name="David Kim",
                email="david.k@example.com",
                phone="+1 (555) 901-2345",
                word_count=310,
                raw_text="David Kim. Cloud DevOps Engineer with 4 years managing Kubernetes clusters, Docker containers, AWS infrastructure, Linux, and CI/CD automation pipelines.",
                total_experience_years=4.0,
                skills=[
                    SkillItem(canonical_name="Docker", raw_name="Docker", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Created optimized multi-stage Docker build images."),
                    SkillItem(canonical_name="Kubernetes", raw_name="Kubernetes", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Managed 15-node production Kubernetes cluster."),
                    SkillItem(canonical_name="AWS", raw_name="AWS", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Provisioned VPC, EKS, and IAM security groups on AWS."),
                    SkillItem(canonical_name="CI/CD", raw_name="CI/CD", category="Cloud & DevOps", confidence=1.0, evidence_snippet="Built automated release pipelines using GitHub Actions."),
                    SkillItem(canonical_name="Linux", raw_name="Linux", category="Systems & OS", confidence=1.0, evidence_snippet="Administered Ubuntu and RHEL server environments."),
                    SkillItem(canonical_name="Python", raw_name="Python", category="Programming Languages", confidence=1.0, evidence_snippet="Scripted automation utilities in Python and Bash."),
                ],
                experience=[
                    ExperienceItem(
                        role="DevOps Engineer",
                        company="CloudReliability Corp",
                        start_date="2020",
                        end_date="Present",
                        duration_years=4.0,
                        description="Engineered zero-downtime deployment pipelines on AWS and Kubernetes.",
                        matched_skills=["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
                        snippet="Engineered zero-downtime deployment pipelines on AWS and Kubernetes.",
                    )
                ],
                education=[
                    EducationItem(
                        degree="Bachelor of Engineering",
                        institution="Georgia Tech",
                        field_of_study="Electrical & Computer Engineering",
                        graduation_year=2020,
                        snippet="B.E. in Computer Engineering, Georgia Tech (2020).",
                    )
                ],
                projects=[
                    ProjectItem(
                        title="Infrastructure as Code for EKS",
                        description="Terraform and Kubernetes scripts to orchestrate cloud workloads.",
                        technologies=["Kubernetes", "AWS", "Docker"],
                        snippet="Terraform and Kubernetes scripts to orchestrate cloud workloads.",
                    )
                ],
                certifications=[],
                summary="Cloud and DevOps engineer focused on Kubernetes, Docker, automated CI/CD pipelines, and AWS.",
            ),
        ]

        for r in resumes_data:
            self.resumes[r.resume_id] = r

        # Seed 2 realistic benchmark jobs
        job_ml = JobDescriptionParsed(
            job_id="job_senior_nlp_engineer",
            title="Senior Machine Learning / NLP Engineer",
            company="HCLTech AI Labs",
            department="Applied Artificial Intelligence",
            raw_text="""
We are seeking an experienced Senior Machine Learning Engineer specializing in Natural Language Processing (NLP) to lead our semantic information retrieval initiatives.

Core Responsibilities:
- Design, train, and deploy deep learning NLP architectures and Transformer models.
- Build production-grade inference microservices using Python and Docker.
- Implement continuous model evaluation and MLOps deployment workflows on AWS.
- Collaborate with cross-functional teams to integrate recommendation engines.

Required Qualifications (Must Have):
- 3+ years of professional software engineering and ML experience.
- Strong proficiency in Python and deep learning frameworks like PyTorch.
- Hands-on experience with Natural Language Processing (NLP) and Transformers.
- Familiarity with containerization using Docker.

Preferred Qualifications (Nice to Have):
- Experience with MLOps tracking tools (e.g., MLflow, Kubeflow).
- Cloud deployment experience on AWS or Google Cloud.
- Knowledge of relational databases and SQL.
- Prior exposure to FastAPI and RESTful microservice architectures.
            """.strip(),
            required_skills=["Python", "PyTorch", "Natural Language Processing", "Transformers", "Docker"],
            preferred_skills=["MLOps", "AWS", "SQL", "FastAPI"],
            min_experience_years=3.0,
            responsibilities=[
                "Design, train, and deploy deep learning NLP architectures and Transformer models.",
                "Build production-grade inference microservices using Python and Docker.",
                "Implement continuous model evaluation and MLOps deployment workflows on AWS.",
            ],
            qualifications=[
                "Bachelor's or Master's degree in Computer Science, AI, or equivalent.",
                "3+ years of professional ML experience.",
            ],
            weights=WeightConfig(
                required_skills=0.40,
                preferred_skills=0.15,
                semantic_similarity=0.25,
                experience=0.15,
                projects=0.05,
            ),
            created_at="2026-10-28T10:00:00Z",
        )

        job_fullstack = JobDescriptionParsed(
            job_id="job_fullstack_ai_developer",
            title="Full Stack Software Engineer (Python & React)",
            company="HCLTech Enterprise Cloud",
            department="Cloud Applications",
            raw_text="""
Looking for a Full Stack Software Engineer to build AI-driven user interfaces and scalable backend microservices.

Core Responsibilities:
- Build high-throughput asynchronous REST APIs using FastAPI and Python.
- Develop responsive, state-driven user interfaces in React and TypeScript.
- Design normalized relational databases using PostgreSQL.
- Containerize application components using Docker.

Required Qualifications:
- 2+ years of full-stack web development experience.
- Strong proficiency in Python and FastAPI.
- Hands-on experience with React and modern JavaScript/TypeScript.
- Experience with PostgreSQL and SQL query optimization.

Preferred Qualifications:
- Familiarity with Docker and container workflows.
- Experience deploying to AWS.
- Knowledge of automated CI/CD pipelines.
            """.strip(),
            required_skills=["Python", "FastAPI", "React", "PostgreSQL"],
            preferred_skills=["Docker", "AWS", "CI/CD", "TypeScript"],
            min_experience_years=2.0,
            responsibilities=[
                "Build high-throughput asynchronous REST APIs using FastAPI and Python.",
                "Develop responsive, state-driven user interfaces in React and TypeScript.",
                "Design normalized relational databases using PostgreSQL.",
            ],
            qualifications=[
                "B.S. in Computer Science or related degree.",
                "2+ years of full-stack engineering.",
            ],
            weights=WeightConfig(
                required_skills=0.40,
                preferred_skills=0.15,
                semantic_similarity=0.25,
                experience=0.15,
                projects=0.05,
            ),
            created_at="2026-10-28T10:15:00Z",
        )

        self.jobs[job_ml.job_id] = job_ml
        self.jobs[job_fullstack.job_id] = job_fullstack


# Singleton store instance
store = DataStore()
