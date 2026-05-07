import numpy as np
from scipy.optimize import minimize
from typing import List, Dict, Optional

from src.models import QuestionItem, TraitState

def prob_grm(theta: float, a: float, b: List[float], k: int) -> float:
    """
    Calculates the probability of observing category k given theta using GRM.

    Args:
        theta (float): Latent trait value.
        a (float): Item discrimination parameter.
        b (List[float]): Item difficulty thresholds.
        k (int): Selected category index (0 to len(b)).

    Returns:
        float: The probability of selecting category k.
    """
    def p_star(t: float, disc: float, diff: float) -> float:
        return 1.0 / (1.0 + np.exp(-disc * (t - diff)))
    
    if k == 0:
        return 1.0 - p_star(theta, a, b[0])
    elif k == len(b):
        return p_star(theta, a, b[-1])
    else:
        return p_star(theta, a, b[k - 1]) - p_star(theta, a, b[k])

def fisher_information_grm(theta: float, a: float, b: List[float]) -> float:
    """
    Calculates the Fisher Information for a given item in the GRM.

    Args:
        theta (float): Latent trait value.
        a (float): Item discrimination parameter.
        b (List[float]): Item difficulty thresholds.

    Returns:
        float: The expected Fisher Information.
    """
    info = 0.0
    for k in range(len(b) + 1):
        p_k = prob_grm(theta, a, b, k)
        if p_k > 1e-10:
            def p_star(t: float, diff: float) -> float:
                return 1.0 / (1.0 + np.exp(-a * (t - diff)))
            
            p_star_k_minus_1 = p_star(theta, b[k-1]) if k > 0 else 1.0
            p_star_k = p_star(theta, b[k]) if k < len(b) else 0.0
            
            dp_k_dtheta = a * (p_star_k_minus_1 * (1 - p_star_k_minus_1) - p_star_k * (1 - p_star_k))
            info += (dp_k_dtheta ** 2) / p_k
    return info

def estimate_theta_map(responses: Dict[str, int], items: Dict[str, QuestionItem]) -> float:
    """
    Estimates the latent trait (theta) using Maximum A Posteriori (MAP) estimation.

    Args:
        responses (Dict[str, int]): Dictionary mapping item_id to selected category index.
        items (Dict[str, QuestionItem]): Dictionary of items answered.

    Returns:
        float: The estimated latent trait value.
    """
    if not responses:
        return 0.0
        
    def neg_log_posterior(theta_val: np.ndarray) -> float:
        t = float(theta_val[0])
        log_prior = -0.5 * (t ** 2)
        log_likelihood = 0.0
        for item_id, resp in responses.items():
            if item_id not in items:
                continue
            item = items[item_id]
            prob = prob_grm(t, item.a, item.b, resp)
            log_likelihood += np.log(prob + 1e-10)
        return -(log_prior + log_likelihood)
        
    res = minimize(neg_log_posterior, x0=np.array([0.0]), bounds=[(-4.0, 4.0)], method='L-BFGS-B')
    return float(res.x[0])

def calculate_se(theta: float, responses: Dict[str, int], items: Dict[str, QuestionItem]) -> float:
    """
    Calculates the Standard Error (SE) of the theta estimate.

    Args:
        theta (float): The estimated latent trait value.
        responses (Dict[str, int]): Dictionary mapping item_id to selected category.
        items (Dict[str, QuestionItem]): Dictionary of items answered.

    Returns:
        float: The standard error.
    """
    info_sum = 1.0  # Prior information (Standard Normal)
    for item_id in responses.keys():
        if item_id in items:
            item = items[item_id]
            info_sum += fisher_information_grm(theta, item.a, item.b)
    return float(1.0 / np.sqrt(info_sum))

def select_next_item(state: TraitState, dimension_items: List[QuestionItem]) -> Optional[QuestionItem]:
    """
    Selects the next optimal item based on maximum Fisher Information.

    Args:
        state (TraitState): The current state of the trait estimation.
        dimension_items (List[QuestionItem]): List of available items for the dimension.

    Returns:
        Optional[QuestionItem]: The item that maximizes information, or None if all answered.
    """
    best_item = None
    max_info = -1.0
    
    for item in dimension_items:
        if item.item_id not in state.answered_items:
            info = fisher_information_grm(state.theta, item.a, item.b)
            if info > max_info:
                max_info = info
                best_item = item
                
    return best_item
