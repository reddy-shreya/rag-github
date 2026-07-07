import os
import tiktoken

def chunk_doc_file(file_path: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Reads a documentation file and splits it into
    overlapping token-based chunks.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if not content.strip():
        return []

    # Use tiktoken to split by tokens
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)

        if chunk_text.strip():
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "file_path": file_path,
                    "chunk_type": "doc_chunk",
                    "name": os.path.basename(file_path),
                    "start_token": start,
                    "end_token": end,
                    "source_type": "doc"
                }
            })

        start += chunk_size - overlap

    return chunks