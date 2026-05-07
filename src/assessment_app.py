import json
import logging
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import ValidationError

from src.models import QuestionItem, TraitState, AssessmentProfile
from src.cat_engine import estimate_theta_map, calculate_se, select_next_item
from src.profile_generator import generate_profile

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ECHOME Assessment API",
    description="Computerized Adaptive Testing engine utilizing Graded Response Models.",
    version="1.0.0",
)

DATA_DIR = Path("data")
ITEM_BANK_FILE = DATA_DIR / "item_bank.json"

ITEM_BANK: Dict[str, QuestionItem] = {}
DIMENSIONS: list[str] = []
session_state: Dict[str, TraitState] = {}

def load_item_bank() -> None:
    """Loads the item bank from disk and initializes the session state."""
    global ITEM_BANK, DIMENSIONS, session_state
    try:
        if not ITEM_BANK_FILE.exists():
            logger.warning(f"Item bank file not found at {ITEM_BANK_FILE}. Using empty bank.")
            return

        with open(ITEM_BANK_FILE, "r", encoding="utf-8") as f:
            raw_items = json.load(f)
            
        ITEM_BANK = {item["item_id"]: QuestionItem(**item) for item in raw_items}
        DIMENSIONS = list(set(item.dimension for item in ITEM_BANK.values()))
        session_state = {dim: TraitState() for dim in DIMENSIONS}
        logger.info(f"Loaded {len(ITEM_BANK)} items across {len(DIMENSIONS)} dimensions.")
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"Failed to load item bank: {e}")
        raise RuntimeError(f"Invalid item bank data: {e}")

load_item_bank()

STATIC_DIR = Path("src/static")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", summary="Serve frontend app")
def read_root() -> FileResponse:
    """
    Serves the main frontend application.

    Returns:
        FileResponse: The index.html file.
    
    Raises:
        HTTPException: If the index.html file is not found.
    """
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_file)

@app.get("/api/next_question", summary="Get next optimal question")
def get_next_question() -> Dict[str, Any]:
    """
    Determines and returns the next optimal question for the user based on CAT.

    Returns:
        Dict[str, Any]: A serialized QuestionItem or a completion status.
    """
    if not ITEM_BANK:
        raise HTTPException(status_code=500, detail="Item bank is empty or not loaded.")

    for dim in DIMENSIONS:
        state = session_state.get(dim)
        if state is None:
            continue
            
        if len(state.responses) < 5 and state.se > 0.32:
            dim_items = [item for item in ITEM_BANK.values() if item.dimension == dim]
            next_item = select_next_item(state, dim_items)
            if next_item:
                return next_item.model_dump()
                
    return {"status": "complete"}

@app.post("/api/submit_answer", summary="Submit answer for a question")
def submit_answer(item_id: str, answer: int) -> Dict[str, Any]:
    """
    Processes a submitted answer and updates the latent trait estimates.

    Args:
        item_id (str): The unique identifier of the question item.
        answer (int): The selected answer on a 1-5 rating scale.

    Returns:
        Dict[str, Any]: The updated theta and standard error.
        
    Raises:
        HTTPException: If the item_id is not found or answer is out of bounds.
    """
    if item_id not in ITEM_BANK:
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found in the item bank.")
        
    if not (1 <= answer <= 5):
        raise HTTPException(status_code=400, detail=f"Expected answer between 1 and 5, got {answer}.")
    
    item = ITEM_BANK[item_id]
    state = session_state[item.dimension]
    
    # Convert 1-5 rating scale to 0-4 category index for GRM
    k = answer - 1
    state.responses[item_id] = k
    if item_id not in state.answered_items:
        state.answered_items.append(item_id)
    
    dim_items_dict = {i_id: ITEM_BANK[i_id] for i_id in state.answered_items}
    state.theta = estimate_theta_map(state.responses, dim_items_dict)
    state.se = calculate_se(state.theta, state.responses, dim_items_dict)
    
    return {"status": "success", "theta": state.theta, "se": state.se}

@app.get("/api/profile", summary="Generate final assessment profile", response_model=AssessmentProfile)
def get_profile() -> AssessmentProfile:
    """
    Generates the final personality/assessment profile based on trait estimates.

    Returns:
        AssessmentProfile: The generated profile containing percentiles and predictions.
    """
    traits = {dim: state.theta for dim, state in session_state.items()}
    profile = generate_profile(traits)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    profile_path = DATA_DIR / "personality_profile.json"
    
    try:
        with open(profile_path, "w", encoding="utf-8") as f:
            f.write(profile.model_dump_json(indent=2))
    except IOError as e:
        logger.error(f"Failed to save profile to disk: {e}")
        
    return profile
