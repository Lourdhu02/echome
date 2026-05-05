from pydantic import BaseModel
from typing import Dict, List, Optional

class QuestionItem(BaseModel):
    item_id: str
    dimension: str
    text: str
    a: float
    b: List[float]

class TraitState(BaseModel):
    theta: float = 0.0
    se: float = 1.0
    answered_items: List[str] = []
    responses: Dict[str, int] = {}

class AssessmentProfile(BaseModel):
    traits: Dict[str, float]
    percentiles: Dict[str, float]
    archetype: str
    behavioral_predictions: List[str]
