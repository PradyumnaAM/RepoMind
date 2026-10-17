import string
from backend.vector_store import get_collection, store_chunks

def keyword_score(question: str, metadata: dict) -> int:
    # Step 1: Convert question to lowercase
    question = question.lower()
    score = 0

    name = metadata["name"].lower()

    clean_name = name.replace("_", " ")
    
    split = clean_name.split()
    mapping = str.maketrans('', '', string.punctuation)
    ques_clean = question.translate(mapping)
    ques_words = ques_clean.split()
    
    for word in split:
        if word in ques_words:
            score += 1


    return score

def keyword_search(question: str, k: int = 5) -> list:
    collection = get_collection()

    results = collection.get(
        include=["documents", "metadatas"]
    )

    # Step 3: Calculate keyword_score for each chunk
    scores = []
    for metadata, document in zip(results["metadatas"], results["documents"]):
        score = keyword_score(question, metadata)
        if score > 0:
            scores.append(
                {
                    "score" : score,
                    "metadata": metadata,
                    "document": document
                }
            )


    scores.sort(key=lambda item: item["score"], reverse = True)

    return scores[:k]

