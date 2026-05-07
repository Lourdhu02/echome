from typing import Dict, List
from scipy.stats import norm

from src.models import AssessmentProfile

def generate_profile(traits: Dict[str, float]) -> AssessmentProfile:
    """
    Generates an assessment profile from raw latent trait estimates.

    Args:
        traits (Dict[str, float]): A dictionary mapping dimension names to theta values.

    Returns:
        AssessmentProfile: The fully populated assessment profile.
    """
    percentiles: Dict[str, float] = {}
    for dim, theta in traits.items():
        # Convert standard normal theta to percentile (0-100)
        percentiles[dim] = float(norm.cdf(theta)) * 100.0

    # Determine archetype based on percentiles
    archetype = "The Generalist"
    is_conscientious = percentiles.get("BigFive_C", 50.0) > 75.0
    is_analytical = percentiles.get("Cognitive", 50.0) > 75.0
    is_extroverted = percentiles.get("BigFive_E", 50.0) > 75.0

    if is_conscientious and is_analytical:
        archetype = "The Focused Engineer"
    elif is_extroverted:
        archetype = "The Communicator"

    # Generate behavioral predictions
    behavioral_predictions: List[str] = []
    
    if percentiles.get("BigFive_C", 50.0) > 60.0:
        behavioral_predictions.append("Prefers highly structured and planned tasks.")
    else:
        behavioral_predictions.append("Thrives in open-ended, spontaneous environments.")

    if percentiles.get("Cognitive", 50.0) > 50.0:
        behavioral_predictions.append("Likely to adopt a deeply analytical problem-solving approach.")
    else:
        behavioral_predictions.append("Tends to rely on intuition and holistic reasoning.")

    return AssessmentProfile(
        traits=traits,
        percentiles=percentiles,
        archetype=archetype,
        behavioral_predictions=behavioral_predictions
    )
