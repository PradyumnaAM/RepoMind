from backend.llm import ask_llm
from backend.repository import load_repository
from backend.chunker import chunk_python_document
from backend.embeddings import embed_chunks, embed_question, split_long_chunk, count_tokens
from backend.retrieval import retrieve_chunks
from backend.vector_store import get_collection, store_chunks,search_chunks,reset_storage
from backend.rag import answer_question
from backend.indexer import index_repository
import numpy as np


def main():
    print("Welcome to RepoMind!")

    while True:
        print("Enter 1 for: Indexing your repository: ")
        print("Enter 2 to ask the LLM a question about your repository: ")
        print("Enter 3 to exit the program: ")
        choice = input("Choose an option: ")

        if choice == "1":
            repo_path = input("Please enter your repository path: ")
            try:
                result = index_repository(repo_path)
                print(f"Files indexed: {result['files_indexed']}")
                print(f"Chunks stored: {result['chunks_stored']}")
            except ValueError as error:
                print(f"Indexing Failed: {error}")
            
        elif choice == "2":
            user_question = input("Enter your question: ").strip()
            if not user_question:
                print("Please enter a valid question.")
                continue
            answer = answer_question(user_question, k=5)
            print(f"Repo Mind: {answer}")

        elif choice == "3":
            print("Goodbye! Thanks for using RepoMind.")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()

############################################################################
## Testing question on repository

    # print("Welcome to RepoMind!")


    # question = "Which function loads repository files and filters unsupported extensions?"

    # answer = answer_question(question, k=5)

    # print("\n===== REPOMIND ANSWER =====")
    # print(answer)

############################################################################
## Testing RAG implementation with LLM

    # document = {
    #     "path": "example.py",
    #     "content": """
    # def authenticate_user(username, password):
    #     return username == "admin" and password == "secret"

    # def calculate_total(prices):
    #     return sum(prices)

    # def send_notification(message):
    #     print(message)
    # """
    # }


    # question = "Where does the application check login credentials?"

    # answer = answer_question(question, k=3)

    # print("\n===== REPOMIND ANSWER =====")
    # print(answer)

############################################################################

## Testing chromabase deletion

    # document = {
    #     "path": "example.py",
    #     "content": """
    # def authenticate_user(username, password):
    #     return username == "admin" and password == "secret"

    # def calculate_total(prices):
    #     return sum(prices)

    # def send_notification(message):
    #     print(message)
    # """
    # }

    # embedded_chunks = embed_chunks(document)

    # collection = get_collection()
    # print("Before reset:", collection.count())

    # collection = reset_storage()
    # print("After reset:", collection.count())

    # store_chunks(embedded_chunks)
    # print("After re-indexing:", collection.count())


############################################################################
## Testing vectorbase search

    # question = "Where does the application check login credentials?"

    # question_embedding = embed_question(question)

    # results = search_chunks(question_embedding, k=3)

    # for i, metadata in enumerate(results["metadatas"][0]):
    #     print("Function:", metadata["name"])
    #     print("File:", metadata["path"])
    #     print("Distance:", results["distances"][0][i])
    #     print("Code:", results["documents"][0][i])
    #     print("----------------------")


############################################################################
## Testing vector database

    # document = {
    #     "path": "example.py",
    #     "content": """
    # def authenticate_user(username, password):
    #     return username == "admin" and password == "secret"

    # def calculate_total(prices):
    #     return sum(prices)

    # def send_notification(message):
    #     print(message)
    # """
    # }

    # embedded_chunks = embed_chunks(document)
    # stored_count = store_chunks(embedded_chunks)

    # collection = get_collection()

    # print("Stored this run:", stored_count)
    # print("Total database records:", collection.count())

############################################################################
## Testing embedding and chunking 

    # long_function = """def process_large_dataset():
    #     total = 0
    #     records = []
    #     for item in range(100):
    #         value = item * 2
    #         records.append(value)
    #         total += value
    #     return total, records
    # """

    # document = {
    #     "path": "test_repository.py",
    #     "content": (
    #         """def greet(name):
    #     return f"Hello, {name}!"


    # def authenticate_user(username, password):
    #     if not username or not password:
    #         return False
    #     return username == "admin" and password == "secret"


    # """
    #         + long_function
    #         + "\n    # Additional processing\n"
    #         + "    total += 1\n" * 150
    #     )
    # }

    # results = embed_chunks(document)

    # print("\n===== DAY 4 FINAL TEST =====")
    # print("Total embedded chunks:", len(results))

    # for i, result in enumerate(results, start=1):
    #     chunk = result["chunk"]
    #     embedding = result["embedding"]

    #     print(f"\nChunk {i}")
    #     print("Function:", chunk["name"])
    #     print("File:", chunk["path"])
    #     print("Embedding dimensions:", len(embedding))
    #     print("Token count:", count_tokens(chunk["content"]))

    #     assert len(embedding) == 384, "Incorrect embedding dimensions"
    #     assert count_tokens(chunk["content"]) <= 256, "Chunk exceeds token limit"

    # assert len(results) > 0, "No chunks were embedded"

    # print("\nDAY 4 TEST PASSED!")

############################################################################

## Testing splitting chunks intp smaller chunks with offsets

    # text = "def greet():\n    print('Hello')\n" * 100

    # chunks = split_long_chunk(text)

    # print("Number of chunks:", len(chunks))

    # for chunk in chunks:
    #     print("Type:", type(chunk))
    #     print("Token count:", count_tokens(chunk))


############################################################################

## Testing spliting chunks into smaller chunks

    # text = "This is a test sentence. " * 100

    # chunks = split_long_chunk(text)

    # print("Number of chunks:", len(chunks))

    # for chunk in chunks:
    #     print("Type:", type(chunk))
    #     print("Token count:", count_tokens(chunk))

