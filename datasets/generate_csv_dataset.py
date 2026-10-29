"""
Generate TalentLens AI Benchmark Dataset in CSV format.
Suitable for:
1. Training and testing ML classification models (Binary Relevance: 1/0).
2. Information Retrieval (IR) Ranking Evaluation (NDCG@K, P@K, MRR).
3. Academic and industrial project submissions (HCLTech portal).

All candidate identities are synthetic, anonymized, and devoid of protected demographic attributes.
"""

import csv
import os
import random

random.seed(42)

JOBS = [
    {
        "job_id": "JOB_ML_01",
        "job_title": "Machine Learning / NLP Engineer",
        "department": "Artificial Intelligence & Data",
        "required_skills": ["Python", "PyTorch", "Natural Language Processing", "Transformers"],
        "preferred_skills": ["Docker", "AWS", "MLOps", "FastAPI"],
        "min_experience_years": 3.0,
        "job_description": "Seeking an ML Engineer with strong Python and PyTorch expertise, practical experience in Natural Language Processing, and HuggingFace Transformers to build and deploy language models."
    },
    {
        "job_id": "JOB_FSD_02",
        "job_title": "Full-Stack Cloud Engineer",
        "department": "Platform Engineering",
        "required_skills": ["Python", "FastAPI", "React", "PostgreSQL"],
        "preferred_skills": ["Docker", "TypeScript", "Tailwind CSS", "AWS"],
        "min_experience_years": 2.5,
        "job_description": "Looking for a Full-Stack Engineer proficient in Python, FastAPI, React, and PostgreSQL to design and maintain responsive enterprise cloud applications."
    },
    {
        "job_id": "JOB_DE_03",
        "job_title": "Data Platform & ETL Engineer",
        "department": "Enterprise Data Analytics",
        "required_skills": ["Python", "SQL", "Apache Spark", "Kafka"],
        "preferred_skills": ["Snowflake", "Docker", "AWS", "Airflow"],
        "min_experience_years": 3.5,
        "job_description": "Hiring a Data Engineer with hands-on skills in Python, distributed SQL, Apache Spark, and real-time Kafka streaming architectures to orchestrate high-throughput data pipelines."
    },
    {
        "job_id": "JOB_DEVOPS_04",
        "job_title": "Cloud DevOps & Kubernetes Engineer",
        "department": "Infrastructure & Cloud",
        "required_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
        "preferred_skills": ["Terraform", "Python", "Prometheus", "Bash"],
        "min_experience_years": 4.0,
        "job_description": "Seeking a Cloud DevOps Engineer to manage scalable Kubernetes clusters, Docker containerization, automated CI/CD pipelines, and infrastructure on AWS."
    },
    {
        "job_id": "JOB_CYBER_05",
        "job_title": "Cybersecurity & Application Security Analyst",
        "department": "Information Security",
        "required_skills": ["Linux", "Network Security", "Python", "Vulnerability Assessment"],
        "preferred_skills": ["SIEM", "Docker", "Cryptography", "OWASP"],
        "min_experience_years": 3.0,
        "job_description": "Seeking an Application Security Analyst skilled in Linux network security, vulnerability assessments, OWASP guidelines, and Python scripting for threat intelligence."
    }
]

