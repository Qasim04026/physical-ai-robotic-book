import os
from openai import OpenAI
from typing import List, Dict

class EmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-ada-002"

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts using OpenAI API."""
        if not texts:
            return []
        try:
            response = self.client.embeddings.create(input=texts, model=self.model)
            return [d.embedding for d in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []

if __name__ == "__main__":
    # Example Usage (requires OPENAI_API_KEY to be set in environment)
    from dotenv import load_dotenv
    load_dotenv()

    if os.getenv("OPENAI_API_KEY"):
        embedding_generator = EmbeddingGenerator()
        test_texts = [
            "This is a test sentence.",
            "Another sentence for embedding."
        ]
        embeddings = embedding_generator.generate_embeddings(test_texts)

        if embeddings:
            print(f"Generated {len(embeddings)} embeddings. Each embedding has dimension {len(embeddings[0])}.")
            # print(embeddings[0][:5]) # Print first 5 dimensions of the first embedding
        else:
            print("Failed to generate embeddings.")
    else:
        print("OPENAI_API_KEY not set. Please set it in your .env file or environment variables.")
