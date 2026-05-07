import pytest
import numpy as np

from src.cat_engine import prob_grm, fisher_information_grm, estimate_theta_map, calculate_se
from src.models import QuestionItem

@pytest.fixture
def mock_item() -> QuestionItem:
    return QuestionItem(
        item_id="q1",
        dimension="Cognitive",
        text="Sample question",
        a=1.5,
        b=[-2.0, -0.5, 0.5, 2.0]
    )

@pytest.mark.parametrize("k", [0, 1, 2, 3, 4])
def test_prob_grm(mock_item: QuestionItem, k: int) -> None:
    theta = 0.0
    p_k = prob_grm(theta, mock_item.a, mock_item.b, k)
    assert 0.0 <= p_k <= 1.0

def test_prob_grm_sum_to_one(mock_item: QuestionItem) -> None:
    theta = 1.0
    total_prob = sum(prob_grm(theta, mock_item.a, mock_item.b, k) for k in range(5))
    assert np.isclose(total_prob, 1.0)

def test_fisher_information(mock_item: QuestionItem) -> None:
    theta = 0.0
    info = fisher_information_grm(theta, mock_item.a, mock_item.b)
    assert info > 0.0

def test_estimate_theta_map() -> None:
    item1 = QuestionItem(item_id="1", dimension="dim", text="q1", a=1.0, b=[-2.0, -0.5, 0.5, 2.0])
    item2 = QuestionItem(item_id="2", dimension="dim", text="q2", a=1.0, b=[-2.0, -0.5, 0.5, 2.0])
    
    items = {"1": item1, "2": item2}
    responses_high = {"1": 4, "2": 4}
    responses_low = {"1": 0, "2": 0}
    
    theta_high = estimate_theta_map(responses_high, items)
    theta_low = estimate_theta_map(responses_low, items)
    
    assert theta_high > theta_low

def test_calculate_se(mock_item: QuestionItem) -> None:
    items = {mock_item.item_id: mock_item}
    responses = {mock_item.item_id: 2}
    
    se = calculate_se(0.0, responses, items)
    assert se > 0.0
    assert se < 1.0  # Because prior gives 1.0, and item adds info
