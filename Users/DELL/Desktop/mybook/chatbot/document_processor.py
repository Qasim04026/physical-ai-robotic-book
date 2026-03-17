import os
import re
import markdown
import tiktoken
from typing import List, Dict

def read_markdown_files(directory: str) -> List[Dict[str, str]]:
    """Reads all markdown files from a directory and returns their content."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append({"filepath": filepath, "content": content})
    return documents

def chunk_content(documents: List[Dict[str, str]], max_tokens: int = 500, overlap: int = 50) -> List[Dict[str, str]]:
    """Chunks document content into smaller pieces based on token count."""
    tokenizer = tiktoken.get_encoding("cl100k_base")
    chunks = []
    for doc in documents:
        content = doc["content"]
        filepath = doc["filepath"]

        # Convert markdown to plain text to get a more accurate token count for content
        plain_text = re.sub(r'<[^>]+>', '', markdown.markdown(content))
        tokens = tokenizer.encode(plain_text)

        i = 0
        while i < len(tokens):
            chunk_tokens = tokens[i : i + max_tokens]
            chunk_text = tokenizer.decode(chunk_tokens)
            chunks.append({
                "filepath": filepath,
                "content": chunk_text,
                "start_token": i,
                "end_token": i + len(chunk_tokens)
            })
            i += (max_tokens - overlap)
            if max_tokens - overlap <= 0: # Avoid infinite loop if overlap >= max_tokens
                i += max_tokens
    return chunks

if __name__ == "__main__":
    # Example Usage:
    # Assuming your book/docs directory is at the parent level
    docs_directory = "../book/docs/"
    if os.path.exists(docs_directory):
        print(f"Reading markdown files from: {docs_directory}")
        documents = read_markdown_files(docs_directory)
        print(f"Found {len(documents)} documents.")

        if documents:
            chunks = chunk_content(documents)
            print(f"Generated {len(chunks)} chunks.")
            # for i, chunk in enumerate(chunks[:5]): # Print first 5 chunks
            #     print(f"--- Chunk {i+1} from {chunk['filepath']} ---")
            #     print(chunk['content'][:200]) # Print first 200 chars of chunk
            #     print("\n")
        else:
            print("No documents found to chunk.")
    else:
        print(f"Directory not found: {docs_directory}")
        print("Please ensure the '../book/docs/' directory exists relative to the chatbot folder.")
