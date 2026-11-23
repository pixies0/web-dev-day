"""Entidades e valores do domínio de chamados."""
from dataclasses import dataclass
from enum import Enum

class StatusChamado(str, Enum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"

@dataclass
class Chamado:
    id: int
    titulo: str
    descricao: str
    solicitante: str
    status: StatusChamado = StatusChamado.ABERTO
