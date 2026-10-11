import pytest
from backend.chunker import chunk_python_document


@pytest.fixture
def sample_document():
    return {
        "path": "sample.py",
        "content": '''DATABASE_URL = "sqlite:///app.db"

@decorator_one
@decorator_two
def greet():
    return "Hello"

DEBUG = True

class UserService:
    @staticmethod
    def get_user():
        return "Alice"

async def fetch_data():
    return "Data loaded"
'''
    }


@pytest.fixture
def chunks(sample_document):
    return chunk_python_document(sample_document)


def test_chunk_count(chunks):
    assert len(chunks) == 4


def test_function_chunk(chunks):
    function = next(c for c in chunks if c["name"] == "greet")

    assert function["type"] == "function"
    assert function["start_line"] == 3
    assert function["end_line"] == 6
    assert "@decorator_one" in function["content"]
    assert "@decorator_two" in function["content"]


def test_method_chunk(chunks):
    method = next(c for c in chunks if c["name"] == "get_user")

    assert method["type"] == "method"
    assert method["class_name"] == "UserService"
    assert method["start_line"] == 11
    assert method["end_line"] == 13
    assert "@staticmethod" in method["content"]


def test_async_function(chunks):
    function = next(c for c in chunks if c["name"] == "fetch_data")

    assert function["type"] == "function"
    assert function["start_line"] == 15
    assert function["end_line"] == 16
    assert "async def" in function["content"]


def test_configuration_chunk(chunks):
    config = next(c for c in chunks if c["type"] == "configuration")

    assert config["name"] == "module_config"
    assert config["start_line"] == 1
    assert config["end_line"] == 8

    assert config["source_ranges"] == [
        {"start_line": 1, "end_line": 1},
        {"start_line": 8, "end_line": 8}
    ]

    assert "DATABASE_URL" in config["content"]
    assert "DEBUG = True" in config["content"]
    assert "def greet" not in config["content"]


def test_invalid_python():
    document = {
        "path": "broken.py",
        "content": "def broken(\n    return 100"
    }

    assert chunk_python_document(document) == []


def test_empty_file():
    document = {
        "path": "empty.py",
        "content": ""
    }

    assert chunk_python_document(document) == []