CANDIDATES = [
    # ML / NLP profiles
    ("Alice Chen", 6.0, "Master of Science", "Computer Science",
     ["Python", "PyTorch", "Natural Language Processing", "Transformers", "Docker", "AWS", "MLOps"],
     "Senior Machine Learning Engineer with 6 years experience fine-tuning LLMs, PyTorch transformer pipelines, and deploying scalable MLOps inference microservices on AWS.",
     "JOB_ML_01", 1, 2),

    ("Elena Rostov", 4.5, "Ph.D.", "Computational Linguistics",
     ["Python", "PyTorch", "Natural Language Processing", "Transformers", "TensorFlow"],
     "NLP Research Scientist specializing in transformer-based sentiment analysis, tokenization algorithms, and generative language modeling with PyTorch.",
     "JOB_ML_01", 1, 2),

    ("Priya Sharma", 3.5, "Master of Technology", "Artificial Intelligence",
     ["Python", "PyTorch", "Transformers", "scikit-learn", "FastAPI", "Docker"],
     "AI Engineer with 3.5 years building text classification and embedding retrieval architectures using PyTorch, HuggingFace, and FastAPI endpoints.",
     "JOB_ML_01", 1, 2),

    ("Morgan Lee", 2.0, "Bachelor of Science", "Statistics & Data Science",
     ["Python", "Pandas", "NumPy", "scikit-learn", "SQL"],
     "Junior Data Scientist focused on exploratory statistical modeling, tabular feature engineering, regression models, and SQL querying.",
     "JOB_ML_01", 0, 1),

    ("Vikram Malhotra", 5.0, "Bachelor of Engineering", "Computer Science",
     ["Python", "TensorFlow", "Computer Vision", "OpenCV", "Docker"],
     "Computer Vision Specialist with 5 years developing convolutional neural networks, object detection models in OpenCV, and TensorFlow inference.",
     "JOB_ML_01", 0, 1),

    ("Samantha Brooks", 1.5, "Bachelor of Science", "Information Systems",
     ["Python", "HTML", "CSS", "SQL"],
     "Associate Software Analyst with 1.5 years experience in automated testing, basic Python scripting, and SQL relational database queries.",
     "JOB_ML_01", 0, 0),

    # Full-Stack profiles
    ("Jordan Smith", 4.0, "Bachelor of Science", "Software Engineering",
     ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "TypeScript", "Tailwind CSS"],
     "Full-Stack Software Engineer with 4 years designing RESTful APIs in FastAPI, interactive React/TypeScript single-page applications, and PostgreSQL data schemas.",
     "JOB_FSD_02", 1, 2),

    ("Carol Zhang", 5.0, "Master of Science", "Information Technology",
     ["React", "TypeScript", "Node.js", "Python", "FastAPI", "PostgreSQL", "Tailwind CSS"],
     "Senior Full-Stack Developer with 5 years building responsive web frontends in React and TypeScript with scalable Python backend services.",
     "JOB_FSD_02", 1, 2),

    ("Amitabh Sen", 3.0, "Bachelor of Technology", "Computer Engineering",
     ["Python", "Django", "FastAPI", "PostgreSQL", "React", "Docker"],
     "Web Applications Engineer with 3 years deploying Django and FastAPI microservices, implementing React UI views, and managing PostgreSQL databases.",
     "JOB_FSD_02", 1, 2),

    ("Liam Gallagher", 2.0, "Bachelor of Science", "Computer Science",
     ["Python", "Flask", "PostgreSQL", "Git"],
     "Junior Backend Developer with 2 years maintaining Flask endpoints and writing SQL queries for PostgreSQL databases.",
     "JOB_FSD_02", 0, 1),

    ("Marcus Vance", 7.0, "Bachelor of Engineering", "Electrical Engineering",
     ["C++", "Embedded Systems", "Linux", "Python", "RTOS"],
     "Embedded Firmware Engineer with 7 years developing low-level RTOS device drivers, microcontroller firmware, and C++ communication protocols.",
     "JOB_FSD_02", 0, 0),

    ("Chloe Bennett", 3.5, "Bachelor of Design", "HCI & Web Design",
     ["Figma", "HTML", "CSS", "JavaScript", "React"],
     "UI/UX Frontend Designer focused on user journey wireframing in Figma, design systems, HTML5/CSS3 styling, and React component prototyping.",
     "JOB_FSD_02", 0, 1),

    # Data Platform profiles
    ("Bob Martinez", 5.5, "Master of Science", "Data Analytics",
     ["Python", "SQL", "Apache Spark", "Kafka", "Docker", "AWS", "Airflow", "Snowflake"],
     "Lead Data Platform Engineer with 5.5 years designing distributed streaming ETL architectures using Apache Spark, Kafka, and Airflow orchestration.",
     "JOB_DE_03", 1, 2),

    ("Deepak Joshi", 4.0, "Bachelor of Engineering", "Information Technology",
     ["Python", "SQL", "Apache Spark", "Kafka", "PostgreSQL", "AWS"],
     "Data Engineer with 4 years building batch and real-time ingestion pipelines in PySpark, managing Kafka topics, and optimizing analytical SQL queries.",
     "JOB_DE_03", 1, 2),

    ("Hannah Arendt", 3.5, "Master of Science", "Applied Mathematics",
     ["Python", "SQL", "Apache Spark", "Snowflake", "Pandas"],
     "Big Data Analyst with 3.5 years building automated ETL transformations in PySpark and Snowflake data warehouses for corporate business intelligence.",
     "JOB_DE_03", 1, 2),

    ("Tariq Al-Mansoor", 2.5, "Bachelor of Science", "Computer Science",
     ["Python", "SQL", "MongoDB", "Pandas"],
     "Database Analyst with 2.5 years experience writing transactional SQL queries, optimizing MongoDB NoSQL schemas, and statistical data cleaning in Pandas.",
     "JOB_DE_03", 0, 1),

    ("Rachel Green", 1.0, "Bachelor of Commerce", "Business Analytics",
     ["Excel", "Power BI", "SQL", "Python"],
     "Junior BI Reporting Analyst with 1 year creating Power BI KPI dashboards and extracting executive summaries using SQL.",
     "JOB_DE_03", 0, 0),

    # Cloud DevOps profiles
    ("Casey Rivera", 6.0, "Bachelor of Science", "Computer Engineering",
     ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Terraform", "Python", "Prometheus"],
     "Principal Cloud DevOps Architect with 6 years provisioning Terraform infrastructure as code, maintaining multi-tenant Kubernetes clusters, and AWS security.",
     "JOB_DEVOPS_04", 1, 2),

    ("Kavita Rao", 4.5, "Master of Technology", "Cloud Computing",
     ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Bash", "Python"],
     "Site Reliability Engineer with 4.5 years managing automated GitHub Actions CI/CD pipelines, containerizing services with Docker, and monitoring Linux servers.",
     "JOB_DEVOPS_04", 1, 2),

    ("Dmitri Volkov", 4.0, "Bachelor of Science", "Telecommunications",
     ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Ansible"],
     "DevOps Systems Administrator with 4 years orchestrating Docker containers, managing Linux production clusters, and deploying AWS EC2/EKS workloads.",
     "JOB_DEVOPS_04", 1, 2),

    ("Lucas Silva", 2.0, "Bachelor of Science", "Information Technology",
     ["Linux", "Docker", "Git", "Bash"],
     "Junior Systems Administrator with 2 years managing Ubuntu servers, shell scripting, and basic Docker container deployments.",
     "JOB_DEVOPS_04", 0, 1),

    ("Zoe Saldana", 3.0, "Bachelor of Arts", "Digital Media",
     ["WordPress", "HTML", "CSS", "PHP", "cPanel"],
     "Web Administrator with 3 years hosting WordPress websites, managing cPanel domains, and writing basic PHP templates.",
     "JOB_DEVOPS_04", 0, 0),

    # Cybersecurity profiles
    ("Gabriel Torres", 5.0, "Master of Science", "Information Security",
     ["Linux", "Network Security", "Python", "Vulnerability Assessment", "SIEM", "OWASP", "Docker"],
     "Senior Security Operations Analyst with 5 years managing Splunk SIEM alerts, vulnerability pen-testing, Linux hardening, and Python automation scripts.",
     "JOB_CYBER_05", 1, 2),

    ("Sunita Mehra", 4.0, "Bachelor of Technology", "Cyber Security",
     ["Linux", "Network Security", "Python", "Vulnerability Assessment", "Cryptography", "Wireshark"],
     "Application Security Engineer with 4 years conducting network security audits, vulnerability scans with Nessus, and writing Python packet sniffers.",
     "JOB_CYBER_05", 1, 2),

    ("Julian Ward", 2.5, "Bachelor of Science", "Computer Forensics",
     ["Linux", "Python", "Network Security", "Wireshark"],
     "SOC Analyst with 2.5 years triaging network intrusion alerts, analyzing PCAP files, and basic Linux log investigations.",
     "JOB_CYBER_05", 1, 1),

    ("Brandon Lee", 1.5, "Bachelor of Science", "Networking",
     ["Cisco Packet Tracer", "Network Fundamentals", "Windows Server", "TCP/IP"],
     "Junior IT Support Specialist with 1.5 years configuring Cisco routers, subnetting LANs, and troubleshooting Windows workstations.",
     "JOB_CYBER_05", 0, 0),

    ("Fiona Gallagher", 3.5, "Bachelor of Engineering", "Electrical Engineering",
     ["MATLAB", "Simulink", "C", "PLC Programming"],
     "Controls Systems Engineer with 3.5 years developing PLC ladder logic and SCADA industrial automation interfaces in MATLAB.",
     "JOB_CYBER_05", 0, 0)
]

