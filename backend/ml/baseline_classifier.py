import os
import joblib
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


class BaselineRelevanceClassifier:
    """
    Supervised Machine Learning Baseline:
    TF-IDF (1-2 n-grams) + L2 Regularized Logistic Regression.
    Predicts binary candidate-job relevance:
    1 = Qualified / Recommended for Human Review
    0 = Does Not Meet Criteria
    """

    def __init__(self, model_path: str = "./models/baseline_relevance.joblib"):
        self.model_path = model_path
        self.pipeline: Pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=3000, stop_words="english")),
            ("clf", LogisticRegression(C=1.0, solver="liblinear", random_state=42))
        ])
        self.is_trained = False
        self._load_if_exists()

    def _load_if_exists(self):
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                self.is_trained = True
            except Exception as e:
                print(f"[TalentLens AI] Warning: Could not load baseline model from {self.model_path}: {e}")

    def train(self, texts: list[str], labels: list[int]) -> Dict[str, Any]:
        """Trains the pipeline on paired texts and evaluates training metrics."""
        self.pipeline.fit(texts, labels)
        self.is_trained = True

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.pipeline, self.model_path)

        preds = self.pipeline.predict(texts)
        probs = self.pipeline.predict_proba(texts)[:, 1]

        return {
            "train_samples": len(texts),
            "precision": float(precision_score(labels, preds, zero_division=0)),
            "recall": float(recall_score(labels, preds, zero_division=0)),
            "f1_score": float(f1_score(labels, preds, zero_division=0)),
            "roc_auc": float(roc_auc_score(labels, probs)) if len(set(labels)) > 1 else 1.0,
        }

    def evaluate(self, test_texts: list[str], test_labels: list[int]) -> Dict[str, Any]:
        """Evaluates model performance on held-out test data."""
        if not self.is_trained:
            raise RuntimeError("Model is not trained. Train the model first.")

        preds = self.pipeline.predict(test_texts)
        probs = self.pipeline.predict_proba(test_texts)[:, 1]

        cm = confusion_matrix(test_labels, preds).tolist()

        return {
            "test_samples": len(test_texts),
            "precision": round(float(precision_score(test_labels, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(test_labels, preds, zero_division=0)), 4),
            "f1_score": round(float(f1_score(test_labels, preds, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(test_labels, probs)), 4) if len(set(test_labels)) > 1 else 1.0,
            "confusion_matrix": cm,
            "classification_report": classification_report(test_labels, preds, output_dict=True, zero_division=0),
        }

    def predict_relevance(self, resume_text: str, job_text: str) -> Tuple[int, float]:
        """
        Combines resume and job text and returns (prediction, calibrated_probability).
        """
        combined = f"{resume_text} [SEP] {job_text}"
        if not self.is_trained:
            return 1, 0.5  # Neutral untrained prior

        pred = int(self.pipeline.predict([combined])[0])
        prob = float(self.pipeline.predict_proba([combined])[0][1])
        return pred, round(prob, 4)
