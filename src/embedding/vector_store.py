import chromadb
from src.embedding.embedder import embed_texts

# Initialize persistent ChromaDB client
client = chromadb.PersistentClient(path="vectorstore/")

def get_or_create_collection(name: str):
    """
    Gets existing collection or creates a new one.
    """
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

def add_chunks(chunks: list[dict], collection_name: str):
    """
    Embeds chunks and stores them in ChromaDB collection.
    Skips if collection already has data.
    """
    collection = get_or_create_collection(collection_name)

    # Skip if already embedded
    if collection.count() > 0:
        print(f"Collection '{collection_name}' already has {collection.count()} chunks, skipping embedding.")
        return

    print(f"Embedding {len(chunks)} chunks into '{collection_name}'...")

    texts = [chunk["content"] for chunk in chunks]
    embeddings = embed_texts(texts)

    # ChromaDB requires string IDs
    ids = [f"{collection_name}_{i}" for i in range(len(chunks))]

    # Flatten metadata — ChromaDB only accepts str, int, float, bool
    metadatas = []
    for chunk in chunks:
        meta = {}
        for k, v in chunk["metadata"].items():
            if v is None:
                meta[k] = ""
            else:
                meta[k] = str(v)
        metadatas.append(meta)

    # Add in batches of 500
    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        collection.add(
            ids=ids[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size],
            documents=texts[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size]
        )

    print(f"Stored {len(chunks)} chunks in '{collection_name}' successfully.")

def similarity_search(query: str, collection_name: str, top_k: int = 5) -> list[dict]:
    """
    Embeds query and retrieves top-k most similar chunks.
    """
    collection = get_or_create_collection(collection_name)

    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    # Package results cleanly
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": 1 - results["distances"][0][i]  # cosine similarity
        })

    return chunks