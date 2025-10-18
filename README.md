# FinPlan AI

Personal financial planning platform that combines multi-agent orchestration, Retrieval-Augmented Generation, and predictive modeling to deliver goal-aligned investment recommendations and portfolio insights.

---

## Features
- **Personalized Investment Strategy** — recommendations across stocks, SIPs, precious metals, real estate, and financial schemes.  
- **AI-Powered Modeling** — LLMs + RAG + FAISS vector search for context-aware advice and explainable forecasts.  
- **Customer Intelligence** — clustering artifacts and example pipelines for segmentation and targeted recommendations.  
- **Modular Agent Orchestration** — pluggable agents, tool adapters, and plan templates for extensible workflows.  
- **Demos and UIs** — Streamlit and FastAPI / Flask entry points for rapid prototyping and stakeholder demos.  
- **Reproducible Artifacts** — bundled model checkpoints, FAISS index, sample notebooks, and test data.

---

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite  
- **Frontend**: React.js, Tailwind CSS  
- **ML and Retrieval**: PyTorch artifacts, FAISS vector index, embeddings + RAG pipelines  
- **Tools**: Streamlit demos, local JSON stores for quick experiments

---

## Quick Start
1. Clone repository
```bash
git clone https://github.com/yatesh12/FinPlan.git
cd <repo-folder>
```
2. Backend setup
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with necessary keys
python init_sqlite_db.py
uvicorn main:app --reload
```
3. Frontend setup
```bash
cd frontend
npm install
npm start
```
4. Streamlit demo
```bash
cd backend
streamlit run streamlit_app.py
```

---

## Project Structure
- **backend/** — FastAPI app, services, ML utilities, Streamlit demo, DB migrations  
- **frontend/** — React UI, API clients, pages and assets  
- **data/** — model artifacts, FAISS index, sample CSVs and PDFs  
- **rag_system/** and **rag_index_faiss/** — ingestion pipelines, vector store, FAISS index files  
- **multi_agent_orchestrator.py**, **ai_agent_system.py**, **agent_config.py** — core orchestration and agent definitions  
- **demo_ai_agent.py**, **app.py**, **enhanced_app*.py** — entry points and demos

---

## 🧭 Architecture Overview

![AstraMind Architecture](assets/architecture.png)

*Figure: High-level system architecture showing multi-agent orchestration, RAG retrieval, ML services, and frontend integration.*

---

## Contributing and License
- **Contributing**: Fork, create a feature branch, add tests, and open a PR with a clear description and changelog. Follow existing code patterns for agents, prompts, and schema validation.  
- **Recommended License**: MIT or Apache 2.0. Add a LICENSE file to define project terms.

