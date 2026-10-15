# RepoMind

**Ask questions about a local Python codebase using retrieval-augmented generation (RAG).**

RepoMind is a local-first, command-line codebase assistant. Point it at a repository, index its Python code, and ask natural-language questions about functions, classes, configuration, and implementation details. It retrieves relevant code snippets from ChromaDB and uses a locally served Ollama language model to generate a grounded response.

> **Status:** Working prototype / MVP in development. Python indexing and question answering work end to end; retrieval coverage, evaluation, and developer experience are still being improved.

## Why RepoMind?

Understanding an unfamiliar codebase usually means opening many files, searching for function names, and reconstructing how pieces fit together. RepoMind experiments with a simpler workflow: index the source once, then ask questions in plain English.

Unlike sending an entire repository to an LLM, RepoMind embeds smaller code sections and retrieves a limited set of relevant snippets for each question.

## Features

- **Recursive repository loading** with file extension, directory, and size filters.
- **Python AST-based chunking** of top-level functions, class methods, and top-level assignments.
- **Token-aware splitting** for large chunks, with overlapping windows.
- **Local semantic embeddings** using `sentence-transformers/all-MiniLM-L6-v2`.
- **Persistent vector search** with ChromaDB.
- **Local LLM responses** via Ollama's OpenAI-compatible API (configured for `qwen3:4b`).
- **Interactive CLI** for indexing a repository and asking questions.
- **Grounding instructions** that tell the model to use retrieved repository context and acknowledge insufficient information.

## Architecture

```text
Repository directory
       |
       v
File discovery and filtering (repository.py)
       |
       v
Python AST chunking (chunker.py)
       |
       v
Token-aware splitting + MiniLM embeddings (embeddings.py)
       |
       v
Persistent ChromaDB collection (vector_store.py)
       |
       +--------------------------------+
                                        |
User question                           |
       |                                |
       v                                |
Question embedding                      |
       |                                |
       v                                |
Similarity search <---------------------+
       |
       v
Top-k code snippets + metadata
       |
       v
RAG prompt (rag.py)
       |
       v
Ollama / qwen3:4b (llm.py)
       |
       v
Answer in terminal
```

The retrieval pipeline is **stateless**: each question is handled independently, without previous chat history.

## Tech stack

| Area | Technology |
| --- | --- |
| Language | Python |
| Code parsing | Python built-in `ast` |
| Embeddings | Sentence Transformers / `all-MiniLM-L6-v2` |
| Vector database | ChromaDB (persistent local storage) |
| Language model | Ollama / `qwen3:4b` |
| LLM client | OpenAI Python SDK, using Ollama's compatible endpoint |
| Numerical operations | NumPy |
| Tests | pytest (tests are included; passing status is not asserted here) |

## Getting started

### Prerequisites

