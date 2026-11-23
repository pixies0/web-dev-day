"""Isolamento: cada teste recebe um repositório independente."""
import pytest
from fastapi.testclient import TestClient
from app.dependencias import obter_repositorio
from app.main import app
from app.repositorios.memoria import RepositorioMemoria

@pytest.fixture
def cliente():
    repositorio = RepositorioMemoria()
    app.dependency_overrides[obter_repositorio] = lambda: repositorio
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
