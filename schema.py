from pydantic import BaseModel
from typing import Dict, Optional

class LegalQuery(BaseModel):
    user_input: str
    feedback: Optional[str] = None

class LegalResponse(BaseModel):
    domain: str
    confidence: float
    legal_route: str
    timeline: str
    outcome: str
    process_steps: str
    glossary: Dict[str, str]