- Python 3.12 is the development environment used for this project; other versions have not been verified.
- [Ollama](https://ollama.com/) installed and running locally.
- An internet connection for the initial embedding-model download, unless the model is already cached.

### 1. Clone the repository

```bash
git clone https://github.com/PradyumnaAM/RepoMind.git
cd RepoMind
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

The repository's `requirements.txt` has not yet been populated. Install the packages used by the current implementation:

```bash
python -m pip install sentence-transformers chromadb openai numpy pytest
```

Dependency versions are not pinned yet; reproducible installation across environments is still a TODO.

### 4. Prepare the local LLM

```bash
ollama pull qwen3:4b
```

Ensure the Ollama service is running at `http://localhost:11434`. Depending on your installation, Ollama may already run as a background service; otherwise start it with:

```bash
ollama serve
```

The current model name and endpoint are configured in `backend/llm.py`.

### 5. Run RepoMind

From the **repository root**, run:

```bash
python -m backend.main
```

Using `-m backend.main` ensures imports such as `from backend.indexer import index_repository` resolve correctly.

## Usage

The CLI offers three choices:

```text
Welcome to RepoMind!
Enter 1 for: Indexing your repository:
Enter 2 to ask the LLM a question about your repository:
Enter 3 to exit the program:
Choose an option:
```

**Index a repository:** Select `1` and enter the full path to a local repository. For example:

```text
Choose an option: 1
Please enter your repository path: C:\Projects\my-python-app
Files indexed: 5
Chunks stored: 15
```

*The counts above are illustrative; actual results depend on the repository.*

**Ask a question:** Select `2` after indexing:

```text
Choose an option: 2
Enter your question: Which function loads repository files?
```

Other useful questions to try:

- Which function filters unsupported file extensions?
- Where is the vector database initialized?
- How are embeddings generated?
- Which functions are involved in answering a question?
- What configuration values are defined in this module?

**Exit:** Select `3`.

### Indexing behavior

- The current indexer **only embeds Python (`.py`) documents**, even though the loader accepts additional extensions.
- A Python file without supported AST chunks may not count as an indexed file.
- Re-indexing **replaces the previous ChromaDB collection**. RepoMind currently supports one indexed repository at a time.
- ChromaDB persists data under `./data/chroma` relative to the working directory. You generally do not need to re-index merely because the CLI restarted.
- If source files change, re-index to refresh the stored code.

## Project structure

```text
RepoMind/
├── backend/
│   ├── main.py          # Interactive command-line entry point
│   ├── repository.py    # File discovery, filtering, and loading
│   ├── chunker.py       # Python AST code chunk extraction
│   ├── embeddings.py    # Token splitting and vector embeddings
│   ├── indexer.py       # Repository indexing pipeline
│   ├── vector_store.py  # ChromaDB persistence and similarity search
│   ├── retrieval.py     # NumPy cosine-similarity retrieval helper
│   ├── rag.py           # Retrieved-context formatting and RAG prompt
│   └── llm.py           # Ollama/OpenAI-compatible model client
├── tests/
│   ├── test_chunker.py
│   └── test_embeddings.py
├── data/
│   └── chroma/          # Local vector database (generated data)
├── requirements.txt     # Dependency manifest (currently empty)
└── README.md
```

## How it works

### 1. Discover files

`backend/repository.py` walks the repository and filters files by extension and size (1 MB maximum per file). It excludes paths containing `.git`, `.venv`, `venv`, `node_modules`, or `__pycache__`. The loader can read several common source and text extensions, but only `.py` files currently proceed through indexing.

### 2. Extract code chunks

`backend/chunker.py` parses Python source with `ast.parse`. It extracts top-level functions (including async functions), methods inside top-level classes, and top-level assignments. Chunks include a relative file path, a name, a type, code content, and available source-line metadata.

### 3. Embed chunks

`backend/embeddings.py` uses the MiniLM sentence-transformer model to embed code. Long chunks are divided into overlapping token windows before embedding.

### 4. Store and retrieve

`backend/vector_store.py` saves code text, embeddings, and selected metadata in the persistent `repomind_code` ChromaDB collection. For a user question, RepoMind embeds the question and retrieves the nearest `k` chunks (the CLI currently uses `k=5`).

### 5. Generate an answer

`backend/rag.py` builds a prompt containing retrieved file/function labels and code. `backend/llm.py` sends that prompt to `qwen3:4b` via Ollama and returns the generated text.

## Current limitations

RepoMind is a learning-oriented MVP, not yet a production code-search service.

- **Python-only indexing:** Other extensions are loadable but not embedded by the current indexer.
- **Incomplete code coverage:** Imports, standalone expressions, nested functions, and other constructs may not be captured as independent chunks.
- **Top-k retrieval is not a complete repository inventory:** Questions such as “list every file” may omit files because only a few relevant chunks reach the model.
- **No conversational memory:** Follow-up questions do not automatically retain earlier context.
- **No incremental indexing:** Re-indexing processes the repository again and replaces the stored collection.
- **Limited source citations:** File names appear in prompts, but answers do not yet have a structured, verified file-and-line citation system.
- **Tokenizer warnings:** Long input tokenization can produce max-length warnings; final chunk lengths and behavior still need explicit validation.
- **Local resource requirements:** Indexing speed and LLM response time depend on model availability and hardware.
- **No evaluation benchmark yet:** Retrieval quality and answer accuracy have not been systematically measured.

## Testing

Tests currently live in `tests/test_chunker.py` and `tests/test_embeddings.py`.

To run them from the project root:

```bash
python -m pytest tests/ -v
```

These tests have not been independently executed or verified as passing as part of this documentation update. End-to-end testing also requires a running Ollama service and an available embedding model.

## Roadmap

- [ ] Validate token-window sizes and resolve noisy tokenizer warnings
- [ ] Improve chunk coverage and preserve precise source-line references
- [ ] Add repository-wide metadata and file-list queries
- [ ] Improve retrieval relevance and evaluate grounded answer quality
- [ ] Expand automated unit and integration tests
- [ ] Add incremental indexing and support for multiple repositories
- [ ] Add optional conversation history and follow-up-aware retrieval
- [ ] Add configuration management, error handling, and progress reporting
- [ ] Populate and pin dependencies in `requirements.txt`
- [ ] Add a proper `.gitignore` and stop tracking generated artifacts

## Security and privacy notes

RepoMind is designed to run embeddings, vector storage, and LLM inference locally. The first use of the sentence-transformer model may contact Hugging Face to download or check model files. Avoid indexing secrets, credentials, or sensitive code you are not authorized to process. Treat repository contents as untrusted data: retrieved source code should not be followed as instructions.

## Author

Developed by [PradyumnaAM](https://github.com/PradyumnaAM).

---

**RepoMind** — exploring practical code intelligence with Python, AST parsing, embeddings, vector search, and local LLMs.
