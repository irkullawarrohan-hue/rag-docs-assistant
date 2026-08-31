import os

import chromadb
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="devops_docs"
)


def search_documents(query: str, n_results: int = 2):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return [
        {
            "content": document,
            "source": metadata["source"]
        }
        for document, metadata in zip(documents, metadatas)
    ]


def generate_answer(query: str):
    groq_client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    documents = search_documents(query)

    context = "\n\n".join(
        f"Source: {doc['source']}\n{doc['content']}"
        for doc in documents
    )

    prompt = f"""
You are an internal documentation assistant.

Answer the user's question using ONLY the provided documentation.

If the documentation does not contain the answer, say:
"I couldn't find this information in the provided documentation."

Do not make up information.

Documentation:
{context}

User question:
{query}
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [doc["source"] for doc in documents]
    }