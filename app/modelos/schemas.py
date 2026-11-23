"""Contratos de entrada e saída da API."""
from pydantic import BaseModel, Field
from app.dominio.chamado import StatusChamado

class ChamadoCriacao(BaseModel):
    titulo: str = Field(min_length=3, max_length=120)
    descricao: str = Field(min_length=5)
    solicitante: str = Field(min_length=3, max_length=80)

class ChamadoResposta(ChamadoCriacao):
    id: int
    status: StatusChamado
