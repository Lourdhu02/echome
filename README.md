# ECHOME: Embedded Cognitive Human Operative Mirror Engine

ECHOME is a sophisticated "Digital Extension" framework designed to clone and automate a user's identity across three fundamental pillars: **Mind**, **Voice**, and **Action**. Built entirely from open-source components and designed for full local execution, ECHOME transitions from a personality assessment tool into a Jarvis-grade personal intelligence layer.

Developed by Raju, an AI/ML Engineer, ECHOME is a showcase of production-grade engineering, merging psychometrics, voice synthesis, and autonomous agent orchestration.

## 🏛️ The Three Pillars

### Pillar 1: Mind (Personality Engine)
The foundation of ECHOME is a high-precision **Computerized Adaptive Testing (CAT)** system. It utilizes **Graded Response Models (GRM)** to accurately map a user's latent traits across 8 dimensions:
- Big Five (OCEAN)
- Cognitive Style
- Lifestyle & Habits
- Entertainment & Media
- Sports & Athletics
- Hobbies & Creative
- Travel & Exploration
- Social & Relationships

The engine uses **Fisher Information** optimization to minimize assessment length while maintaining a Standard Error (SE) < 0.32.

### Pillar 2: Voice (Voice Clone Engine)
A fully local, 4-stage voice cloning pipeline that captures your speaker identity and reproduces it for all synthesized output:
1. **ASR:** OpenAI Whisper (Local) for speech-to-text.
2. **Encoder:** Resemblyzer for d-vector vocal fingerprint extraction.
3. **Synthesis:** Coqui TTS (XTTSv2) for zero-shot voice cloning.
4. **Vocoder:** HiFi-GAN for high-fidelity 22kHz audio generation.

### Pillar 3: Action (Agent Framework)
An autonomous execution layer powered by **LangGraph** and **LangChain**. It routes tasks to specialist agents:
- **BashAgent:** System operations and shell execution.
- **TechAgent:** Architecture and engineering analysis.
- **FileAgent:** Autonomous file management.
- **MemoryManager:** A 3-tier memory system (Episodic, Semantic, Procedural) based on the CoALA framework.

## 🚀 Technical Stack

- **Orchestration:** LangGraph, LangChain
- **Backend:** FastAPI, Python 3.10+
- **Machine Learning:** PyTorch, SciPy, NumPy
- **Voice:** Whisper, Coqui TTS, Resemblyzer
- **Memory:** Qdrant (Vector DB), Mem0
- **Containerization:** Docker & Docker Compose

## 🛠️ Getting Started

### Installation
```bash
git clone https://github.com/Lourdhu02/echome.git
cd echome
pip install -r requirements.txt
```

### Initialize the Mind Engine
```bash
python generate_real_items.py
```

### Launch the Full Environment
```bash
# Start the FastAPI Assessment App and Agent Orchestrator
uvicorn src.assessment_app:app --reload
```

### Docker Deployment
```bash
docker-compose up --build
```

## 📂 Repository Structure
- `src/assessment_app.py`: FastAPI API and Mind Engine interface.
- `src/orchestrator.py`: LangGraph-based agent routing logic (Action Pillar).
- `src/voice_engine.py`: Whisper and XTTSv2 integration (Voice Pillar).
- `src/memory_manager.py`: 3-tier memory system implementation.
- `src/agents/`: Specialist agent implementations.
- `src/cat_engine.py`: IRT and MAP optimization logic.

---
Engineered by Raju | AI/ML Engineer
*The digital mirror. Built to scale, designed to be you.*
