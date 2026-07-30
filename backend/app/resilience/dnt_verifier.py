import re
from typing import List, Tuple
from app.models import GlossaryItem

class DntVerifier:
    @staticmethod
    def verify(source_html: str, translated_html: str, glossary: List[GlossaryItem]) -> Tuple[List[str], List[str], float]:
        dnt_violations = []
        glossary_violations = []

        dnt_terms = [item for item in glossary if item.dnt]
        for dnt in dnt_terms:
            term = dnt.term_en
            if re.search(r'\b' + re.escape(term) + r'\b', source_html, re.IGNORECASE):
                if not re.search(r'\b' + re.escape(term) + r'\b', translated_html):
                    dnt_violations.append(f"DNT term '{term}' missing or translated in output text.")

        forbidden_loanwords = {
            "lead": "prospecto",
            "webinar": "seminario web",
            "landing page": "página de destino",
            "engagement": "participación",
            "customer journey": "recorrido del cliente",
            "newsletter": "boletín de noticias"
        }

        for loanword, replacement in forbidden_loanwords.items():
            if re.search(r'\b' + re.escape(loanword) + r'\b', translated_html, re.IGNORECASE):
                glossary_violations.append(f"Used loanword '{loanword}' instead of approved Spanish term '{replacement}'.")

        # 100 base score, -25 per DNT violation, -10 per glossary violation
        score = max(0.0, 100.0 - (len(dnt_violations) * 25.0) - (len(glossary_violations) * 10.0))
        return dnt_violations, glossary_violations, score
