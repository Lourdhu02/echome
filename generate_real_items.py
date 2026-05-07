import json
import random
from pathlib import Path

# Expanded dimension questions based on ECHOME Architecture Doc
# Targets 8 main dimensions
dimension_questions = {
    "BigFive": [
        "I am the life of the party.",
        "I sympathize with others' feelings.",
        "I am always prepared.",
        "I get stressed out easily.",
        "I have a vivid imagination.",
        "I talk to a lot of different people at parties.",
        "I am not really interested in others' problems.",
        "I leave my belongings around.",
        "I am relaxed most of the time.",
        "I am not interested in abstract ideas.",
        "I feel comfortable around people.",
        "I insult people.",
        "I pay attention to details.",
        "I worry about things.",
        "I have a rich vocabulary.",
        "I keep in the background.",
        "I sympathize with others' feelings.",
        "I make a mess of things.",
        "I seldom feel blue.",
        "I am not interested in abstract ideas."
    ],
    "CognitiveStyle": [
        "I prefer to solve problems through careful analysis rather than intuition.",
        "I enjoy tackling complex, abstract problems.",
        "I rely heavily on data to make decisions.",
        "I process information systematically, step-by-step.",
        "I can quickly adapt my thinking when new information is presented.",
        "I prefer logic over feelings when resolving conflicts.",
        "I enjoy optimizing systems and processes.",
        "I am quick to spot logical inconsistencies.",
        "I prefer long-term strategic planning over short-term tactics.",
        "I break down large tasks into smaller, manageable sub-tasks."
    ],
    "Lifestyle": [
        "I adhere strictly to a daily routine.",
        "I prefer to exercise in the morning rather than the evening.",
        "I closely monitor my diet and nutrition.",
        "I need at least 8 hours of sleep to function optimally.",
        "My workspace is always meticulously organized.",
        "I plan my meals well in advance.",
        "I prefer waking up early over staying up late.",
        "I track my habits and daily goals.",
        "I limit my screen time before bed.",
        "I prefer quiet, distraction-free environments for deep work."
    ],
    "Entertainment": [
        "I prefer scientifically accurate documentaries over action movies.",
        "I enjoy deep, narrative-driven video games.",
        "I frequently read non-fiction books for pleasure.",
        "I enjoy attending live music performances or theatre.",
        "I am drawn to media that explores complex philosophical themes.",
        "I prefer indie films over big-budget blockbusters.",
        "I listen to podcasts on educational or technical topics.",
        "I enjoy strategy board games.",
        "I follow deep analytical essays on media and culture.",
        "I prefer to consume media that challenges my worldview."
    ],
    "Sports": [
        "I enjoy competitive team sports.",
        "I follow professional sports leagues closely.",
        "I prefer individual athletic pursuits like running or swimming.",
        "I enjoy the tactical side of sports more than the physical.",
        "I find watching sports to be a primary form of relaxation.",
        "I enjoy high-intensity interval training (HIIT).",
        "I prefer outdoor sports over indoor gym activities.",
        "I am interested in sports analytics and statistics.",
        "I value sportsmanship over winning at all costs.",
        "I enjoy extreme sports or high-risk athletic activities."
    ],
    "Hobbies": [
        "I enjoy building things with my hands (DIY, woodworking, etc.).",
        "I am passionate about learning new technical skills.",
        "I enjoy artistic expression (painting, writing, music).",
        "I am an avid collector (books, gear, digital assets).",
        "I enjoy gardening or working with nature.",
        "I spend a significant amount of time on passion projects.",
        "I enjoy teaching others about my hobbies.",
        "I am interested in historical research or genealogy.",
        "I enjoy culinary arts and experimenting with recipes.",
        "I prefer hobbies that require deep concentration."
    ],
    "Travel": [
        "I prefer exploring off-the-beaten-path destinations.",
        "I enjoy highly organized and planned travel itineraries.",
        "I travel primarily to experience new cultures and cuisines.",
        "I prefer luxury and comfort when traveling.",
        "I enjoy adventure travel (hiking, backpacking, camping).",
        "I prefer solo travel over group tours.",
        "I am interested in the history and architecture of my destinations.",
        "I travel to disconnect and unplug from technology.",
        "I enjoy visiting bustling urban centers.",
        "I plan my travel based on local events or festivals."
    ],
    "Social": [
        "I prefer small, intimate gatherings over large parties.",
        "I am a good listener and value deep conversations.",
        "I enjoy meeting new people from diverse backgrounds.",
        "I am comfortable taking the lead in social situations.",
        "I prefer asynchronous communication (text/email) over calls.",
        "I value loyalty and long-term friendships above all.",
        "I am quick to forgive and move on from social conflicts.",
        "I enjoy collaborating on group projects.",
        "I am sensitive to the social atmosphere of a room.",
        "I enjoy debating ideas with others."
    ]
}

def generate_items():
    """Generates the item bank JSON file."""
    items = []
    item_idx = 1
    
    for dim, qs in dimension_questions.items():
        for q in qs:
            # Calibrated parameters (3PL simulated)
            a = round(random.uniform(1.0, 2.5), 2)  # Discrimination
            # 4 difficulty thresholds for 5-point Likert
            b = sorted([round(random.uniform(-3.0, 3.0), 2) for _ in range(4)])
            
            items.append({
                "item_id": f"q_{item_idx}",
                "dimension": dim,
                "text": q,
                "a": a,
                "b": b
            })
            item_idx += 1

    output_path = Path("data/item_bank.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    
    print(f"Successfully generated {len(items)} items for ECHOME Mind Engine.")

if __name__ == "__main__":
    generate_items()
