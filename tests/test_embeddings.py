import numpy as np
import pytest

from backend.embeddings import embed_chunks


@pytest.fixture
def sample_document():
    return {
        "path": "example.py",
        "content": """
def greet():
    return "Hello"

def goodbye():
    return "Bye"
"""
    }


@pytest.fixture(scope="module")
def embedded_results():
    document = {
        "path": "example.py",
        "content": """
def greet():
    return "Hello"

def goodbye():
    return "Bye"
"""
    }
    return embed_chunks(document)


def test_embedding_count(embedded_results):
    assert len(embedded_results) == 2


def test_embedding_dimensions(embedded_results):
    for result in embedded_results:
        assert result["embedding"].shape == (384,)


def test_embedding_is_numpy_array(embedded_results):
    for result in embedded_results:
        assert isinstance(result["embedding"], np.ndarray)


def test_chunk_metadata_preserved(embedded_results):
    names = [result["chunk"]["name"] for result in embedded_results]

    assert names == ["greet", "goodbye"]

    for result in embedded_results:
        assert result["chunk"]["path"] == "example.py"
        assert "start_line" in result["chunk"]
        assert "end_line" in result["chunk"]


def test_embedding_chunk_alignment(embedded_results):
    assert embedded_results[0]["chunk"]["name"] == "greet"
    assert embedded_results[1]["chunk"]["name"] == "goodbye"


def test_empty_document():
    document = {
        "path": "empty.py",
        "content": ""
    }

    results = embed_chunks(document)

    assert results == []


def test_embeddings_are_finite(embedded_results):
    for result in embedded_results:
        assert np.all(np.isfinite(result["embedding"]))


def test_different_functions_produce_different_embeddings(embedded_results):
    first = embedded_results[0]["embedding"]
    second = embedded_results[1]["embedding"]

    assert not np.array_equal(first, second)