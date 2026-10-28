# TalentLens AI — Mathematical Formulations and Algorithm Selection

## 1. Problem Formulation

Automated candidate screening is formally formulated as a constrained **Multi-Attribute Utility Theory (MAUT)** and **Rank-Order Information Retrieval** problem.

Let $J = \{S_{\text{req}}, S_{\text{pref}}, E_{\text{min}}, D_J\}$ represent a structured Job Description, where:
- $S_{\text{req}} = \{s_1^*, s_2^*, \dots, s_m^*\}$ is the set of mandatory skills.
- $S_{\text{pref}} = \{p_1^*, p_2^*, \dots, p_k^*\}$ is the set of preferred skills.
- $E_{\text{min}} \in \mathbb{R}_{\ge 0}$ is the minimum required relevant professional experience in years.
- $D_J \in \mathbb{R}^d$ is the dense contextual embedding representation of the job description.

Let $C_i = \{S_{C_i}, E_{C_i}, P_{C_i}, D_{C_i}\}$ denote candidate resume $i$, where:
- $S_{C_i}$ is the set of normalized canonical skills extracted from candidate $i$.
- $E_{C_i}$ is the computed relevant professional experience in years.
- $P_{C_i}$ is the extracted project portfolio.
- $D_{C_i} \in \mathbb{R}^d$ is the dense contextual embedding representation of the candidate resume.

---

## 2. Hybrid Scoring Formulation

The overall match score $\mathcal{M}(C_i, J) \in [0, 100]$ is computed as:

$$\mathcal{M}(C_i, J) = 100 \times \sum_{k=1}^5 w_k \cdot \phi_k(C_i, J)$$

Subject to the convex weighting constraint:
$$\sum_{k=1}^5 w_k = 1.0, \quad w_k \ge 0 \quad \forall k \in \{1, \dots, 5\}$$

### Component Scoring Functions:

1. **Required Skill Coverage ($\phi_1$)**:
   $$\phi_1(C_i, J) = \frac{|S_{C_i} \cap S_{\text{req}}|}{|S_{\text{req}}| + \epsilon}$$
   Measures the exact proportion of mandatory technical proficiencies satisfied by the candidate.

2. **Preferred Skill Coverage ($\phi_2$)**:
   $$\phi_2(C_i, J) = \begin{cases} 
   \frac{|S_{C_i} \cap S_{\text{pref}}|}{|S_{\text{pref}}|}, & \text{if } |S_{\text{pref}}| > 0 \\
   1.0, & \text{if } |S_{\text{pref}}| = 0 
   \end{cases}$$
   Measures bonus alignment with desirable but non-exclusionary qualifications.

3. **Dense Contextual Semantic Similarity ($\phi_3$)**:
   $$\phi_3(C_i, J) = \max\left(0, \frac{D_{C_i} \cdot D_J}{\|D_{C_i}\|_2 \cdot \|D_J\|_2}\right)$$
   Dense representations $D_{C_i}, D_J \in \mathbb{R}^{384}$ are generated using the pretrained `all-MiniLM-L6-v2` Sentence Transformer. Captures semantic phrasing, synonymous domain experience, and conceptual vocabulary overlap beyond exact keyword matches.

4. **Experience Evidence Alignment ($\phi_4$)**:
   $$\phi_4(C_i, J) = \min\left(1.0, \frac{E_{C_i}}{E_{\text{min}} + \epsilon}\right)$$
   Penalizes candidates with less than the minimum requested duration while capping the benefit at 1.0 to prevent age/tenure over-indexing.

5. **Project Evidence Scope ($\phi_5$)**:
   $$\phi_5(C_i, J) = \min\left(1.0, \frac{|P_{C_i}|}{2.0}\right) \times \left(0.5 + 0.5 \cdot \frac{|\text{Tech}(P_{C_i}) \cap (S_{\text{req}} \cup S_{\text{pref}})|}{\max(1, |\text{Tech}(P_{C_i})|)}\right)$$
   Verifies hands-on project artifacts and their technical overlap with role requirements.

---

## 3. Algorithm Selection & Trade-Off Matrix

| Technique | Chosen Approach | Alternative Considered | Engineering Rationale |
|---|---|---|---|
| **Text Extraction** | `pypdf` + `python-docx` | `PyPDF2` (legacy), Tesseract OCR only | `pypdf` is fast, pure-Python, zero external system binary dependencies; robust fallback on malformed streams. |
| **Skill Normalization** | Hierarchical Canonical Taxonomy + Lemmatized Regex Alias Lookup | Unconstrained LLM Named Entity Recognition (NER) | LLMs hallucinate skills not present in text and cost substantial latency. Curated taxonomy ensures 100% deterministic, audit-proof canonicalization. |
| **Semantic Matching** | Sentence Transformers (`all-MiniLM-L6-v2`) | Bag-of-Words, Word2Vec, BERT-base | `all-MiniLM-L6-v2` offers 5x faster inference than BERT-base with 99.2% retained semantic ranking quality on benchmark tasks. |
| **Supervised Baseline** | TF-IDF n-gram (1-3) + Logistic Regression / SGD | End-to-end Deep Neural Net from scratch | Small hiring datasets cause deep networks to overfit rapidly. Linear baselines with L2 regularization provide calibrated decision boundaries and interpretable coefficients. |
| **Recommendation** | Cosine Similarity in Skill-Vector Space + Role Trajectory Graph | Pure Collaborative Filtering (User-Item Matrix) | Cold-start problem: resumes and job postings arrive continuously with zero prior historical interactions. Content-based skill gap analysis solves cold-start immediately. |
