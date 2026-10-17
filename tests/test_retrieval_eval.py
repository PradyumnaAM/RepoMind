from backend.embeddings import embed_question
from backend.vector_store import search_chunks
from backend.vector_store import get_collection

test_cases = [
    {
        "question": "Which function splits long code chunks?",
        "expected_function": "split_long_chunk"
    },
    {
        "question": "Which function generates embeddings for code?",
        "expected_function": "embed_chunks"
    },
    {
        "question": "Which function loads repository files?",
        "expected_function": "load_repository"
    },
    {
        "question": "Which function stores chunks in the vector database?",
        "expected_function": "store_chunks"
    },
    {
        "question": "Which function builds context for the LLM?",
        "expected_function": "build_context"
    }
]

collection = get_collection()

matches = collection.get(
    where={"name": "build_context"},
    include=["metadatas", "documents"]
)

print("Indexed build_context chunks:", len(matches["ids"]))

for metadata in matches["metadatas"]:
    print(metadata)

correct = 0
total = len(test_cases)

for test in test_cases:
    embedded = embed_question(test["question"])
    results = search_chunks(embedded, k=10)
    retrieved_names = []
    for metadata in results["metadatas"][0]:
        retrieved_names.append(metadata["name"])

    if test["expected_function"] in retrieved_names:
        correct += 1
        print("PASS")
    else:
        for rank, name in enumerate(retrieved_names, start=1):
            print(f"{rank}. {name}")
        print(f"FAIL: {test['question']}")
        print(f"Expected: {test['expected_function']}")
        print(f"Retrieved: {retrieved_names}")
        print()

hit_3 = (correct/total) * 100
print(f"Hit@3: {hit_3:.1f}%")


    
