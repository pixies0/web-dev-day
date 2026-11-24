"""Casos de uso do sistema: a camada de serviço depende do contrato TAD."""
from app.dominio.chamado import Chamado, StatusChamado
from app.modelos.schemas import ChamadoCriacao
from app.repositorios.contrato import RepositorioChamados

class ServicoChamados:
    def __init__(self, repositorio: RepositorioChamados) -> None:
        self._repositorio = repositorio

    def listar(self, status: StatusChamado | None = None) -> list[Chamado]:
        chamados = self._repositorio.listar()
        if status is not None:
            return [chamado for chamado in chamados if chamado.status == status]
        return chamados

    def buscar_por_id(self, chamado_id: int) -> Chamado | None:
        return self._repositorio.buscar_por_id(chamado_id)

    def criar(self, dados: ChamadoCriacao) -> Chamado:
        chamado = Chamado(
            id=0,
            titulo=dados.titulo.strip(),
            descricao=dados.descricao.strip(),
            solicitante=dados.solicitante.strip(),
        )
        return self._repositorio.criar(chamado)
