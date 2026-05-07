# ECHOME: High-Precision Adaptive Assessment Engine

ECHOME is a sophisticated Computerized Adaptive Testing (CAT) framework designed to estimate latent human traits with maximal efficiency and mathematical rigor. By leveraging Graded Response Models (GRM) and Bayesian estimation, the engine dynamically recalibrates its internal state with every user interaction, ensuring that every question asked provides the highest possible information gain.

Developed by Raju, this project serves as a demonstration of production-grade AI/ML engineering, combining psychometric theory with a high-performance FastAPI backend and a minimalist, elite design system.

## Core Capabilities

### 1. Mathematical Precision
The engine utilizes the Graded Response Model (GRM), a specialized form of Item Response Theory (IRT) for polytomous data. Latent trait estimation (Theta) is performed using Maximum A Posteriori (MAP) optimization, which balances the observed likelihood with a standard normal prior to ensure stability even with sparse data.

### 2. Information-Theoretic Item Selection
To minimize assessment length without compromising reliability, ECHOME implements active item selection based on Fisher Information. The engine calculates the expected information for every candidate item in the bank relative to the user's current estimated Theta, selecting the item that most effectively reduces the standard error of measurement.

### 3. Dynamic Profiling and Synthesis
Upon reaching the target precision (Standard Error < 0.32), the engine maps the latent multidimensional traits to human-readable percentiles and generates a behavioral synthesis. This involves mapping raw scores to archetypes and predicting behavioral tendencies based on established psychological frameworks.

## Technical Architecture

### Backend Stack
- Framework: FastAPI (Asynchronous, Type-Safe)
- Computation: NumPy, SciPy (Optimization & Statistics)
- Validation: Pydantic v2 (Strict Data Modeling)
- Environment: Docker & Docker Compose

### Frontend Philosophy
The user interface follows a "Less is More" philosophy. Built with pure Vanilla CSS and JavaScript, it prioritizes typography, motion design, and high-contrast dark-mode aesthetics to provide a premium, focused user experience.

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (Optional)

### Installation (Local)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/echome.git
   cd echome
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the Item Bank:
   ```bash
   python generate_real_items.py
   ```
4. Launch the Engine:
   ```bash
   uvicorn src.assessment_app:app --reload
   ```

### Deployment (Docker)
The application is fully containerized for production parity:
```bash
docker-compose up --build
```
The application will be available at `http://localhost:8000`.

## Testing Suite
The codebase maintains high integrity through a comprehensive testing suite powered by `pytest`.
```bash
pytest tests/
```

## Repository Structure
- `src/assessment_app.py`: Main API orchestration and endpoint management.
- `src/cat_engine.py`: Core IRT implementation and optimization logic.
- `src/models.py`: Unified Pydantic schema declarations.
- `src/profile_generator.py`: Behavioral mapping and percentile synthesis logic.
- `src/static/`: Premium minimalist frontend assets.
- `data/`: Local storage for item banks and generated profiles.

---
Engineered by Raju | AI/ML Engineer
Precision. Scale. Synthesis.
