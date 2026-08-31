from fastapi import FastAPI
from app.rag import search_documents, generate_answer


app = FastAPI(title="RAG Docs Assistant")


@app.get("/")
def home():
    return {
        "message": "RAG Docs Assistant is running"
    }


@app.get("/search")
def search(query: str):
    results = search_documents(query)

    return {
        "query": query,
        "results": results
    }


@app.get("/ask")
def ask(query: str):
    return generate_answer(query)