from pathlib import Path

from backend.repository import load_repository
from backend.embeddings import embed_chunks
from backend.vector_store import store_chunks, reset_storage

def index_repository(repo_path):
    repo = Path(repo_path)

    if not repo.is_dir():
        raise ValueError("Invalid repository directory")

    documents = load_repository(repo_path)

    all_embedded_chunks = []
    files_indexed = 0

    for document in documents:
        if Path(document["path"]).suffix != ".py":
            continue

        embedded_document = embed_chunks(document)

        if not embedded_document:
            continue

        all_embedded_chunks.extend(embedded_document)

        files_indexed += 1

    if not all_embedded_chunks:
        raise ValueError("No Python code chunks found to index")

    reset_storage()
    store = store_chunks(all_embedded_chunks)

    results = {
        "files_indexed" : files_indexed,
        "chunks_stored": len(all_embedded_chunks)
    }
    
    return results