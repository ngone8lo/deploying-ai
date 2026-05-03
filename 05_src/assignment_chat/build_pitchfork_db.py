import json
import os
import chromadb
from chromadb.utils import embedding_functions

DATA_PATH = "../documents/pitchfork_content.jsonl"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "pitchfork_reviews"


def load_pitchfork_reviews(limit=500):
    # Loads review text from the Pitchfork JSONL dataset.
    reviews = []

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if limit and i >= limit:
                break

            record = json.loads(line)
            text = record.get("content", "")

            if text.strip():
                reviews.append({
                    "id": str(record.get("reviewid", i)),
                    "text": text
                })

    return reviews


def build_database():
    # Builds a persistent ChromaDB collection using local default embeddings.
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    reviews = load_pitchfork_reviews()

    documents = [review["text"][:3000] for review in reviews]
    ids = [review["id"] for review in reviews]

    collection.add(
        documents=documents,
        ids=ids
    )

    print(f"Added {len(documents)} Pitchfork reviews to ChromaDB.")


if __name__ == "__main__":
    build_database()