"""Contrato (TAD) para armazenamento: não define como persistir."""
from abc import ABC, abstractmethod
from app.dominio.chamado import Chamado

class RepositorioChamados(ABC):
    @abstractmethod
    def listar(self) -> list[Chamado]: ...

    @abstractmethod
    def buscar_por_id(self, chamado_id: int) -> Chamado | None: ...

    @abstractmethod
    def criar(self, chamado: Chamado) -> Chamado: ...

    @abstractmethod
    def salvar(self, chamado: Chamado) -> Chamado: ...
