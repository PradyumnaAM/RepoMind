import numpy as np

def cosine_similarity(vector_a, vector_b) -> float:
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0

    similarity = dot_product / (magnitude_a * magnitude_b)

    return similarity

def retrieve_chunks(question_embedding, embedded_chunks, k=3):
    results = []

    for item in embedded_chunks:
        code_embedding =  item["embedding"]

        score = cosine_similarity(code_embedding, question_embedding)

        result = {
            "chunk": item["chunk"],
            "score": score
        }
        results.append(result)
        
    ranked_results = sorted(
        results,
        key = lambda item: item["score"],
        reverse = True
    )

    return ranked_results[:k]



