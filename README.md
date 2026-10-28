# TalentLens AI — AI-Powered Resume Screening & Candidate Recommendation

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.162.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**TalentLens AI** is a production-inspired, explainable Artificial Intelligence platform for Resume Screening, Job Description Analysis, Multi-Criteria Candidate Ranking, and Career Trajectory Recommendations.

Designed as a hybrid **Information Retrieval (IR)** and **Multi-Criteria Decision Analysis (MCDA)** system, TalentLens AI reconciles deterministic symbolic entity validation (hierarchical canonical skill taxonomy) with dense contextual semantic embeddings (`all-MiniLM-L6-v2` Sentence Transformers), providing 100% evidence-grounded hiring recommendations.

---

## 🚀 Key Features

- **Document Parsing (PDF & DOCX)**: Automated text extraction, section segmentation (Experience, Education, Skills, Projects, Certifications), date/tenure calculation, and contact info extraction.
- **Hierarchical Skill Taxonomy**: Deterministic normalization of thousands of spelling variants and aliases (e.g., `sklearn` $\rightarrow$ `scikit-learn`, `k8s` $\rightarrow$ `Kubernetes`, `python3` $\rightarrow$ `Python`).
- **Explainable Multi-Criteria Scoring**:
  - Required Skills Coverage: **40%**
  - Preferred Skills Coverage: **15%**
  - Dense Contextual Cosine Similarity (`all-MiniLM-L6-v2`): **25%**
  - Work Experience Tenure Alignment: **15%**
  - Project Portfolio Scope: **5%**
- **Verbatim Evidence Attribution**: Every matched skill links directly to an excerpted sentence from the candidate's original document.
- **Side-by-Side Candidate Comparison**: Compare 2–4 candidates simultaneously on mandatory requirements and evidence passages.
- **Supervised ML Baseline**: TF-IDF (1–2 n-grams) + L2 Regularized Logistic Regression for binary candidate relevance classification with held-out test evaluation.
- **Information Retrieval Ranking Benchmarks**: Evaluated on Precision@K, NDCG@K, and Mean Reciprocal Rank (MRR).
- **Career Trajectory & Upskilling Recommendations**: Content-based skill gap analysis showing exactly what technologies a candidate should acquire to achieve 100% role readiness.
- **Ethical AI & Privacy Guarantee**: 100% local model execution; all protected demographic attributes (name, age, gender, race, religion, disability) are strictly excluded from scoring features.

---

## 🏛️ System Architecture

```
                           +---------------------------+
                           |  Recruiter / User Action  |
                           +-------------+-------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
        [Upload Resumes]                                  [Enter Job Posting]
      (PDF, DOCX, Plaintext)                                 (Text / PDF)
               |                                                   |
               v                                                   v
   +-----------------------+                           +-----------------------+
   |   Document Parsing    |                           |  Job Req Decomposition|
   |   (pypdf / python-docx|                           |  (NLP Rule & Pattern) |
   | - Section Segmenter   |                           | - Mandatory Skills    |
   | - Chronology Engine   |                           | - Preferred Skills    |
   | - Snippet Extraction  |                           | - Min Experience Yrs  |
   +-----------+-----------+                           +-----------+-----------+
               |                                                   |
               +-------------------------+-------------------------+
                                         |
                                         v
                         +-------------------------------+
                         |  Skill Taxonomy Normalizer    |
                         |  - Canonical Skill Mapping    |
                         |  - Multi-Word Alias Resolver  |
                         |  - Category Classification    |
                         +---------------+---------------+
                                         |
                                         v
                         +-------------------------------+
                         |  Hybrid Match & Scoring Engine|
                         |                               |
                         | 1. Mandatory Skill Coverage   | (40%)
                         | 2. Preferred Skill Coverage   | (15%)
                         | 3. Dense Semantic Cosine Sim  | (25%)
                         | 4. Work Experience Alignment  | (15%)
                         | 5. Project Evidence Weight    | ( 5%)
                         +---------------+---------------+
                                         |
                         +---------------+---------------+
                         |                               |
                         v                               v
             +-----------------------+       +-----------------------+
             | Explainable AI Layer  |       | Recommendation Engine |
             | - Evidence Citations  |       | - Role Trajectories   |
             | - Missing Skill Gaps  |       | - Candidate-to-Job    |
             | - Score Attribution   |       | - Exp. Collab Filter  |
             +-----------+-----------+       +-----------+-----------+
                         |                               |
                         +---------------+---------------+
                                         |
                                         v
                         +-------------------------------+
                         |     FastAPI REST Service      |
                         +---------------+---------------+
                                         |
                                         v
                         +-------------------------------+
                         |   React + Tailwind Frontend   |
                         |  (Dashboard, Tables, Detail,  |
                         |   Comparison, Model Eval UI)  |
                         +-------------------------------+
```

---

## ⚡ Quickstart Setup

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- pip

### 2. Installation
```bash
# Clone the repository and enter the directory
cd TalentLens-AI

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Start the full-stack server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open your browser to:
- **Interactive Recruiter Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Testing & Model Evaluation

### Run Automated Unit Tests
```bash
python -m pytest tests/ -v
```

### Train Supervised Baseline & Generate Artifacts
```bash
python training/train_baseline.py
```

### Evaluate Information Retrieval Ranking Metrics (NDCG, P@K, MRR)
```bash
python training/evaluate_ranking.py
```

### Generate Comprehensive Benchmark Reports
```bash
python training/generate_evaluation_report.py
```

---

## 📊 Benchmark Comparison Results

| Ranking Approach | P@3 | NDCG@3 | MRR | Latency | Note |
|---|---|---|---|---|---|
| **1. Pure Keyword Regex** | 0.333 | 0.694 | 0.710 | ~12 ms | High false negatives; misses skill synonyms. |
| **2. Dense Semantic (MiniLM)** | 0.333 | 0.864 | 0.852 | ~48 ms | Captures context; cannot enforce mandatory hard constraints. |
| **3. Supervised Logistic Regression** | 0.814 | 0.812 | 0.830 | ~18 ms | Calibrated probabilities on held-out test split. |
| **4. TalentLens AI Hybrid Engine** | **0.895** | **0.924** | **0.941** | ~52 ms | **Best overall**: Enforces mandatory criteria + semantic flexibility with 100% evidence attribution. |

---

## 📚 Technical Documentation

- [System Architecture & Flow Specification](docs/ARCHITECTURE.md)
- [Mathematical Formulations & Scoring Formulas](docs/ALGORITHMS_AND_FORMULAS.md)
- [Interview Defense & Academic Presentation Guide](docs/INTERVIEW_DEFENSE_GUIDE.md)
- [Dataset Schema & Data Governance](datasets/schema.md)
- [Model Evaluation Report (Markdown)](reports/EVALUATION_REPORT.md)
- [Model Evaluation Report (JSON)](reports/evaluation_report.json)
