"""Ponto de entrada da API de chamados."""
from fastapi import FastAPI
from app.controladores.chamados import roteador_chamados

app = FastAPI(
    title="Web Dev Day - Central de Chamados",
    description="API de treinamento: acompanhe os tickets do sprint.",
    version="0.1.0",
)

@app.get("/saude", tags=["Sistema"])
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(roteador_chamados)
