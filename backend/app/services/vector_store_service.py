import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from ..data.roles_taxonomy import TECH_ROLES_DATASET
from ..schemas.role_match import RoleArchetype
from .embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class VectorStoreService:
    """
    Manages ChromaDB vector indexing and similarity retrieval for Career Roles & Job Profiles.
    """

    COLLECTION_NAME = "tech_role_archetypes"

    def __init__(self, embedding_service: Optional[EmbeddingService] = None):
        self.embedding_service = embedding_service or EmbeddingService()
        
        self.chroma_client = chromadb.Client(
            ChromaSettings(
                anonymized_telemetry=False,
                is_persistent=False
            )
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "Standard tech roles and requirements taxonomy", "hnsw:space": "cosine"}
        )
        
        self._seed_roles()

    def _seed_roles(self):
        """
        Indexes all predefined role archetypes into ChromaDB.
        """
        existing_count = self.collection.count()
        if existing_count > 0:
            return

        documents = []
        metadatas = []
        ids = []

        for role in TECH_ROLES_DATASET:
            doc_text = (
                f"{role.title} {role.category} "
                f"{role.description} "
                f"Required: {' '.join(role.required_skills)} "
                f"Preferred: {' '.join(role.preferred_skills)} "
                f"Tools: {' '.join(role.typical_tools)}"
            )
            documents.append(doc_text)
            ids.append(role.id)
            metadatas.append({
                "role_id": role.id,
                "title": role.title,
                "category": role.category,
                "market_demand": role.market_demand,
                "salary_range": role.average_salary_range
            })

        embeddings = self.embedding_service.get_batch_embeddings(documents)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"Successfully seeded {len(ids)} tech roles into ChromaDB vector store.")

    def search_matching_roles(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches ChromaDB for the closest role archetypes matching the candidate's query representation.
        Returns a list of dicts with role and calibrated similarity score (0.0 to 100.0).
        """
        query_embedding = self.embedding_service.get_embedding(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, len(TECH_ROLES_DATASET)),
            include=["metadatas", "distances", "documents"]
        )

        matches = []
        if results and "ids" in results and results["ids"]:
            matched_ids = results["ids"][0]
            distances = results["distances"][0] if "distances" in results else [0.0] * len(matched_ids)

            for role_id, dist in zip(matched_ids, distances):
                # Cosine distance in Chroma: dist = 1 - cos_sim
                # cos_sim = 1 - dist
                raw_cos = max(0.0, min(1.0, 1.0 - dist))
                
                # Calibrate: cosine similarities typically range 0.2 to 0.8 in bag-of-words/dense spaces
                # Map raw_cos [0.1, 0.7] -> [40%, 95%]
                calibrated = min(100.0, max(20.0, (raw_cos ** 0.5) * 100.0))
                
                role_obj = next((r for r in TECH_ROLES_DATASET if r.id == role_id), None)
                if role_obj:
                    matches.append({
                        "role": role_obj,
                        "similarity_score": round(calibrated, 1)
                    })

        return matches
