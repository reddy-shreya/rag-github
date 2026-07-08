from sentence_transformers import SentenceTransformer

# Load model once at module level so it doesn't reload every call
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str], batch_size: int = 64) -> list[list[float]]:
    """
    Takes a list of strings and returns their embeddings.
    Processes in batches to avoid memory issues on large repos.
    """
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = model.encode(batch, show_progress_bar=False)
        all_embeddings.extend(embeddings.tolist())

    return all_embeddings