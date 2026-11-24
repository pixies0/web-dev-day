"""Entidades e valores do domínio de chamados."""
from dataclasses import dataclass
from enum import Enum


class ChamadoJaConcluido(Exception):
    """Exceção de domínio: não é possível concluir um chamado já concluído."""
    def __init__(self, chamado_id: int):
        self.chamado_id = chamado_id
        super().__init__(f"Chamado {chamado_id} já está concluído")


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
        """Marca o chamado como concluído.

        Raises:
            ChamadoJaConcluido: Se o chamado já estiver concluído.
        """
        if self.status == StatusChamado.CONCLUIDO:
            raise ChamadoJaConcluido(self.id)
        self.status = StatusChamado.CONCLUIDO
