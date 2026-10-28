# TalentLens AI — System Architecture & Design Specification

## 1. System Overview

**TalentLens AI** is an explainable, production-inspired AI platform designed for Resume Screening, Job Description Analysis, Candidate-Job Matching, and Career Trajectory Recommendations.

Unlike primitive keyword search tools or opaque "black-box" LLM prompts, TalentLens AI is architected as an **Information Retrieval (IR) and Multi-Criteria Decision Analysis (MCDA)** engine. It reconciles deterministic symbolic entity validation (skill taxonomy matching with syntactic & positional grounding) with continuous dense semantic representations (Sentence Transformers), providing transparent, evidence-backed hiring recommendations.

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
   |   (PyMuPDF/Docx/Regex)|                           |  (NLP Rule & Pattern) |
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
                         |  Hybrid Match & Scoring Engine |
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

## 2. Core Architectural Principles

1. **Separation of Concerns**: Document parsing, semantic feature extraction, multi-attribute scoring, recommendation, and HTTP transport layers are strictly decoupled into discrete modules.
2. **Deterministic Evidence Attribution**: Every skill claimed to be matched must link directly to an exact source sentence or bullet point extracted from the candidate's original document.
3. **No Demographics or Protected Attribute Scoring**: Names, addresses, gender markers, dates of birth, graduation decades, or institution prestige are never injected into feature vectors or scoring functions.
4. **Calibration Transparency**: Candidate scores represent relative compatibility with the evaluated job specification—never an uncalibrated "probability of job success."
5. **Privacy and Zero External Data Leaks**: All NLP models (tokenizers, taxonomy matchers, sentence embeddings) run entirely locally. Resumes are never dispatched to external third-party proprietary APIs.
