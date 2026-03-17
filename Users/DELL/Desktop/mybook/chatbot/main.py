import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .document_processor import read_markdown_files, chunk_content
from openai import OpenAI
from .embedding_generator import EmbeddingGenerator
from .vector_store import VectorStore
from typing import List, Optional

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-3.5-turbo")

if not all([OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, CHAT_MODEL]):
    raise ValueError("Missing one or more environment variables.")

# Initialize OpenAI client for chat completions
openai_chat_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Initialize our components
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()

# Pydantic models for request and response
class ChatRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

class IngestResponse(BaseModel):
    message: str

# Helper function to create embeddings

# Helper function to read markdown files and chunk content
def ingest_documents():
    docs_path = "../book/docs/"
    documents = read_markdown_files(docs_path)
    chunks = chunk_content(documents)

    contents = [chunk["content"] for chunk in chunks]
    metadatas = [{"filepath": chunk["filepath"], "start_token": chunk["start_token"], "end_token": chunk["end_token"]} for chunk in chunks]

    # Generate embeddings for all chunks
    embeddings = embedding_generator.generate_embeddings(contents)

    if not embeddings:
        raise Exception("Failed to generate embeddings for documents.")

    # Recreate collection and upsert vectors
    vector_store.recreate_collection()
    vector_store.upsert_vectors(contents, embeddings, metadatas)


# FastAPI endpoints
@app.post("/ingest", response_model=IngestResponse)
async def ingest_content():
    try:
        ingest_documents()
        return IngestResponse(message="Content ingested successfully.")

def create_embedding(text: str) -> List[float]:
    """Helper to create a single embedding."""
    embeddings = embedding_generator.generate_embeddings([text])
    if embeddings:
        return embeddings[0]
    raise Exception("Failed to generate embedding.")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    query_text = request.question
    if request.selected_text:
        query_text = f"Context: {request.selected_text}\nQuestion: {request.question}"

    query_embedding = create_embedding(query_text)

    search_result = vector_store.search_vectors(query_embedding)

    context_chunks = [hit["content"] for hit in search_result]
    sources = [f"{hit["filepath"]}#L{hit["start_token"]}-L{hit["end_token"]}" for hit in search_result]

    context_str = "\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
        {"role": "user", "content": f"Context: {context_str}\nQuestion: {request.question}"}
    ]

    chat_completion = openai_chat_client.chat.completions.create(
        model=CHAT_MODEL,  # Use environment variable for model
        messages=messages
    )

    answer = chat_completion.choices[0].message.content
    return ChatResponse(answer=answer, sources=sources)

# Initialize OpenAI client for chat completions
openai_chat_client = OpenAI(api_key=OPENAI_API_KEY)
