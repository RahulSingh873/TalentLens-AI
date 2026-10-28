import os
import numpy as np
from typing import List, Union, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingEngine:
    """
    Embedding Engine with primary local SentenceTransformer dense inference
    and transparent, explainable TF-IDF n-gram cosine similarity fallback.
    """
    def __init__(self):
        self._model = None
        self._attempted_load = False
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self._load_model()

    def _load_model(self):
        if self._attempted_load:
            return
        self._attempted_load = True

        local_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "models", "minilm")
        )

        if os.path.exists(local_dir):
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(local_dir)
                self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
                return
            except Exception as e:
                print(f"[TalentLens AI] Dense model load error: {e}")

        # Explicit fallback
        self._model = None
        self.model_name = "tfidf-ngram-cosine"

    def compute_similarity(self, text_a: str, text_b: str) -> Tuple[float, str]:
        """
        Computes cosine similarity between two texts.
        Returns (similarity_score, model_used).
        """
        if not text_a.strip() or not text_b.strip():
            return 0.0, self.model_name

        if self._model is not None:
            try:
                embeddings = self._model.encode([text_a, text_b], convert_to_numpy=True, normalize_embeddings=True)
                score = float(np.dot(embeddings[0], embeddings[1]))
                return max(0.0, min(1.0, score)), self.model_name
            except Exception:
                pass

        # TF-IDF N-gram Cosine Similarity Fallback
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=5000)
        try:
            tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
            sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
            return max(0.0, min(1.0, sim)), "tfidf-ngram-cosine"
        except Exception:
            return 0.0, "tfidf-ngram-cosine"

    def encode_text(self, text: str) -> np.ndarray:
        """Encodes single text into dense vector."""
        if self._model is not None:
            return self._model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return np.zeros(384, dtype=np.float32)


# Global singleton instance
embedding_engine = EmbeddingEngine()
