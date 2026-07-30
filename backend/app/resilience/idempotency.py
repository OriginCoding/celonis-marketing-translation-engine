import time
from typing import Dict, Any, Optional

class IdempotencyManager:
    """
    100% Free & Open-Source Idempotency Key Manager.
    Prevents duplicate execution on network retries by tracking X-Idempotency-Key headers.
    """

    def __init__(self, ttl_seconds: int = 86400):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def check_key(self, idempotency_key: str) -> Optional[Dict[str, Any]]:
        """Returns cached result if idempotency key exists and is valid."""
        if not idempotency_key:
            return None
        
        entry = self.cache.get(idempotency_key)
        if entry:
            if time.time() - entry["timestamp"] < self.ttl_seconds:
                return entry["response"]
            else:
                del self.cache[idempotency_key]
        return None

    def record_key(self, idempotency_key: str, response: Dict[str, Any]):
        """Records completed job response against idempotency key."""
        if idempotency_key:
            self.cache[idempotency_key] = {
                "response": response,
                "timestamp": time.time()
            }
