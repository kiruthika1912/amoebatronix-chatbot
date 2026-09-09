from pathlib import Path

from sentence_transformers import SentenceTransformer
import faiss


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

KB_DIR = BASE_DIR / "knowledge_base"

COMPANY_FILE = KB_DIR / "company.txt"

INDEX_FILE = BASE_DIR / "company_index.faiss"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!")


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():

            chunks.append(chunk)

    return chunks


# ============================================================
# BUILD FAISS INDEX
# ============================================================

def build_index():

    if not COMPANY_FILE.exists():

        raise FileNotFoundError(
            f"company.txt not found at: {COMPANY_FILE}"
        )

    text = COMPANY_FILE.read_text(
        encoding="utf-8"
    )

    chunks = create_chunks(text)

    if not chunks:

        raise ValueError(
            "company.txt is empty."
        )

    print(
        f"Creating embeddings for {len(chunks)} chunks..."
    )

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    print("\n================================")
    print("FAISS INDEX CREATED SUCCESSFULLY")
    print("================================")

    print(
        "Chunks:",
        len(chunks)
    )

    print(
        "Index:",
        INDEX_FILE
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    build_index()