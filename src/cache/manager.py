import uuid
from typing import Any, cast

import numpy as np
from diskcache import Cache
from ollama import Client

from src.config.logger import logger
from src.config.settings import settings

# in production, use a vector db (ChromaDB, Pinecone, etc.)


class CacheManager:
    "manages cache connections and operations"

    def __init__(self):
        self.cache = Cache("./storage")
        self.ollama_client = Client(host=settings.ollama_host)
        self.threshold = settings.cache_similarity_threshold

    def startup(self):
        """run a cheap query to check cache connection"""

        try:
            self.cache.get("test")
            logger.info("cache connection ok")
        except Exception:
            logger.exception("cache startup failed")
            raise

    def _create_embedding(self, text: str) -> np.ndarray | None:
        """create embedding for text"""

        try:
            response = self.ollama_client.embeddings(
                model=settings.embedding_model, prompt=text
            )

            embedding = response["embedding"]
            return np.array(embedding)
        except Exception as e:
            logger.error(f"create embedding failed: {e}")

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """calculate cosine similarity between two vectors"""

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def get(self, query: str):
        """retrieve cached result for query"""

        try:
            query_embedding = self._create_embedding(query)
            if query_embedding is None:
                return None

            best_match = None
            best_similarity = 0.0

            for key in self.cache:
                cached_data = cast(dict[str, Any], self.cache[key])  # dict cache data
                cached_data_embedding = np.array(cached_data["embedding"])

                similarity = self._cosine_similarity(
                    query_embedding, cached_data_embedding
                )

                if similarity > best_similarity and similarity >= self.threshold:
                    best_similarity = similarity
                    best_match = cached_data

            if best_match:
                logger.info(f"cache hit (similarity: {best_similarity:.3f})")
                return best_match["result"]
            else:
                logger.info("cache missed!")
                return None

        except Exception as e:
            logger.error(f"retrieve cache failed: {e}")
            return None

    def set(self, query: str, result: dict):
        """store query result in cache"""

        try:
            query_embedding = self._create_embedding(query)

            if query_embedding is None:
                return

            key = str(uuid.uuid4())

            self.cache[key] = {
                "query": query,
                "embedding": query_embedding.tolist(),
                "result": result,
            }

            logger.info("result cached!")

        except Exception:
            logger.exception("set cache failed")

    def dispose(self):
        """dispose cache connection"""

        self.cache.close()
        logger.info("cache connection disposed")


cache_manager = CacheManager()
