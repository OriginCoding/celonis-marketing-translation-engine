from typing import List
from app.models import GlossaryItem

DEFAULT_GLOSSARY: List[GlossaryItem] = [
    GlossaryItem(term_en="AI", term_es="IA", dnt=False, notes="Abbreviate as IA in running text"),
    GlossaryItem(term_en="Artificial Intelligence", term_es="Inteligencia artificial", dnt=False, notes="Full form of IA"),
    GlossaryItem(term_en="Agent", term_es="Agente", dnt=False, notes="Generic term; see Agent C for product name"),
    GlossaryItem(term_en="Agent C", term_es="Agent C", dnt=True, notes="Celonis product name, never translate"),
    GlossaryItem(term_en="Brand", term_es="Marca", dnt=False, notes=""),
    GlossaryItem(term_en="Brand tone", term_es="Tono de marca", dnt=False, notes=""),
    GlossaryItem(term_en="Call-to-action", term_es="Llamada a la acción", dnt=False, notes="Short form CTA is acceptable"),
    GlossaryItem(term_en="Campaign", term_es="Campaña", dnt=False, notes=""),
    GlossaryItem(term_en="Celonis", term_es="Celonis", dnt=True, notes="Company and product name, never translate"),
    GlossaryItem(term_en="Celonis Process Intelligence", term_es="Celonis Process Intelligence", dnt=True, notes="Full product name"),
    GlossaryItem(term_en="Confidence score", term_es="Puntuación de confianza", dnt=False, notes=""),
    GlossaryItem(term_en="Content", term_es="Contenido", dnt=False, notes=""),
    GlossaryItem(term_en="Conversion Rate", term_es="Tasa de conversión", dnt=False, notes=""),
    GlossaryItem(term_en="CTA", term_es="CTA", dnt=True, notes="Abbreviation, keep as-is"),
    GlossaryItem(term_en="Customer journey", term_es="Recorrido del cliente", dnt=False, notes="Do not use 'customer journey' in Spanish text"),
    GlossaryItem(term_en="Engagement", term_es="Participación", dnt=False, notes="Do not use 'engagement' as a loanword"),
    GlossaryItem(term_en="Glossary", term_es="Glosario", dnt=False, notes=""),
    GlossaryItem(term_en="Landing page", term_es="Página de destino", dnt=False, notes="Do not use 'landing page' in Spanish text"),
    GlossaryItem(term_en="Lead", term_es="Prospecto", dnt=False, notes="Use 'prospecto', not 'lead'"),
    GlossaryItem(term_en="MCP", term_es="MCP", dnt=True, notes="Technical abbreviation, keep as-is"),
    GlossaryItem(term_en="Newsletter", term_es="Boletín de noticias", dnt=False, notes="Do not use 'newsletter' in Spanish text"),
    GlossaryItem(term_en="Pipeline", term_es="Canal de ventas", dnt=False, notes="Use 'canal de ventas' in marketing context"),
    GlossaryItem(term_en="Process Intelligence", term_es="Process Intelligence", dnt=True, notes="Celonis product category name"),
    GlossaryItem(term_en="Quality gate", term_es="Control de calidad", dnt=False, notes=""),
    GlossaryItem(term_en="ROI", term_es="ROI", dnt=True, notes="Abbreviation, keep as-is"),
    GlossaryItem(term_en="Skill", term_es="Skill", dnt=True, notes="AI agent component term, keep as-is"),
    GlossaryItem(term_en="Touchpoint", term_es="Punto de contacto", dnt=False, notes=""),
    GlossaryItem(term_en="Translation memory", term_es="Memoria de traducción", dnt=False, notes=""),
    GlossaryItem(term_en="Webinar", term_es="Seminario web", dnt=False, notes="Use 'seminario web', not 'webinar'"),
    GlossaryItem(term_en="Workflow", term_es="Flujo de trabajo", dnt=False, notes="")
]

class GlossaryService:
    def __init__(self):
        self.glossary = DEFAULT_GLOSSARY

    def get_all(self) -> List[GlossaryItem]:
        return self.glossary

    def get_dnt_terms(self) -> List[GlossaryItem]:
        return [item for item in self.glossary if item.dnt]
