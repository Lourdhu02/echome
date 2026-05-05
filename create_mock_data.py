import json
import random
import os

dimensions = ["BigFive_O", "BigFive_C", "BigFive_E", "BigFive_A", "BigFive_N", "Cognitive", "Lifestyle", "Entertainment"]
items = []

for i in range(1, 241):
    dim = dimensions[i % len(dimensions)]
    items.append({
        "item_id": f"q_{i}",
        "dimension": dim,
        "text": f"This is a mocked question for {dim} (Question {i}). Do you strongly agree?",
        "a": round(random.uniform(0.8, 2.5), 2),
        "b": sorted([round(random.uniform(-3, 3), 2) for _ in range(4)])
    })

os.makedirs("data", exist_ok=True)
with open("data/item_bank.json", "w") as f:
    json.dump(items, f, indent=2)
