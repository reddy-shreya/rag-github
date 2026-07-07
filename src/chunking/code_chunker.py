import os
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_java as tsjava
import tree_sitter_cpp as tscpp
import tree_sitter_go as tsgo
import tree_sitter_rust as tsrust
import tree_sitter_typescript as tstypescript

# Map file extensions to tree-sitter language modules
LANGUAGE_MAP = {
    ".py": tspython.language(),
    ".js": tsjavascript.language(),
    ".jsx": tsjavascript.language(),
    ".java": tsjava.language(),
    ".cpp": tscpp.language(),
    ".c": tscpp.language(),
    ".go": tsgo.language(),
    ".rs": tsrust.language(),
    ".ts": tstypescript.language_typescript(),
    ".tsx": tstypescript.language_tsx(),
}

# Node types we want to extract as chunks
CHUNK_NODE_TYPES = {
    "function_definition",      # Python
    "class_definition",         # Python
    "function_declaration",     # JS, Java, Go
    "method_declaration",       # Java
    "class_declaration",        # JS, Java
    "impl_item",                # Rust
    "function_item",            # Rust
    "arrow_function",           # JS
}

def get_parser(extension: str):
    lang = LANGUAGE_MAP.get(extension)
    if lang is None:
        return None
    return Parser(Language(lang))

def chunk_code_file(file_path: str) -> list[dict]:
    """
    Parses a code file using tree-sitter and extracts
    functions/classes as individual chunks with metadata.
    """
    ext = os.path.splitext(file_path)[1].lower()
    parser = get_parser(ext)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source_code = f.read()

    # If no parser available, fall back to line-based chunking
    if parser is None:
        return line_based_chunk(file_path, source_code)

    tree = parser.parse(bytes(source_code, "utf-8"))
    chunks = []
    extract_chunks(tree.root_node, source_code, file_path, chunks)

    # If AST found no meaningful nodes, fall back to line-based
    if not chunks:
        return line_based_chunk(file_path, source_code)

    return chunks

def extract_chunks(node, source_code: str, file_path: str, chunks: list):
    """
    Recursively walks AST nodes and extracts meaningful chunks.
    """
    if node.type in CHUNK_NODE_TYPES:
        chunk_text = source_code[node.start_byte:node.end_byte]
        
        # Try to get name of function/class
        name = None
        for child in node.children:
            if child.type == "identifier":
                name = source_code[child.start_byte:child.end_byte]
                break

        chunks.append({
            "content": chunk_text,
            "metadata": {
                "file_path": file_path,
                "chunk_type": node.type,
                "name": name,
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "source_type": "code"
            }
        })

    for child in node.children:
        extract_chunks(child, source_code, file_path, chunks)

def line_based_chunk(file_path: str, source_code: str, lines_per_chunk: int = 40) -> list[dict]:
    """
    Fallback chunker — splits file into chunks of N lines.
    """
    lines = source_code.split("\n")
    chunks = []

    for i in range(0, len(lines), lines_per_chunk):
        chunk_lines = lines[i:i + lines_per_chunk]
        chunk_text = "\n".join(chunk_lines)

        if chunk_text.strip():
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "file_path": file_path,
                    "chunk_type": "line_chunk",
                    "name": None,
                    "start_line": i + 1,
                    "end_line": min(i + lines_per_chunk, len(lines)),
                    "source_type": "code"
                }
            })

    return chunks