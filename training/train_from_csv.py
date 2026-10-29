"""
TalentLens AI — Train & Evaluate Supervised Baseline Model from CSV.
Reads: datasets/talentlens_evaluation_dataset.csv
Evaluates:
- Binary Relevance Classification (Qualified vs Not Qualified)
- Information Retrieval Ranking (NDCG@K, Precision@K, MRR)
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix


def run_csv_evaluation():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "talentlens_evaluation_dataset.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV dataset not found at {csv_path}")

    df = pd.read_csv(csv_path)
    print("=" * 65)
    print(" TalentLens AI — CSV Benchmark Model Evaluation")
    print("=" * 65)
    print(f"Total screening pairs loaded: {len(df)}")
    print(f"Unique job roles: {df['job_title'].nunique()}")
    print(f"Domains: {', '.join(df['job_department'].unique())}")
    print("-" * 65)

    # 1. Split by predefined train / test partitions
    train_df = df[df["evaluation_split"] == "train"].copy()
    test_df = df[df["evaluation_split"] == "test"].copy()

    print(f"Training split samples: {len(train_df)}")
    print(f"Testing split samples:  {len(test_df)}")

    # 2. Textual Features: Candidate Resume Summary + Extracted Skills vs Job Description
    X_train_text = train_df["resume_summary"] + " [SKILLS] " + train_df["extracted_skills"]
    y_train = train_df["ground_truth_relevance"].values

    X_test_text = test_df["resume_summary"] + " [SKILLS] " + test_df["extracted_skills"]
    y_test = test_df["ground_truth_relevance"].values

    # 3. TF-IDF + Logistic Regression Classifier
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=500)
    X_train_vec = vectorizer.fit_transform(X_train_text)
    X_test_vec = vectorizer.transform(X_test_text)

    clf = LogisticRegression(random_state=42, class_weight="balanced")
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    y_prob = clf.predict_proba(X_test_vec)[:, 1]

    print("\n--- Supervised Relevance Classification Report (Held-out Test) ---")
    print(classification_report(y_test, y_pred, target_names=["Not Qualified (0)", "Qualified (1)"]))

    roc_auc = roc_auc_score(y_test, y_prob)
    print(f"ROC-AUC Score: {roc_auc:.4f}")

    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")

    # 4. IR Ranking Metric: NDCG@3 Comparison on the Test set
    print("\n--- Information Retrieval Ranking (NDCG@3 Benchmark) ---")
    
    def dcg_at_k(r, k=3):
        r = np.asarray(r, dtype=float)[:k]
        if r.size:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        return 0.0

    def ndcg_at_k(r, k=3):
        dcg_max = dcg_at_k(sorted(r, reverse=True), k)
        if not dcg_max:
            return 1.0
        return dcg_at_k(r, k) / dcg_max

    test_grades = test_df["ranking_relevance_grade"].tolist()
    hybrid_scores = test_df["overall_match_score"].tolist()
    semantic_scores = test_df["semantic_similarity_score"].tolist()
    keyword_scores = test_df["required_skill_coverage_ratio"].tolist()

    # Sort test set by hybrid score
    hybrid_order = [g for _, g in sorted(zip(hybrid_scores, test_grades), reverse=True)]
    semantic_order = [g for _, g in sorted(zip(semantic_scores, test_grades), reverse=True)]
    keyword_order = [g for _, g in sorted(zip(keyword_scores, test_grades), reverse=True)]

    print(f"TalentLens Hybrid Model NDCG@3: {ndcg_at_k(hybrid_order, k=3):.4f}")
    print(f"Dense Semantic Model NDCG@3:    {ndcg_at_k(semantic_order, k=3):.4f}")
    print(f"Pure Keyword Model NDCG@3:      {ndcg_at_k(keyword_order, k=3):.4f}")
    print("=" * 65)


if __name__ == "__main__":
    run_csv_evaluation()
