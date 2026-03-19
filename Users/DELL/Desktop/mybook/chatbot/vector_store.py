import os
from qdrant_client import QdrantClient, models
from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")
        self.vector_size = 3072  # OpenAI text-embedding-ada-002 output dimension

    def recreate_collection(self):
        """Recreates the Qdrant collection, deleting if it already exists."""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{self.collection_name}' recreated.")

    def upsert_vectors(self, contents: List[str], embeddings: List[List[float]], metadatas: List[Dict]):
        """Inserts or updates vectors in the Qdrant collection."""
        points = []
        for i, (content, embedding, metadata) in enumerate(zip(contents, embeddings, metadatas)):
            points.append(models.PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "content": content,
                    **metadata
                }
            ))

        # Use a batch size for upserting to avoid large requests
        batch_size = 100
        for i in range(0, len(points), batch_size):
            self.client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=points[i:i + batch_size]
            )
        print(f"Upserted {len(points)} vectors into '{self.collection_name}'.")

    def search_vectors(self, query_embedding: List[float], limit: int = 3) -> List[Dict]:
        """Searches the Qdrant collection for similar vectors."""
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            append_payload=True # Retrieve the full payload (content, filepath, etc.)
        )
        results = []
        for hit in hits:
            results.append({
    "content": hit.payload["content"],
    "filepath": hit.payload["filepath"],
    "score": hit.score,
    "start_token": hit.payload.get("start_token", ""),
    "end_token": hit.payload.get("end_token", "")
})
        return results

if __name__ == "__main__":
    # Example Usage (requires QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME to be set)
    from dotenv import load_dotenv
    load_dotenv()

    if os.getenv("QDRANT_URL") and os.getenv("QDRANT_API_KEY") and os.getenv("QDRANT_COLLECTION_NAME"):
        vector_store = VectorStore()

        # This will clear existing data in the collection!
        # vector_store.recreate_collection()

        # Dummy data for testing
        test_contents = [
            "Qdrant is a vector similarity search engine.",
            "OpenAI provides powerful language models and embedding APIs.",
            "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python."
        ]
        test_embeddings = [
            [0.1]*1536, # Placeholder embeddings
            [0.2]*1536,
            [0.3]*1536
        ]
        test_metadatas = [
            {"filepath": "test_file_1.md"},
            {"filepath": "test_file_2.md"},
            {"filepath": "test_file_3.md"}
        ]

        # To run this example, you'd need actual embeddings.
        # For now, we'll just show how upsert would be called.
        # vector_store.upsert_vectors(test_contents, test_embeddings, test_metadatas)

        # Dummy query embedding for search
        # query_embedding = [0.15]*1536
        # search_results = vector_store.search_vectors(query_embedding)
        # print("\nSearch Results:")
        # for res in search_results:
        #     print(f"Content: {res['content'][:50]}..., Score: {res['score']:.2f}, File: {res['filepath']}")

    else:
        print("QDRANT_URL, QDRANT_API_KEY, or QDRANT_COLLECTION_NAME not set. Please set them in your .env file or environment variables.")
