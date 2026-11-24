"""Testes básicos. Amplie-os ao resolver os tickets."""

def test_saude(cliente):
    resposta = cliente.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_listagem_inicial(cliente):
    resposta = cliente.get("/chamados")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_criar_e_buscar_chamado(cliente):
    resposta = cliente.post("/chamados", json={
        "titulo": "  Solicitar teclado  ",
        "descricao": "  Teclado com teclas quebradas  ",
        "solicitante": "  Denise  ",
    })
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "Solicitar teclado"
    assert resposta.json()["status"] == "aberto"
    chamado_id = resposta.json()["id"]
    assert cliente.get(f"/chamados/{chamado_id}").status_code == 200


def test_chamado_inexistente(cliente):
    resposta = cliente.get("/chamados/999")
    assert resposta.status_code == 404


def test_filtrar_chamados_por_status_aberto(cliente):
    """GET /chamados?status=aberto retorna somente chamados com status aberto."""
    resposta = cliente.get("/chamados?status=aberto")
    assert resposta.status_code == 200
    chamados = resposta.json()
    assert len(chamados) == 1
    assert chamados[0]["status"] == "aberto"
    assert chamados[0]["id"] == 1


def test_filtrar_chamados_por_status_em_andamento(cliente):
    """GET /chamados?status=em_andamento retorna somente chamados com status em_andamento."""
    resposta = cliente.get("/chamados?status=em_andamento")
    assert resposta.status_code == 200
    chamados = resposta.json()
    assert len(chamados) == 1
    assert chamados[0]["status"] == "em_andamento"
    assert chamados[0]["id"] == 2


def test_filtrar_chamados_por_status_concluido(cliente):
    """GET /chamados?status=concluido retorna somente chamados com status concluido."""
    resposta = cliente.get("/chamados?status=concluido")
    assert resposta.status_code == 200
    chamados = resposta.json()
    assert len(chamados) == 1
    assert chamados[0]["status"] == "concluido"
    assert chamados[0]["id"] == 3


def test_filtrar_chamados_status_sem_resultados(cliente):
    """Status válido sem chamados correspondentes retorna lista vazia e 200."""
    # Cria um novo repositório vazio para este teste
    from app.repositorios.memoria import RepositorioMemoria
    from app.dependencias import obter_repositorio
    from app.main import app

    repositorio_vazio = RepositorioMemoria()
    # Limpa os exemplos iniciais
    repositorio_vazio._chamados.clear()
    repositorio_vazio._proximo_id = 1

    app.dependency_overrides[obter_repositorio] = lambda: repositorio_vazio
    try:
        resposta = cliente.get("/chamados?status=aberto")
        assert resposta.status_code == 200
        assert resposta.json() == []
    finally:
        app.dependency_overrides.clear()


def test_listagem_sem_filtro_retorna_todos(cliente):
    """GET /chamados sem parâmetro continua retornando todos os chamados."""
    resposta = cliente.get("/chamados")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_concluir_chamado_sucesso(cliente):
    """PATCH /chamados/{id}/concluir - Concluir um chamado aberto com sucesso."""
    # Usa o chamado ID 1 que está com status ABERTO
    resposta = cliente.patch("/chamados/1/concluir")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == 1
    assert resposta.json()["status"] == "concluido"


def test_concluir_chamado_inexistente(cliente):
    """PATCH /chamados/{id}/concluir - Retorna 404 para ID inexistente."""
    resposta = cliente.patch("/chamados/999/concluir")
    assert resposta.status_code == 404
    assert "não encontrado" in resposta.json()["detail"].lower()


def test_concluir_chamado_ja_concluido(cliente):
    """PATCH /chamados/{id}/concluir - Retorna 409 para chamado já concluído."""
    # Usa o chamado ID 3 que já está com status CONCLUIDO
    resposta = cliente.patch("/chamados/3/concluir")
    assert resposta.status_code == 409
    assert "já concluído" in resposta.json()["detail"].lower() or "ja concluido" in resposta.json()["detail"].lower()
