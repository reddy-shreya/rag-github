import os

CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".go", ".rs", ".rb", ".cs"}
DOC_EXTENSIONS = {".md", ".rst", ".txt"}

IGNORE_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv",
    "venv", "env", "dist", "build", ".next", ".nuxt",
    "coverage", ".pytest_cache", ".mypy_cache", "target",
    "static", "assets", "public"
}

def get_relevant_files(repo_path:str)->dict:
    code_files=[]
    doc_files=[]

    for root,dirs,files in os.walk(repo_path):
        dirs[:]=[d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext=os.path.splitext(file)[1].lower()
            full_path=os.path.join(root,file)

            if ext in CODE_EXTENSIONS:
                code_files.append(full_path)
            elif ext in DOC_EXTENSIONS:
                doc_files.append(full_path)
    return{"code": code_files,"docs":doc_files}

