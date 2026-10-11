from backend.llm import ask_llm
from backend.repository import load_repository
from backend.chunker import chunk_python_document
from backend.embeddings import embed_chunks
import numpy as np

def main():
    print("Welcome to RepoMind!")



############################################################################
## Testing embedder


document = {
    "path": "example.py",
    "content": """
def greet():
    return "Hello"

def goodbye():
    return "Bye"
"""
}

results = embed_chunks(document)

for result in results:
    print("Function Name:", result["chunk"]["name"])
    print("Embedding Shape:", result["embedding"].shape)
    print("File Path:", result["chunk"]["path"])
    print("------------------------")


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