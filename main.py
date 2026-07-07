from src.ingestion.repo_loader import clone_repo
from src.ingestion.file_filter import get_relevant_files
from src.chunking.code_chunker import chunk_code_file
from src.chunking.doc_chunker import chunk_doc_file

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



if __name__ == "__main__":
    main()