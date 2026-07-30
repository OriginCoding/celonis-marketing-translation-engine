import re
from typing import List, Tuple
from bs4 import BeautifulSoup

class HtmlGuardrail:
    @staticmethod
    def validate(source_html: str, translated_html: str) -> Tuple[bool, float, List[str]]:
        issues = []
        penalty = 0.0

        source_soup = BeautifulSoup(source_html, "html.parser")
        trans_soup = BeautifulSoup(translated_html, "html.parser")

        tags_to_check = ["h1", "h2", "h3", "a", "p", "li", "blockquote", "img"]
        for tag in tags_to_check:
            src_count = len(source_soup.find_all(tag))
            trans_count = len(trans_soup.find_all(tag))
            if src_count != trans_count:
                issues.append(f"Tag <{tag}> count mismatch: source has {src_count}, translation has {trans_count}")
                penalty += 15.0

        # Link URL preservation check
        src_links = [a.get("href") for a in source_soup.find_all("a") if a.get("href")]
        trans_links = [a.get("href") for a in trans_soup.find_all("a") if a.get("href")]
        if src_links != trans_links:
            issues.append("Hyperlink href attributes modified or missing in translated text.")
            penalty += 20.0

        score = max(0.0, 100.0 - penalty)
        return (len(issues) == 0, score, issues)
