from sentence_transformers import SentenceTransformer
from backend.chunker import chunk_python_document

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_chunks(document):
    chunks = chunk_python_document(document)
    contents = []
    results = []

    for chunk in chunks:
        contents.append(chunk["content"])
    
    
    embeddings = embedder.encode(contents)

    for chunk, embedding in zip(chunks, embeddings):
        dictionary = {
            "chunk" : chunk,
            "embedding" : embedding 
        }

        results.append(dictionary)
    return results





    

        
