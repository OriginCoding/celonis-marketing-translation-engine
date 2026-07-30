import re
from bs4 import BeautifulSoup, NavigableString
from app.models import GlossaryItem
from app.core.llm_provider import LLMProvider
from typing import List, Tuple

TRANSLATABLE_ATTRIBUTES = [
    "placeholder", "alt", "title", "aria-label", 
    "aria-description", "aria-placeholder", "aria-roledescription"
]

PARAGRAPH_TAGS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th", "div", "blockquote", "figcaption"]

class TranslationAgent:
    """
    Context-Aware HTML Translation Agent powered by LLMProvider.
    Translates paragraph blocks as complete semantic units while preserving 100% of DOM AST tags, links, and structure.
    Preserves whitespace boundaries and enforces strict glossary term replacement.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.llm_provider = LLMProvider(model_name=model_name, temperature=0.2)
        self.last_prompt_payloads = []

    def _translate_block(
        self,
        text: str,
        dnt_terms: List[str],
        inject_error: bool
    ) -> str:
        """Translates a text block, splitting by linebreaks if multi-paragraph text is provided."""
        text = re.sub(r"\s+([,\.;:\?!])", r"\1", text)

        if "\n" in text:
            lines = text.split("\n")
            translated_lines = []
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    translated_lines.append(line)
                else:
                    llm_res = self.llm_provider.generate_translation(
                        source_text=stripped,
                        dnt_terms=dnt_terms,
                        target_lang="Spanish (es-ES)",
                        inject_error=inject_error
                    )
                    self.last_prompt_payloads.append(llm_res.prompt_payload.model_dump())
                    leading = line[:len(line) - len(line.lstrip())]
                    trailing = line[len(line.rstrip()):]
                    translated_lines.append(f"{leading}{llm_res.raw_output}{trailing}")
            return "\n".join(translated_lines)
        else:
            llm_res = self.llm_provider.generate_translation(
                source_text=text,
                dnt_terms=dnt_terms,
                target_lang="Spanish (es-ES)",
                inject_error=inject_error
            )
            self.last_prompt_payloads.append(llm_res.prompt_payload.model_dump())
            return llm_res.raw_output

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

        # 2. Block-Level Semantic Translation for Leaf Paragraph Elements (p, h1-h6, li, div, td, th)
        for tag_name in PARAGRAPH_TAGS:
            for p_tag in soup.find_all(tag_name):
                # Skip container tags that contain child block elements
                if any(child.name in PARAGRAPH_TAGS for child in p_tag.find_all(True)):
                    continue

                full_text = p_tag.get_text(separator=" ", strip=True)
                full_text = re.sub(r"\s+([,\.;:\?!])", r"\1", full_text)
                if not full_text:
                    continue

                anchors = p_tag.find_all("a")
                if anchors:
                    for a in anchors:
                        a_text = a.get_text(strip=True)
                        if a_text:
                            a_translated = self._translate_block(a_text, dnt_terms, inject_error)
                            a.string = a_translated
                    
                    for elem in p_tag.find_all(string=True):
                        if elem.parent and elem.parent.name == "a":
                            continue
                        elem_str = str(elem)
                        elem_text = elem_str.strip()
                        if elem_text:
                            leading_space = " " if elem_str.startswith((" ", "\t", "\r", "\n")) else ""
                            trailing_space = " " if elem_str.endswith((" ", "\t", "\r", "\n")) else ""
                            t_text = self._translate_block(elem_text, dnt_terms, inject_error)
                            elem.replace_with(f"{leading_space}{t_text}{trailing_space}")
                else:
                    translated_p = self._translate_block(full_text, dnt_terms, inject_error)
                    p_tag.string = translated_p

        # 3. Translate any remaining standalone string nodes outside paragraph tags
        for element in soup.find_all(string=True):
            if element.parent and element.parent.name in ["script", "style", "meta", "head", "title"]:
                continue
            if element.parent and element.parent.name in PARAGRAPH_TAGS:
                continue

            original_str = str(element)
            text = original_str.strip()
            if not text:
                continue

            leading_space = " " if original_str.startswith((" ", "\t", "\r", "\n")) else ""
            trailing_space = " " if original_str.endswith((" ", "\t", "\r", "\n")) else ""

            translated_text = self._translate_block(text, dnt_terms, inject_error)
            replacement = f"{leading_space}{translated_text}{trailing_space}"
            element.replace_with(replacement)

        # 4. Handle title tag separately
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title_text = title_tag.string.strip()
            translated_title = self._translate_block(title_text, dnt_terms, inject_error)
            title_tag.string.replace_with(translated_title)

        output_html = str(soup).strip()

        # 5. Strict Post-Processing Sweep: Enforce non-DNT glossary terms while protecting DNT terms
        dnt_protected = {}
        sorted_dnt = sorted(dnt_terms, key=len, reverse=True)
        for idx, dnt in enumerate(sorted_dnt):
            placeholder = f"__DNT_POST_PROTECT_{idx}__"
            pattern = re.compile(r"\b" + re.escape(dnt) + r"\b")
            if pattern.search(output_html):
                output_html = pattern.sub(placeholder, output_html)
                dnt_protected[placeholder] = dnt

        for g_item in non_dnt_glossary:
            pattern = re.compile(r"\b" + re.escape(g_item.term_en) + r"\b", re.IGNORECASE)
            output_html = pattern.sub(g_item.term_es, output_html)

        for placeholder, original_dnt in dnt_protected.items():
            output_html = output_html.replace(placeholder, original_dnt)

        if output_html.startswith("html\n") or output_html.startswith("html\r\n"):
            output_html = output_html[4:].strip()

        return output_html, self.last_prompt_payloads
