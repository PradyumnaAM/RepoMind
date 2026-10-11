from pathlib import Path

MAX_FILE_SIZE = 1000000
IGNORED_DIRECTORIES = {".git",".venv","venv","node_modules","__pycache__"}
ALLOWED_EXTENSIONS = {".py",".js",".jsx",".ts",".tsx",".java",".html",".css",".sql",".md",".json",".yaml",".yml",}

def should_ignore_file(file_path: Path) -> bool:
    for file in file_path.parts:
        if file in IGNORED_DIRECTORIES:
            return True
        
    return False

def is_allowed_file(file_path: Path) -> bool:
    if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
        return True
    return False

def is_file_too_large(file_path: Path) -> bool:
    return file_path.stat().st_size > MAX_FILE_SIZE

def list_repository_files(repo_path: str) -> list[str]:
    repo = Path(repo_path)
    
    if not repo.exists():
        raise ValueError("Repository path does not exist")

    files= []

    for file in repo.rglob("*"):
        if file.is_file() and not should_ignore_file(file) and is_allowed_file(file) and not is_file_too_large(file):
            files.append(str(file))

    return files

def load_file(file_path: str) -> str:
    path = Path(file_path)
    return path.read_text(encoding= "utf-8")

def load_repository(repo_path: str) -> list[dict]:
    repo = Path(repo_path)
    documents = []
    files = list_repository_files(repo_path)

    for file in files:
        try:
            inside_file = load_file(file) 
        except UnicodeDecodeError:
            print(f"Skipping unreadable file: {file}")
            continue
    
        contents = {
            "path": str(Path(file).relative_to(repo)),
            "content" : inside_file
        }
        documents.append(contents)
    return documents





        
        





