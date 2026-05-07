import json
import random

dimension_questions = {
    "BigFive_O": [
        "I have a rich vocabulary.",
        "I have a vivid imagination.",
        "I have excellent ideas.",
        "I am quick to understand things.",
        "I use difficult words.",
        "I spend time reflecting on things.",
        "I am full of ideas.",
        "I enjoy thinking about complex concepts.",
        "I am interested in abstract ideas.",
        "I appreciate art and aesthetics."
    ],
    "BigFive_C": [
        "I am always prepared.",
        "I pay attention to details.",
        "I get chores done right away.",
        "I like order.",
        "I follow a schedule.",
        "I am exacting in my work.",
        "I do things according to a plan.",
        "I continue until everything is perfect.",
        "I make plans and stick to them.",
        "I love keeping things neat and clean."
    ],
    "BigFive_E": [
        "I am the life of the party.",
        "I feel comfortable around people.",
        "I start conversations.",
        "I talk to a lot of different people at parties.",
        "I don't mind being the center of attention.",
        "I enjoy being part of a group.",
        "I easily make friends.",
        "I take charge in social situations.",
        "I know how to captivate people.",
        "I am skilled in handling social situations."
    ],
    "BigFive_A": [
        "I sympathize with others' feelings.",
        "I have a soft heart.",
        "I take time out for others.",
        "I feel others' emotions.",
        "I make people feel at ease.",
        "I inquire about others' well-being.",
        "I know how to comfort others.",
        "I love children.",
        "I am on good terms with nearly everyone.",
        "I have a good word for everyone."
    ],
    "BigFive_N": [
        "I get stressed out easily.",
        "I worry about things.",
        "I am easily disturbed.",
        "I get upset easily.",
        "I change my mood a lot.",
        "I have frequent mood swings.",
        "I often feel blue.",
        "I get irritated easily.",
        "I panic easily.",
        "I feel threatened easily."
    ],
    "Cognitive": [
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
    ]
}

items = []
item_idx = 1
for dim, qs in dimension_questions.items():
    for q in qs:
        # Realistic discrimination 'a' (typically 0.5 to 2.5)
        a = round(random.uniform(0.8, 2.5), 2)
        # Realistic difficulty thresholds 'b' for 5-point scale (b1, b2, b3, b4) ordered
        b1 = round(random.uniform(-3.0, -1.5), 2)
        b2 = round(random.uniform(-1.0, 0.0), 2)
        b3 = round(random.uniform(0.1, 1.5), 2)
        b4 = round(random.uniform(1.6, 3.0), 2)
        
        items.append({
            "item_id": f"q_{item_idx}",
            "dimension": dim,
            "text": q,
            "a": a,
            "b": [b1, b2, b3, b4]
        })
        item_idx += 1

with open("data/item_bank.json", "w") as f:
    json.dump(items, f, indent=2)
