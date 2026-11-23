"""Ponto de composição da injeção de dependências do FastAPI."""
from fastapi import Depends
from app.repositorios.contrato import RepositorioChamados
from app.repositorios.memoria import RepositorioMemoria
from app.servicos.chamados import ServicoChamados

_repositorio_compartilhado = RepositorioMemoria()

def obter_repositorio() -> RepositorioChamados:
    return _repositorio_compartilhado

def obter_servico(
    repositorio: RepositorioChamados = Depends(obter_repositorio),
) -> ServicoChamados:
    return ServicoChamados(repositorio)
