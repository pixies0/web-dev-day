# Web Dev Day — Central de Chamados

Projeto didático de FastAPI para um **sprint de 3 horas**. Você recebeu uma API funcional, mas com tarefas pendentes de uma equipe fictícia.

## Preparar o ambiente

Use **Python 3.11 ou superior**. Abra um terminal na pasta raiz do projeto.

No Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

No Prompt de Comando (cmd), a ativação é `.venv\Scripts\activate.bat`.
No Powershell (ps), a ativação é `.venv\Scripts\Activate.PSI`.


Caso utilize Miniconda, você pode criar um ambiente com `conda create -n web-dev-day python=3.13 -y` e ativá-lo com `conda activate web-dev-day`, seguido de `python -m pip install -r requirements.txt`.

Documentação automática da API: <http://127.0.0.1:8000/docs>

Execute os testes em outro terminal com o ambiente ativo:

```bash
python -m pytest -q
```

## Endpoints disponíveis no projeto inicial

| Método | Caminho | Descrição |
|---|---|---|
| GET | `/saude` | Estado da API |
| GET | `/chamados` | Lista chamados |
| GET | `/chamados?status_filtro=aberto` | Lista por status (investigue o comportamento) |
| GET | `/chamados/{chamado_id}` | Busca um chamado |
| POST | `/chamados` | Cadastra um chamado |

Exemplo de POST:

```json
{
  "titulo": "Solicitar mouse",
  "descricao": "Mouse do laboratório não funciona",
  "solicitante": "Marina"
}
```

Os dados ficam **em memória** e são reiniciados ao reiniciar o processo. PostgreSQL não é necessário neste sprint.

## Tickets do sprint

Abra o arquivo [`docs/index.html`](docs/index.html) no navegador para acessar o walkthrough completo da atividade, com critérios de aceite e exemplos similares. É possível publicá-lo via GitHub Pages selecionando `main` e `/docs` nas configurações de Pages.

## Arquitetura (inicial)

- `app/controladores/`: rotas HTTP (papel de controller).
- `app/modelos/`: schemas de entrada e saída.
- `app/dominio/`: entidade de domínio (modelo).
- `app/servicos/`: regras e casos de uso.
- `app/repositorios/`: contrato abstrato e implementação de persistência.
- `app/dependencias.py`: montagem das dependências.

## Documentação de entrega (ticket WDD-004)

**A completar pelo desenvolvedor:** registre o fluxo de uma requisição, o endpoint de conclusão e como executar os testes.
