from sentence_transformers import SentenceTransformer
from backend.chunker import chunk_python_document

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(document):
    chunks = chunk_python_document(document)
    contents = []
    results = []
    processed_chunks = []

    for chunk in chunks:
        content = chunk["content"]

        if is_chunk_too_long(content):
            smaller_chunks = split_long_chunk(content)

            for small_chunk in smaller_chunks:
                new_chunk = chunk.copy()
                new_chunk["content"] = small_chunk
                processed_chunks.append(new_chunk)
        else:
            processed_chunks.append(chunk)

    for processed_chunk in processed_chunks:
        contents.append(processed_chunk["content"])   
    embeddings = embedder.encode(contents)

    for processed_chunk, embedding in zip(processed_chunks, embeddings):
        dictionary = {
            "chunk" : processed_chunk,
            "embedding" : embedding

        }

        results.append(dictionary)
    return results


def embed_question(question):
    return embedder.encode(question)

def count_tokens(text) -> int:
    tokens = embedder.tokenizer.encode(text)
    return len(tokens)

def is_chunk_too_long(text) -> bool:
    tokens = embedder.tokenizer.encode(text, verbose=False)
    return len(tokens) > embedder.max_seq_length
    
def split_long_chunk(text, chunk_size=200, overlap=40):
    encoded = embedder.tokenizer(
        text,
        add_special_tokens=False,
        return_offsets_mapping=True,
        verbose = False
    )

    offsets = encoded["offset_mapping"]
    step_size = chunk_size - overlap
    small_chunks = []
    start = 0
    while start < len(offsets):
        end = start + chunk_size
        start_char = offsets[start][0]
        last_token_index = min(end, len(offsets)) - 1
        end_char = offsets[last_token_index][1]
        
        text_chunk = text[start_char:end_char]

        small_chunks.append(text_chunk)

        if end >= len(offsets):
            break

        start += step_size  

    return small_chunks

    

        
