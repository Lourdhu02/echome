from pydantic import BaseModel, Field
from typing import Dict, List

class QuestionItem(BaseModel):
    """Represents a question item in the Graded Response Model."""
    item_id: str = Field(..., description="Unique identifier for the item")
    dimension: str = Field(..., description="The latent trait dimension this item measures")
    text: str = Field(..., description="The text of the question")
    a: float = Field(..., description="Item discrimination parameter")
    b: List[float] = Field(..., description="Item difficulty thresholds")

class TraitState(BaseModel):
    """Maintains the state of a latent trait estimation during assessment."""
    theta: float = Field(default=0.0, description="Current estimate of the latent trait")
    se: float = Field(default=1.0, description="Standard error of the current estimate")
    answered_items: List[str] = Field(default_factory=list, description="List of answered item IDs")
    responses: Dict[str, int] = Field(default_factory=dict, description="Mapping of item ID to selected category")

class AssessmentProfile(BaseModel):
    """The final generated profile after assessment completion."""
    traits: Dict[str, float] = Field(..., description="Raw theta estimates for each dimension")
    percentiles: Dict[str, float] = Field(..., description="Percentile scores for each dimension")
    archetype: str = Field(..., description="The computed user archetype")
    behavioral_predictions: List[str] = Field(..., description="Predicted behavioral tendencies")
