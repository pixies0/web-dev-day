def test_concluir_chamado_existente(cliente):
    resposta = cliente.patch("/chamados/1/concluir")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "concluido"

    consulta = cliente.get("/chamados/1")

    assert consulta.status_code == 200
    assert consulta.json()["status"] == "concluido"


def test_concluir_chamado_inexistente(cliente):
    resposta = cliente.patch("/chamados/999/concluir")

    assert resposta.status_code == 404


def test_concluir_chamado_duplicado_retorna_conflito(cliente):
    primeira = cliente.patch("/chamados/1/concluir")
    segunda = cliente.patch("/chamados/1/concluir")

    assert primeira.status_code == 200
    assert segunda.status_code == 409


def test_chamado_ja_concluido_desde_o_inicio(cliente):
    resposta = cliente.patch("/chamados/3/concluir")

    assert resposta.status_code == 409

