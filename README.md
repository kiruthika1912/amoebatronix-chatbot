# AmoebaTronix Smart Support AI Chatbot

An enterprise-ready AI knowledge assistant powered by **FastAPI**, **Retrieval-Augmented Generation (RAG)**, **Sentence-Transformers**, and a modern web interface.

---

## 📁 Project Directory Structure & File Guide

```text
amoebatronix-chatbot/
│
├── run.py                       # 🚀 Single runner: Starts Backend API + Frontend UI simultaneously
├── .gitignore                   # Ignores virtual envs, caches, model files, and IDE configs
├── README.md                    # Project documentation & file guide
│
├── backend/                     # ⚙️ Python RAG Engine & REST API
│   ├── app.py                   # FastAPI app: routes (/ask, /health), CORS, and Frontend static mounting
│   ├── rag.py                   # Loads knowledge documents, generates embeddings & computes similarity
│   ├── answer_generator.py      # Grounded response generator: cleans & extracts concise answers
│   ├── requirements.txt         # Python package dependencies
│   │
│   └── knowledge_base/          # 📄 Enterprise knowledge base text sources
│       ├── company.txt          # Company profile, headquarters, contact info, business hours
│       ├── services.txt         # IT services, infrastructure, networking, AMC, software development
│       ├── products.txt         # Hardware catalog: servers, workstations, laptops, networking gear
│       ├── cloud_solutions.txt  # Cloud migration, Microsoft Azure, Google Workspace, backups
│       └── faq.txt              # Frequently asked questions and common queries
│
└── frontend/                    # 🌐 Web UI Interface
    ├── index.html               # Semantic HTML5 chat interface layout & quick query chips
    ├── style.css                # Visual theme, typography, responsive styling & chat animations
    ├── script.js                # Frontend controller: connects to /ask, manages chat state & rendering
    └── amoeba chatbot.html      # Original standalone prototype layout (kept for reference)
```

---

## 📝 Detailed File Roles & Uses

### Root
- **`run.py`**:
  - The primary entry point for the entire project.
  - Starts the FastAPI Uvicorn server and serves both the backend API and frontend static UI together on `http://127.0.0.1:8000`.
  - Automatically pops open your default web browser to the chat application.

### Backend (`backend/`)
- **`backend/app.py`**:
  - Sets up the FastAPI application with CORS enabled for cross-origin callers.
  - Endpoints:
    - `GET /`: Serves the Chatbot web interface (`frontend/index.html`).
    - `GET /health`: Health-check endpoint returning system status.
    - `POST /ask`: Accepts a JSON query (`{"question": "..."}`), retrieves relevant context, generates an answer, and returns the response.
    - `GET /docs`: Interactive Swagger API documentation.
- **`backend/rag.py`**:
  - Handles the RAG pipeline.
  - Loads all `.txt` documents from `backend/knowledge_base/`, breaks them into manageable chunks, and encodes them using `sentence-transformers/all-MiniLM-L6-v2`.
  - Provides `get_context(question)` which calculates cosine similarity between the query embedding and document embeddings to retrieve the top matching excerpts.
- **`backend/answer_generator.py`**:
  - Applies topic detection, keyword scoring, and sentence filtering to extract clean, grounded answers directly from the retrieved context without hallucination.
- **`backend/knowledge_base/`**:
  - The ground truth information files. Update any `.txt` file here to add or revise facts about the company, products, or services.

### Frontend (`frontend/`)
- **`frontend/index.html`**:
  - Clean HTML5 chat window, sidebar navigation, project selector, and quick question suggestions.
- **`frontend/style.css`**:
  - Responsive stylesheet featuring modern card designs, chat bubbles, badges, and responsive layouts.
- **`frontend/script.js`**:
  - Listens for user input (Enter key or Send button click).
  - Dynamically dispatches POST requests to `/ask`.
  - Displays user message, animated loading state, bot reply, and error handling.

---

## ⚡ Quick Start: Running in a Single Command

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Activate Virtual Environment (if not already active)
```powershell
# In PowerShell:
.\backend\venv\Scripts\Activate.ps1
```

### 3. Start the Unified Application
Run from the project root:
```powershell
python run.py
```

- Both Backend and Frontend start on: **`http://127.0.0.1:8000`**
- Your default web browser will automatically open to the Chatbot!
- Interactive API Documentation is available at: **`http://127.0.0.1:8000/docs`**
