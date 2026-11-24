"""Controladores HTTP: recebem requisições e delegam casos de uso."""
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencias import obter_servico
from app.dominio.chamado import StatusChamado
from app.modelos.schemas import ChamadoCriacao, ChamadoResposta
from app.servicos.chamados import ServicoChamados

roteador_chamados = APIRouter(prefix="/chamados", tags=["Chamados"])

@roteador_chamados.get("", response_model=list[ChamadoResposta])
def listar_chamados(
    status: StatusChamado | None = None,
    servico: ServicoChamados = Depends(obter_servico),
):
    return servico.listar(status)

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
    return servico.criar(dados)