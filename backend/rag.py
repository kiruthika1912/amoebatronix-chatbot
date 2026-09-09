import os
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# KNOWLEDGE BASE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
KB_DIR = BASE_DIR / "knowledge_base"


# ============================================================
# EMBEDDING MODEL
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

documents = []
document_embeddings = []


def load_knowledge_base():

    global documents
    global document_embeddings

    documents = []

    kb_files = [
        "company.txt",
        "services.txt",
        "products.txt",
        "cloud_solutions.txt",
        "faq.txt"
    ]

    for filename in kb_files:

        file_path = KB_DIR / filename

        if not file_path.exists():
            print(f"WARNING: {filename} not found")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().strip()

            if not text:
                print(f"WARNING: {filename} is empty")
                continue

            # Split large files into smaller chunks
            chunks = split_text(text)

            for chunk in chunks:

                documents.append({
                    "source": filename,
                    "text": chunk
                })

            print(f"Loaded: {filename}")

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if documents:
        texts = [doc["text"] for doc in documents]

        document_embeddings = model.encode(
            texts,
            convert_to_numpy=True
        )

        print(f"\nKnowledge Base loaded successfully.")
        print(f"Total chunks: {len(documents)}")

    else:
        document_embeddings = []

        print("\nERROR: No Knowledge Base documents found.")


# ============================================================
# TEXT CHUNKING
# ============================================================

def split_text(text, chunk_size=1000):

    words = text.split()

    chunks = []

    current_chunk = []

    current_length = 0

    for word in words:

        current_chunk.append(word)

        current_length += len(word) + 1

        if current_length >= chunk_size:

            chunks.append(" ".join(current_chunk))

            current_chunk = []

            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ============================================================
# RETRIEVE RELEVANT INFORMATION
# ============================================================

def retrieve_context(question, top_k=4):

    if not documents or len(document_embeddings) == 0:

        return []

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    similarities = cosine_similarity(
        question_embedding,
        document_embeddings
    )[0]

    ranked_indexes = similarities.argsort()[::-1]

    results = []

    for index in ranked_indexes[:top_k]:

        results.append({
            "source": documents[index]["source"],
            "text": documents[index]["text"],
            "score": float(similarities[index])
        })

    return results


# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def get_context(question, top_k=4):

    results = retrieve_context(question, top_k)

    if not results:
        return "", []

    context_parts = []

    for result in results:

        context_parts.append(
            f"[Source: {result['source']}]\n"
            f"{result['text']}"
        )

    context = "\n\n".join(context_parts)

    return context, results


# ============================================================
# LOAD KB WHEN SERVER STARTS
# ============================================================

load_knowledge_base()