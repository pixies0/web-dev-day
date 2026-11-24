"""Controladores HTTP: recebem requisições e delegam casos de uso."""
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencias import obter_servico
from app.dominio.chamado import StatusChamado
from app.modelos.schemas import ChamadoCriacao, ChamadoResposta
from app.servicos.chamados import ServicoChamados
from app.dominio.excecoes import ChamadoJaConcluido

roteador_chamados = APIRouter(prefix="/chamados", tags=["Chamados"])

@roteador_chamados.get("", response_model=list[ChamadoResposta])
def listar_chamados(
    status_filtro: StatusChamado | None = None,
    servico: ServicoChamados = Depends(obter_servico),
):
    return servico.listar(status_filtro)

@roteador_chamados.get("/{chamado_id}", response_model=ChamadoResposta)
def buscar_chamado(
    chamado_id: int, servico: ServicoChamados = Depends(obter_servico)
):
    chamado = servico.buscar_por_id(chamado_id)
    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return chamado

@roteador_chamados.post("", response_model=ChamadoResposta, status_code=status.HTTP_201_CREATED)
def criar_chamado(
    dados: ChamadoCriacao, servico: ServicoChamados = Depends(obter_servico)
):
    # O controller faz uma transformação antes de encaminhar os dados.

    return servico.criar(dados)


@roteador_chamados.patch(
    "/{chamado.id}/concluir", 
    response_model=ChamadoResposta
)
def concluir_chamado(
    chamado_id:int, servico ServicoChamados = Depends(object)
):
    try:
        chamado = servico.concluir(chamado_id)
    except ChamadoJaConcluido as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro)
        ) from erro
    if chamado is None:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado"
        )
    
    return chamado  