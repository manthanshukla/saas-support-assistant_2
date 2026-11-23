
from pypdf import PdfReader
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import re


# 1. Load PDF
BASE_DIR = Path(__file__).resolve().parents[1]
PDF_PATH = BASE_DIR / "knowledge_base" / "clouddesk_knowledge_base.pdf"


def load_pdf():
    reader = PdfReader(str(PDF_PATH))

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    return text


# 2. Divide PDF into chunks
def create_chunks(text):

    chunks = re.split(
        r"(?=Document\s+\d+\s*[·])",
        text
    )

    chunks = [
        chunk.strip()
        for chunk in chunks
        if re.match(r"Document\s+\d+\s*[·]", chunk.strip())
    ]

    return chunks


# 3. Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# 4. Read PDF and create chunks
pdf_text = load_pdf()
knowledge_chunks = create_chunks(pdf_text)


# 5. Convert PDF chunks into embeddings
embeddings = model.encode(
    knowledge_chunks,
    convert_to_numpy=True
)

# 6. Create FAISS index
faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)


# 7. Search for relevant chunks
def retrieve_documents(query: str, top_k=3):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx != -1:
            results.append({
                "content": knowledge_chunks[idx],
                "score": float(score)
            })

    return results
