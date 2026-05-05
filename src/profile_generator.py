from typing import Dict, List
from scipy.stats import norm
from src.models import AssessmentProfile

def generate_profile(traits: Dict[str, float]) -> AssessmentProfile:
    percentiles = {}
    for dim, theta in traits.items():
        percentiles[dim] = float(norm.cdf(theta)) * 100.0

    archetype = "The Generalist"
    if percentiles.get("BigFive_C", 50) > 75 and percentiles.get("Cognitive", 50) > 75:
        archetype = "The Focused Engineer"
    elif percentiles.get("BigFive_E", 50) > 75:
        archetype = "The Communicator"

    behavioral_predictions = [
        "Prefers structured tasks" if percentiles.get("BigFive_C", 50) > 60 else "Prefers open-ended tasks",
        "Likely to adopt analytical approach" if percentiles.get("Cognitive", 50) > 50 else "Likely to adopt intuitive approach"
    ]

    return AssessmentProfile(
        traits=traits,
        percentiles=percentiles,
        archetype=archetype,
        behavioral_predictions=behavioral_predictions
    )
