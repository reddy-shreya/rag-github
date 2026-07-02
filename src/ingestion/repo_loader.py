import os
from git import Repo

def clone_repo(repo_url: str, base_dir: str = "data/repos") -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        print(f"Repo already exists at {repo_path}, skipping clone.")
        return repo_path

    os.makedirs(base_dir, exist_ok=True)
    print(f"Cloning {repo_url}...")
    Repo.clone_from(repo_url, repo_path)
    print("Clone complete.")
    return repo_path