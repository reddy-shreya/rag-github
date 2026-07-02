from src.ingestion.repo_loader import clone_repo
from src.ingestion.file_filter import get_relevant_files

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

if __name__ == "__main__":
    main()