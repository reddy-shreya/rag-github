from src.ingestion.repo_loader import clone_repo
from src.ingestion.file_filter import get_relevant_files
from src.chunking.code_chunker import chunk_code_file
from src.chunking.doc_chunker import chunk_doc_file
from src.embedding.vector_store import add_chunks,similarity_search

def main():
    repo_url = input("Enter GitHub repo URL: ").strip()
    
    repo_path = clone_repo(repo_url)
    files = get_relevant_files(repo_path)
    
    print(f"\n--- Ingestion Summary ---")
    print(f"Code files (.py): {len(files['code'])}")
    print(f"Doc files (.md/.rst): {len(files['docs'])}")
    
    print(f"\nSample code files:")
    for f in files['code'][:5]:
        print(f"  {f}")
    
    print(f"\nSample doc files:")
    for f in files['docs'][:5]:
        print(f"  {f}")

    print(f"\nChunking code files...")
    code_chunks = []
    for file_path in files['code']:
        chunks = chunk_code_file(file_path)
        code_chunks.extend(chunks)
    
    # Chunk doc files
    print(f"Chunking doc files...")
    doc_chunks = []
    for file_path in files['docs']:
        chunks = chunk_doc_file(file_path)
        doc_chunks.extend(chunks)

    print(f"\n--- Chunking Summary ---")
    print(f"Total code chunks: {len(code_chunks)}")
    print(f"Total doc chunks: {len(doc_chunks)}")

    print(f"\nSample code chunk:")
    if code_chunks:
        sample = code_chunks[0]
        print(f"  File: {sample['metadata']['file_path']}")
        print(f"  Type: {sample['metadata']['chunk_type']}")
        print(f"  Name: {sample['metadata']['name']}")
        print(f"  Lines: {sample['metadata']['start_line']} - {sample['metadata']['end_line']}")
        print(f"  Content preview: {sample['content'][:100]}...")

    print(f"\nSample doc chunk:")
    if doc_chunks:
        sample = doc_chunks[0]
        print(f"  File: {sample['metadata']['file_path']}")
        print(f"  Type: {sample['metadata']['chunk_type']}")
        print(f"  Content preview: {sample['content'][:100]}...")

    # Day 3 — Embedding + Vector Store
    print(f"\n--- Embedding + Storing ---")
    add_chunks(code_chunks, "code_chunks")
    add_chunks(doc_chunks, "doc_chunks")

    # Test similarity search
    print(f"\n--- Similarity Search Test ---")
    query = "how does FastAPI handle request validation?"
    print(f"Query: {query}\n")

    print("Top 3 code results:")
    code_results = similarity_search(query, "code_chunks", top_k=3)
    for i, result in enumerate(code_results):
        print(f"  {i+1}. {result['metadata']['file_path']}")
        print(f"     Function: {result['metadata']['name']}")
        print(f"     Score: {result['score']:.3f}")
        print(f"     Preview: {result['content'][:80]}...")

    print("\nTop 3 doc results:")
    doc_results = similarity_search(query, "doc_chunks", top_k=3)
    for i, result in enumerate(doc_results):
        print(f"  {i+1}. {result['metadata']['file_path']}")
        print(f"     Score: {result['score']:.3f}")
        print(f"     Preview: {result['content'][:80]}...")

if __name__ == "__main__":
    main()