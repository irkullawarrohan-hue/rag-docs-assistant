import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="devops_docs"
)

results = collection.query(
    query_texts=["What is Kubernetes?"],
    n_results=2
)

for document, metadata in zip(
    results["documents"][0],
    results["metadatas"][0]
):
    print("\nSOURCE:", metadata["source"])
    print("CONTENT:", document)