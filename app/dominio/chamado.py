"""Entidades e valores do domínio de chamados."""
from dataclasses import dataclass
from enum import Enum

from app.dominio.excecoes import ChamadoJaConcluido


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

    def concluir(self) -> None:
        if self.status == StatusChamado.CONCLUIDO:
            raise ChamadoJaConcluido(
                "Chamado já está concluído"
            )
        self.status = StatusChamado.CONCLUIDO
