"""Casos de uso do sistema: a camada de serviço depende do contrato TAD."""
from app.dominio.chamado import Chamado, ChamadoJaConcluido, StatusChamado
from app.modelos.schemas import ChamadoCriacao
from app.repositorios.contrato import RepositorioChamados


class ChamadoNaoEncontrado(Exception):
    """Exceção de serviço: chamado não encontrado no repositório."""
    def __init__(self, chamado_id: int):
        self.chamado_id = chamado_id
        super().__init__(f"Chamado {chamado_id} não encontrado")


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
        # Regra de negócio: normalização de entrada (remoção de espaços em branco)
        titulo = dados.titulo.strip()
        descricao = dados.descricao.strip()
        solicitante = dados.solicitante.strip()

        chamado = Chamado(
            id=0,
            titulo=titulo,
            descricao=descricao,
            solicitante=solicitante,
        )
        return self._repositorio.criar(chamado)

    def concluir(self, chamado_id: int) -> Chamado:
        """Conclui um chamado pelo ID.

        Args:
            chamado_id: ID do chamado a ser concluído.

        Returns:
            O chamado atualizado com status CONCLUIDO.

        Raises:
            ChamadoNaoEncontrado: Se o chamado não existir.
            ChamadoJaConcluido: Se o chamado já estiver concluído (do domínio).
        """
        chamado = self._repositorio.buscar_por_id(chamado_id)
        if chamado is None:
            raise ChamadoNaoEncontrado(chamado_id)

        # Aplica a regra de domínio
        chamado.concluir()

        # Persiste a alteração
        return self._repositorio.salvar(chamado)