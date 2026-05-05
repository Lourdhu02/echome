import numpy as np
from scipy.optimize import minimize
from typing import List, Dict, Optional
from src.models import QuestionItem, TraitState

def prob_grm(theta: float, a: float, b: List[float], k: int) -> float:
    def p_star(t, disc, diff):
        return 1.0 / (1.0 + np.exp(-disc * (t - diff)))
    
    if k == 0:
        return 1.0 - p_star(theta, a, b[0])
    elif k == len(b):
        return p_star(theta, a, b[-1])
    else:
        return p_star(theta, a, b[k - 1]) - p_star(theta, a, b[k])

def fisher_information_grm(theta: float, a: float, b: List[float]) -> float:
    info = 0.0
    for k in range(len(b) + 1):
        p_k = prob_grm(theta, a, b, k)
        if p_k > 1e-10:
            def p_star(t, diff):
                return 1.0 / (1.0 + np.exp(-a * (t - diff)))
            
            p_star_k_minus_1 = p_star(theta, b[k-1]) if k > 0 else 1.0
            p_star_k = p_star(theta, b[k]) if k < len(b) else 0.0
            
            dp_k_dtheta = a * (p_star_k_minus_1 * (1 - p_star_k_minus_1) - p_star_k * (1 - p_star_k))
            info += (dp_k_dtheta ** 2) / p_k
    return info

def estimate_theta_map(responses: Dict[str, int], items: Dict[str, QuestionItem]) -> float:
    if not responses:
        return 0.0
        
    def neg_log_posterior(theta_val):
        t = theta_val[0]
        log_prior = -0.5 * (t ** 2)
        log_likelihood = 0.0
        for item_id, resp in responses.items():
            item = items[item_id]
            prob = prob_grm(t, item.a, item.b, resp)
            log_likelihood += np.log(prob + 1e-10)
        return -(log_prior + log_likelihood)
        
    res = minimize(neg_log_posterior, x0=np.array([0.0]), bounds=[(-4.0, 4.0)], method='L-BFGS-B')
    return float(res.x[0])

def calculate_se(theta: float, responses: Dict[str, int], items: Dict[str, QuestionItem]) -> float:
    info_sum = 1.0 
    for item_id in responses.keys():
        info_sum += fisher_information_grm(theta, items[item_id].a, items[item_id].b)
    return 1.0 / np.sqrt(info_sum)

def select_next_item(state: TraitState, dimension_items: List[QuestionItem]) -> Optional[QuestionItem]:
    best_item = None
    max_info = -1.0
    
    for item in dimension_items:
        if item.item_id not in state.answered_items:
            info = fisher_information_grm(state.theta, item.a, item.b)
            if info > max_info:
                max_info = info
                best_item = item
                
    return best_item
