import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.models import QuestionItem, TraitState, AssessmentProfile
from src.cat_engine import estimate_theta_map, calculate_se, select_next_item
from src.profile_generator import generate_profile
from typing import Dict, List
import os

app = FastAPI()

with open("data/item_bank.json", "r") as f:
    raw_items = json.load(f)
    ITEM_BANK = {item["item_id"]: QuestionItem(**item) for item in raw_items}

DIMENSIONS = list(set(item.dimension for item in ITEM_BANK.values()))
session_state: Dict[str, TraitState] = {dim: TraitState() for dim in DIMENSIONS}

app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("src/static/index.html")

@app.get("/api/next_question")
def get_next_question():
    for dim in DIMENSIONS:
        state = session_state[dim]
        if len(state.responses) < 5 and state.se > 0.32:
            dim_items = [item for item in ITEM_BANK.values() if item.dimension == dim]
            next_item = select_next_item(state, dim_items)
            if next_item:
                return next_item.model_dump()
    return {"status": "complete"}

@app.post("/api/submit_answer")
def submit_answer(item_id: str, answer: int):
    if item_id not in ITEM_BANK:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = ITEM_BANK[item_id]
    state = session_state[item.dimension]
    
    state.responses[item_id] = answer
    state.answered_items.append(item_id)
    
    dim_items_dict = {i_id: ITEM_BANK[i_id] for i_id in state.answered_items}
    state.theta = estimate_theta_map(state.responses, dim_items_dict)
    state.se = calculate_se(state.theta, state.responses, dim_items_dict)
    
    return {"status": "success", "theta": state.theta, "se": state.se}

@app.get("/api/profile")
def get_profile():
    traits = {dim: state.theta for dim, state in session_state.items()}
    profile = generate_profile(traits)
    
    os.makedirs("data", exist_ok=True)
    with open("data/personality_profile.json", "w") as f:
        f.write(profile.model_dump_json(indent=2))
        
    return profile.model_dump()
