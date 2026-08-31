from app.rag import search_documents


def test_search_returns_results():
    results = search_documents("What is Kubernetes?")

    assert len(results) > 0
    assert "content" in results[0]
    assert "source" in results[0]


def test_search_finds_kubernetes_document():
    results = search_documents("What is Kubernetes?")

    sources = [result["source"] for result in results]

    assert "kubernetes.md" in sources