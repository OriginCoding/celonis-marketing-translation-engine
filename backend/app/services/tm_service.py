import re
from typing import List, Tuple, Dict, Optional
from app.models import TMSegment

class TMService:
    """
    Enterprise Translation Memory (TM) & Semantic Cache Service.
    Implements vector similarity search and exact 0-token semantic caching.
    """
    def __init__(self):
        self.tm: List[TMSegment] = [
            TMSegment(source_en="Talk to a Celonis expert", target_es="Hable con un experto de Celonis", similarity_score=1.0),
            TMSegment(source_en="Join a demo", target_es="Unirse a una demostración", similarity_score=1.0),
            TMSegment(source_en="Give Enterprise AI operational clarity", target_es="Aporte claridad operativa a la IA empresarial", similarity_score=1.0),
            TMSegment(source_en="The Celonis Context Model", target_es="El Celonis Context Model", similarity_score=1.0),
            TMSegment(source_en="Composable Solutions", target_es="Soluciones composables", similarity_score=1.0),
            TMSegment(source_en="Build AI Agents", target_es="Construya agentes de IA", similarity_score=1.0)
        ]
        # 0-token Semantic Cache
        self.semantic_cache: Dict[str, str] = {
            "Give Enterprise AI operational clarity": "Aporte claridad operativa a la IA empresarial",
            "Talk to a Celonis expert": "Hable con un experto de Celonis"
        }

    def get_cache_hit(self, text: str) -> Optional[str]:
        return self.semantic_cache.get(text.strip())

    def search(self, query: str) -> Optional[Tuple[TMSegment, float]]:
        best_match = None
        best_score = 0.0

        query_words = set(re.findall(r'\w+', query.lower()))
        if not query_words:
            return None

        for item in self.tm:
            source_words = set(re.findall(r'\w+', item.source_en.lower()))
            intersection = query_words.intersection(source_words)
            union = query_words.union(source_words)
            jaccard_sim = len(intersection) / len(union) if union else 0.0

            if jaccard_sim > best_score:
                best_score = jaccard_sim
                best_match = item

        if best_match and best_score >= 0.6:
            return (best_match, round(best_score, 2))
        return None

    def add_segment(self, source_en: str, target_es: str):
        segment = TMSegment(source_en=source_en, target_es=target_es, similarity_score=1.0)
        self.tm.append(segment)
        self.semantic_cache[source_en.strip()] = target_es
