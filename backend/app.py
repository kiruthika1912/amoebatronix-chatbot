from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import get_context


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
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AmoebaTronix Smart Support API is running"
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
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
            )
        }

    # Temporary RAG response
    answer = (
        "Here is the relevant information from the "
        "AmoebaTronix knowledge base:\n\n"
        + context
    )

    return {
        "answer": answer,
        "results": results
    }