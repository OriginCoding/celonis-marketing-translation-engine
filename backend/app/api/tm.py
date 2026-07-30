from fastapi import APIRouter
from typing import List
from app.models import TMSegment, GlossaryItem
from app.services.glossary_service import GlossaryService
from app.services.tm_service import TMService

router = APIRouter(prefix="/api/tm", tags=["Translation Memory & Glossary"])
glossary_service = GlossaryService()
tm_service = TMService()

@router.get("/glossary", response_model=List[GlossaryItem])
def get_glossary():
    return glossary_service.get_all()

@router.get("/memory", response_model=List[TMSegment])
def get_translation_memory():
    return tm_service.tm