############################################################################

## Testing retrival and embedding

    # document = {
    #     "path": "example.py",
    #     "content": """
    # def authenticate_user(username, password):
    #     return username == "admin" and password == "secret"

    # def calculate_total(prices):
    #     return sum(prices)

    # def send_notification(message):
    #     print(message)

    # def get_user_profile(user_id):
    #     return {"id": user_id, "name": "Alex"}
    # """
    # }

    # embedded_chunks = embed_chunks(document)
    # question = "Where does the application check login credentials?"

    # question_embedding = embed_question(question)
    # top_chunks = retrieve_chunks(question_embedding,embedded_chunks, k=5)

    # for result in top_chunks:
    #     print(result["chunk"]["name"])
    #     print(result["score"])
    #     print(result["chunk"]["path"])
    #     print(round(result["score"], 4))



############################################################################
## Testing embedder


    # document = {
    #     "path": "example.py",
    #     "content": """
    # def greet():
    #     return "Hello"

    # def goodbye():
    #     return "Bye"
    # """
    # }

    # results = embed_chunks(document)

    # for result in results:
    #     print("Function Name:", result["chunk"]["name"])
    #     print("Embedding Shape:", result["embedding"].shape)
    #     print("File Path:", result["chunk"]["path"])
    #     print("------------------------")


############################################################################

###### TESTING ALL FUNCTIONS TILL NOW

    # document = {
    #     "path": "sample.py",
    #     "content": '''DATABASE_URL = "sqlite:///app.db"

    # @decorator_one
    # @decorator_two
    # def greet():
    #     return "Hello"

    # DEBUG = True

    # class UserService:
    #     @staticmethod
    #     def get_user():
    #         return "Alice"

    # async def fetch_data():
    #     return "Data loaded"
    # '''
    # }

    # chunks = chunk_python_document(document)

    # print(f"Total no.of chunks: {len(chunks)}")
    # for chunk in chunks:
    #     print(chunk["type"])
    #     print(chunk["name"])
    #     print(chunk["start_line"])
    #     print(chunk["end_line"])
    #     print(chunk["content"])


############################################################################
## Testing the decorated function chunker

    # document = {
    #     "path": "example.py",
    #     "content": """@decorator_one
    # @decorator_two
    # def greet():
    #     return "Hello"
    # """
    # }

    # chunks = chunk_python_document(document)

    # for chunk in chunks:
    #     print(chunk["start_line"])
    #     print(chunk["content"])

############################################################################

## Testing error handling

    # documents = [
    #     {
    #         "path": "broken.py",
    #         "content": "def broken(\n    return 100"
    #     },
    #     {
    #         "path": "working.py",
    #         "content": "def add(a, b):\n    return a + b"
    #     }
    # ]

    # all_chunks = []

    # for document in documents:
    #     chunks = chunk_python_document(document)
    #     all_chunks.extend(chunks)

    # print("Total chunks:", len(all_chunks))

    # for chunk in all_chunks:
    #     print(chunk["path"], chunk["name"])

############################################################################

## Testing assignment seperate chunks and function seperate chunk

    # document = {
    #     "path": "config.py",
    #     "content": """DATABASE_URL = "sqlite:///database.db"

    # def connect():
    #     print("Connecting to database")

    # DEBUG = True
    # """
    # }

    # chunks = chunk_python_document(document)

    # for chunk in chunks:
    #     if chunk["type"] == "configuration":
    #         print(chunk["source_ranges"])


############################################################################

## Testing assigned variables into chunks

    # document = {
    #     "path": "config.py",
    #     "content": """DATABASE_URL = "sqlite:///database.db"
    # DEBUG = True
    # MAX_CONNECTIONS = 10
    # """
    # }

    # chunks = chunk_python_document(document)

    # for chunk in chunks:
    #     print("Type:", chunk["type"])
    #     print("Name:", chunk["name"])
    #     print("Lines:", chunk["start_line"], "-", chunk["end_line"])
    #     print("Content:")
    #     print(chunk["content"])


############################################################################

##  Test for async function chunker

    # document = {
    #     "path": "example.py",
    #     "content": 
    #     """class UserService:
    #     async def fetch_user(self):
    #         return {"name": "Alex"}

    #     async def fetch_data():
    #         return [1, 2, 3]
    #     """
    # }

    # chunks = chunk_python_document(document)

    # for chunk in chunks:
    #     print(chunk["type"], chunk["name"])
    #     print("Lines:", chunk["start_line"], "-", chunk["end_line"])
    #     print()

############################################################################

##  Test for chunker with class name and method

    # document = {
    #         "path": "example.py",
    #         "content": """
    # class UserService:
    #     database = "postgres"

    #     def get_user(self):
    #         pass

    #     def delete_user(self):
    #         pass

    # def calculate_total(items):
    #     return sum(items)
    # """
    # }

    # chunks = chunk_python_document(document)

    # for chunk in chunks:
    #     print(chunk["type"], chunk["name"])
    #     print("Lines:", chunk["start_line"], "-", chunk["end_line"])
    #     print()

############################################################################

##  Test for llm.py

    # while True:
    #     user_question = input("user: ")
    #     if user_question.strip().lower() in ("goodbye", "bye", "exit"):
    #         print("RepoMind: Goodbye!")
    #         break
    #     if user_question.strip() == "":
    #         print("Please enter a question!")
    #         continue
    #     answer = ask_llm(user_question)
    
    #     print("RepoMind: ", answer)

############################################################################

if __name__ == "__main__":
    main()