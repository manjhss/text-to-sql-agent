from diskcache import Cache as d_cache

from src.config.logger import logger

# in production, use a vector db (ChromaDB, Pinecone, etc.)


class Cache:
    "manages cache connections"

    def __init__(self):
        self.cache = d_cache("./storage")

    def startup(self):
        """run a cheap query to check cache connection"""

        try:
            self.cache.get("test")
            logger.info("cache connection ok")
        except Exception:
            logger.exception("cache startup failed")
            raise

    def dispose(self):
        """dispose cache connection"""

        self.cache.close()
        logger.info("cache connection disposed")


cache = Cache()
