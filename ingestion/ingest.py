from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DOCS_DIR = Path("docs")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "devops_docs"


def load_documents():
    documents = []

    for file_path in DOCS_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def main():
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    document_chunks = []
    chunk_ids = []
    metadatas = []

    counter = 0

    for document in documents:
        chunks = chunk_text(document["content"])

        for chunk in chunks:
            document_chunks.append(chunk)
            chunk_ids.append(f"chunk-{counter}")
            metadatas.append({
                "source": document["source"]
            })

            counter += 1

    embeddings = model.encode(document_chunks).tolist()

    collection.add(
        ids=chunk_ids,
        documents=document_chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(document_chunks)} chunks in ChromaDB")


if __name__ == "__main__":
    main()