def calculate_metrics(cand_skills, job_req, job_pref, cand_exp, job_min_exp, base_label):
    cand_set = {s.lower() for s in cand_skills}
    req_set = {s.lower() for s in job_req}
    pref_set = {s.lower() for s in job_pref}

    req_overlap = len(cand_set.intersection(req_set))
    req_coverage = round(req_overlap / len(req_set), 3)

    pref_overlap = len(cand_set.intersection(pref_set))
    pref_coverage = round(pref_overlap / max(len(pref_set), 1), 3)

    exp_score = min(round(cand_exp / max(job_min_exp, 1.0), 3), 1.0)

    # Realistic simulated dense semantic similarity
    if base_label == 1:
        semantic_sim = round(random.uniform(0.78, 0.94), 3)
    else:
        semantic_sim = round(random.uniform(0.32, 0.65), 3)

    # Composite multi-attribute score (40% req, 15% pref, 25% semantic, 15% exp, 5% project)
    project_score = 0.9 if base_label == 1 else 0.5
    overall_score = round(
        (req_coverage * 0.40 +
         pref_coverage * 0.15 +
         semantic_sim * 0.25 +
         exp_score * 0.15 +
         project_score * 0.05) * 100,
        1
    )

    if overall_score >= 75.0:
        tier = "Strong Match"
    elif overall_score >= 55.0:
        tier = "Moderate Match"
    elif overall_score >= 40.0:
        tier = "Weak Match"
    else:
        tier = "Low Match"

    return req_overlap, req_coverage, pref_overlap, pref_coverage, semantic_sim, exp_score, overall_score, tier


