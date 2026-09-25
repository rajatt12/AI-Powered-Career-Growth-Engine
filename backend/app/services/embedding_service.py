import logging
import numpy as np
from typing import List, Optional
from sklearn.feature_extraction.text import HashingVectorizer
from ..config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Dual-engine embedding service:
    1. Gemini API Embeddings (`text-embedding-004`) when API key is active.
    2. Deterministic 384-dimensional Local Hashing & Subword Vectorizer
       (Guarantees consistent 384-dim vector space for indexing and querying without state drift).
    """

    VECTOR_DIMENSION = 384

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.gemini_client = None
        if self.api_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Embedding client: {e}")

        # Deterministic 384-dim vectorizer with word and bigram tokens
        self._local_vectorizer = HashingVectorizer(
            n_features=self.VECTOR_DIMENSION,
            ngram_range=(1, 2),
            alternate_sign=False,
            norm='l2'
        )

    def is_gemini_active(self) -> bool:
        return self.gemini_client is not None and bool(self.api_key)

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates a normalized embedding vector for a given text string.
        """
        if self.is_gemini_active():
            try:
                response = self.gemini_client.models.embed_content(
                    model="text-embedding-004",
                    contents=text,
                )
                if response and hasattr(response, "embedding") and response.embedding:
                    vec = np.array(response.embedding.values, dtype=np.float32)
                    norm = np.linalg.norm(vec)
                    if norm > 0:
                        vec = vec / norm
                    return vec.tolist()
            except Exception as e:
                logger.warning(f"Gemini embedding call failed: {e}. Falling back to local vectorizer.")

        # Local Deterministic 384-dim Vectorizer
        sparse_vec = self._local_vectorizer.transform([text])
        dense_vec = sparse_vec.toarray()[0].astype(np.float32)
        norm = np.linalg.norm(dense_vec)
        if norm > 0:
            dense_vec = dense_vec / norm
        return dense_vec.tolist()

    def get_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a batch of text documents.
        """
        if not self.is_gemini_active():
            sparse_matrix = self._local_vectorizer.transform(texts)
            dense_matrix = sparse_matrix.toarray().astype(np.float32)
            norms = np.linalg.norm(dense_matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            dense_matrix = dense_matrix / norms
            return dense_matrix.tolist()

        return [self.get_embedding(t) for t in texts]

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two normalized vectors (returns float between 0.0 and 1.0).
        """
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        
        dot = float(np.dot(a, b))
        norm_a = float(np.linalg.norm(a))
        norm_b = float(np.linalg.norm(b))
        
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
            
        sim = dot / (norm_a * norm_b)
        return float(max(0.0, min(1.0, sim)))
