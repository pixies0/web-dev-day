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
