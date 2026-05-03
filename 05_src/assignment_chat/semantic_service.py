import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "pitchfork_reviews"


def get_collection():
    # Loads the persistent ChromaDB collection using local default embeddings.
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )


def semantic_search(query: str, n_results: int = 3):
    # Searches Pitchfork reviews by semantic similarity.
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]


def semantic_service(query: str) -> str:
    # Returns the most relevant Pitchfork review excerpts.
    documents = semantic_search(query)

    if not documents:
        return "I could not find relevant Pitchfork reviews."

    response = "Here are the most relevant Pitchfork review excerpts:\n\n"

    for i, document in enumerate(documents, start=1):
        preview = document[:600].replace("\n", " ")
        response += f"{i}. {preview}...\n\n"

    return response


if __name__ == "__main__":
    test_query = input("Ask about Pitchfork reviews: ")
    print(semantic_service(test_query))