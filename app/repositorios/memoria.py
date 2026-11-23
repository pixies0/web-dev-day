"""Implementação concreta do repositório, sem banco de dados."""
from app.dominio.chamado import Chamado, StatusChamado
from app.repositorios.contrato import RepositorioChamados

class RepositorioMemoria(RepositorioChamados):
    def __init__(self) -> None:
        exemplos = [
            Chamado(1, "Impressora sem conexão", "Impressora do setor financeiro offline", "Ana", StatusChamado.ABERTO),
            Chamado(2, "Atualizar navegador", "Atualizar navegador da recepção", "Bruno", StatusChamado.EM_ANDAMENTO),
            Chamado(3, "Acesso ao sistema", "Permissão para consultar relatório", "Carla", StatusChamado.CONCLUIDO),
        ]
        self._chamados = {item.id: item for item in exemplos}
        self._proximo_id = 4

    def listar(self) -> list[Chamado]:
        return list(self._chamados.values())

    def buscar_por_id(self, chamado_id: int) -> Chamado | None:
        return self._chamados.get(chamado_id)

    def criar(self, chamado: Chamado) -> Chamado:
        chamado.id = self._proximo_id
        self._chamados[chamado.id] = chamado
        self._proximo_id += 1
        return chamado

    def salvar(self, chamado: Chamado) -> Chamado:
        if chamado.id not in self._chamados:
            raise KeyError(f"Chamado {chamado.id} inexistente")
        self._chamados[chamado.id] = chamado
        return chamado