def generate_dataset():
    output_path = os.path.join(os.path.dirname(__file__), "talentlens_evaluation_dataset.csv")
    job_map = {j["job_id"]: j for j in JOBS}

    rows = []
    pair_counter = 1

    # Generate primary target pairs
    for cand in CANDIDATES:
        name, exp, degree, field, skills, summary, target_job_id, suitability, grade = cand
        job = job_map[target_job_id]

        req_overlap, req_cov, pref_overlap, pref_cov, sem_sim, exp_score, match_score, tier = calculate_metrics(
            skills, job["required_skills"], job["preferred_skills"], exp, job["min_experience_years"], suitability
        )

        rows.append({
            "pair_id": f"TL_PAIR_{pair_counter:03d}",
            "candidate_id": f"CAND_{(pair_counter % 27) + 1:03d}",
            "candidate_name": name,
            "total_experience_years": exp,
            "education_level": degree,
            "degree_major": field,
            "extracted_skills": "; ".join(skills),
            "resume_summary": summary,
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "job_department": job["department"],
            "job_required_skills": "; ".join(job["required_skills"]),
            "job_preferred_skills": "; ".join(job["preferred_skills"]),
            "job_min_experience_years": job["min_experience_years"],
            "required_skill_overlap_count": req_overlap,
            "required_skill_coverage_ratio": req_cov,
            "preferred_skill_overlap_count": pref_overlap,
            "preferred_skill_coverage_ratio": pref_cov,
            "semantic_similarity_score": sem_sim,
            "experience_fit_ratio": exp_score,
            "overall_match_score": match_score,
            "match_tier": tier,
            "ground_truth_relevance": suitability,
            "ranking_relevance_grade": grade,
            "evaluation_split": "train" if (pair_counter % 4 != 0) else "test"
        })
        pair_counter += 1

    # Cross-match pairs (to create realistic negative/cross-domain examples for robust ML evaluation)
    cross_pairs = [
        # ML candidate applied to Full-Stack
        (CANDIDATES[0], "JOB_FSD_02", 0, 0),
        (CANDIDATES[1], "JOB_DE_03", 0, 1),
        # Full-stack applied to ML
        (CANDIDATES[6], "JOB_ML_01", 0, 1),
        (CANDIDATES[7], "JOB_DEVOPS_04", 0, 1),
        # Data engineer applied to ML
        (CANDIDATES[12], "JOB_ML_01", 1, 1),
        # DevOps applied to Full-Stack
        (CANDIDATES[17], "JOB_FSD_02", 0, 1),
        # Cyber analyst applied to Cloud DevOps
        (CANDIDATES[22], "JOB_DEVOPS_04", 0, 1),
        # Junior developer applied to Senior Cloud DevOps
        (CANDIDATES[3], "JOB_DEVOPS_04", 0, 0),
        # ML researcher applied to Cybersecurity
        (CANDIDATES[2], "JOB_CYBER_05", 0, 0),
        # Full-Stack applied to Data Platform
        (CANDIDATES[8], "JOB_DE_03", 0, 1),
        # Data Engineer applied to Cybersecurity
        (CANDIDATES[13], "JOB_CYBER_05", 0, 0),
        # DevOps applied to Data Platform
        (CANDIDATES[18], "JOB_DE_03", 0, 1),
        # Embedded applied to ML
        (CANDIDATES[10], "JOB_ML_01", 0, 0),
        # UI designer applied to Data Platform
        (CANDIDATES[11], "JOB_DE_03", 0, 0),
        # Junior support applied to Full-Stack
        (CANDIDATES[25], "JOB_FSD_02", 0, 0),
        # Associate applied to DevOps
        (CANDIDATES[5], "JOB_DEVOPS_04", 0, 0),
        # Controls engineer applied to NLP
        (CANDIDATES[26], "JOB_ML_01", 0, 0),
        # Data analyst applied to NLP
        (CANDIDATES[14], "JOB_ML_01", 0, 1),
        # SRE applied to Full-Stack
        (CANDIDATES[19], "JOB_FSD_02", 0, 1),
        # SecOps applied to NLP
        (CANDIDATES[23], "JOB_ML_01", 0, 0),
        # SysAdmin applied to Cybersecurity
        (CANDIDATES[20], "JOB_CYBER_05", 1, 1),
        # Lead ML applied to Data Platform
        (CANDIDATES[0], "JOB_DE_03", 0, 1),
        # Lead Data Engineer applied to Cloud DevOps
        (CANDIDATES[12], "JOB_DEVOPS_04", 1, 1)
    ]

    for cand_tuple, cross_job_id, suitability, grade in cross_pairs:
        name, exp, degree, field, skills, summary, _, _, _ = cand_tuple
        job = job_map[cross_job_id]

        req_overlap, req_cov, pref_overlap, pref_cov, sem_sim, exp_score, match_score, tier = calculate_metrics(
            skills, job["required_skills"], job["preferred_skills"], exp, job["min_experience_years"], suitability
        )

        rows.append({
            "pair_id": f"TL_PAIR_{pair_counter:03d}",
            "candidate_id": f"CAND_{(pair_counter % 27) + 1:03d}",
            "candidate_name": name,
            "total_experience_years": exp,
            "education_level": degree,
            "degree_major": field,
            "extracted_skills": "; ".join(skills),
            "resume_summary": summary,
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "job_department": job["department"],
            "job_required_skills": "; ".join(job["required_skills"]),
            "job_preferred_skills": "; ".join(job["preferred_skills"]),
            "job_min_experience_years": job["min_experience_years"],
            "required_skill_overlap_count": req_overlap,
            "required_skill_coverage_ratio": req_cov,
            "preferred_skill_overlap_count": pref_overlap,
            "preferred_skill_coverage_ratio": pref_cov,
            "semantic_similarity_score": sem_sim,
            "experience_fit_ratio": exp_score,
            "overall_match_score": match_score,
            "match_tier": tier,
            "ground_truth_relevance": suitability,
            "ranking_relevance_grade": grade,
            "evaluation_split": "train" if (pair_counter % 4 != 0) else "test"
        })
        pair_counter += 1

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} benchmark records at: {output_path}")

if __name__ == "__main__":
    generate_dataset()
