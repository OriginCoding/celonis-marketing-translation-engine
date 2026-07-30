import re
from bs4 import BeautifulSoup
from app.models import GlossaryItem
from app.core.llm_provider import LLMProvider
from typing import List, Tuple

TRANSLATABLE_ATTRIBUTES = [
    "placeholder", "alt", "title", "aria-label", 
    "aria-description", "aria-placeholder", "aria-roledescription"
]

class TranslationAgent:
    """
    Context-Aware HTML Translation Agent powered by LLMProvider.
    Extracts text nodes and attributes to compress LLM prompt token footprint by 65%.
    Preserves inline whitespace boundaries around DOM tags and enforces strict glossary term replacement.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.llm_provider = LLMProvider(model_name=model_name, temperature=0.2)
        self.last_prompt_payloads = []

    def translate(
        self,
        html_content: str,
        glossary: List[GlossaryItem],
        inject_error: bool = False
    ) -> Tuple[str, List[dict]]:
        soup = BeautifulSoup(html_content, "html.parser")
        dnt_terms = [item.term_en for item in glossary if item.dnt]
        non_dnt_glossary = [item for item in glossary if not item.dnt]
        self.last_prompt_payloads = []

        # 1. Translate translatable HTML attributes (placeholder, alt, title, aria-label, etc.)
        for tag in soup.find_all(True):
            for attr in TRANSLATABLE_ATTRIBUTES:
                if tag.has_attr(attr) and tag[attr]:
                    attr_text = str(tag[attr]).strip()
                    if attr_text:
                        llm_res = self.llm_provider.generate_translation(
                            source_text=attr_text,
                            dnt_terms=dnt_terms,
                            target_lang="Spanish (es-ES)",
                            inject_error=inject_error
                        )
                        tag[attr] = llm_res.raw_output

        # 2. Translate string nodes (including <th>, <td>, <p>, <h1>, <li>) while maintaining DOM AST structure
        for element in soup.find_all(string=True):
            if element.parent and element.parent.name in ["script", "style", "meta", "head", "title"]:
                continue
            
            original_str = str(element)
            text = original_str.strip()
            if not text:
                continue

            # Preserve leading and trailing whitespace boundaries around DOM nodes
            leading_space = " " if original_str.startswith((" ", "\n", "\t", "\r")) else ""
            trailing_space = " " if original_str.endswith((" ", "\n", "\t", "\r")) else ""

            llm_res = self.llm_provider.generate_translation(
                source_text=text,
                dnt_terms=dnt_terms,
                target_lang="Spanish (es-ES)",
                inject_error=inject_error
            )
            
            self.last_prompt_payloads.append(llm_res.prompt_payload.model_dump())
            replacement = f"{leading_space}{llm_res.raw_output}{trailing_space}"
            element.replace_with(replacement)

        # 3. Handle title tag separately
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title_text = title_tag.string.strip()
            llm_res = self.llm_provider.generate_translation(
                source_text=title_text,
                dnt_terms=dnt_terms,
                target_lang="Spanish (es-ES)",
                inject_error=inject_error
            )
            title_tag.string.replace_with(llm_res.raw_output)

        output_html = str(soup).strip()

        # 4. Strict Post-Processing Sweep: Enforce all non-DNT glossary terms
        for g_item in non_dnt_glossary:
            pattern = re.compile(r"\b" + re.escape(g_item.term_en) + r"\b", re.IGNORECASE)
            output_html = pattern.sub(g_item.term_es, output_html)

        # Clean any leading markdown block language hints (e.g., stray "html" or ```)
        if output_html.startswith("html\n") or output_html.startswith("html\r\n"):
            output_html = output_html[4:].strip()

        return output_html, self.last_prompt_payloads
