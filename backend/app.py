from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag import get_context
from answer_generator import generate_answer

# Paths
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(
    title="AmoebaTronix Smart Support API",
    version="1.0.0"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------

class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AmoebaTronix Smart Support API"
    }


# -----------------------------
# Ask Question
# -----------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question."
        }

    context, results = get_context(question)

    if not context:
        return {
            "answer": (
                "I couldn't find relevant information in the "
                "AmoebaTronix knowledge base."
            ),
            "results": []
        }

    # Generate grounded answer from retrieved context
    answer = generate_answer(question, context)

    # Fallback to context if generator returns empty
    if not answer:
        answer = context

    return {
        "answer": answer,
        "results": results
    }


# -----------------------------
# Serve Frontend Static Files
# -----------------------------

if FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend"
    )