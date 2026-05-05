import numpy as np
from src.cat_engine import prob_grm, fisher_information_grm, estimate_theta_map, calculate_se
from src.models import QuestionItem

def test_prob_grm():
    theta = 0.0
    a = 1.0
    b = [-2.0, -0.5, 0.5, 2.0]
    p_k = prob_grm(theta, a, b, 2)
    assert 0.0 <= p_k <= 1.0

def test_fisher_information():
    theta = 0.0
    a = 1.0
    b = [-2.0, -0.5, 0.5, 2.0]
    info = fisher_information_grm(theta, a, b)
    assert info > 0.0

def test_estimate_theta_map():
    item1 = QuestionItem(item_id="1", dimension="dim", text="q1", a=1.0, b=[-2.0, -0.5, 0.5, 2.0])
    item2 = QuestionItem(item_id="2", dimension="dim", text="q2", a=1.0, b=[-2.0, -0.5, 0.5, 2.0])
    
    items = {"1": item1, "2": item2}
    responses_high = {"1": 4, "2": 4}
    responses_low = {"1": 0, "2": 0}
    
    theta_high = estimate_theta_map(responses_high, items)
    theta_low = estimate_theta_map(responses_low, items)
    
    assert theta_high > theta_low

def test_calculate_se():
    item1 = QuestionItem(item_id="1", dimension="dim", text="q1", a=1.0, b=[-2.0, -0.5, 0.5, 2.0])
    items = {"1": item1}
    responses = {"1": 2}
    
    se = calculate_se(0.0, responses, items)
    assert se > 0.0
