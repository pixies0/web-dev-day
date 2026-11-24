# Web Dev Day — Central de Chamados

API de treinamento em **FastAPI** para gestão de chamados internos. Projeto didático que demonstra arquitetura em camadas (Controller → Service → Repository + TAD), injeção de dependências, testes automatizados e documentação interativa via Swagger.

---

## 📋 Sumário

- [Instalação](#instalação)
- [Endpoints](#endpoints)
- [Testes](#testes)
- [Arquitetura](#arquitetura)
- [Padrão de Commits](#padrão-de-commits)
- [Observações](#observações)

---

## Instalação

### Pré-requisitos

- **Python 3.10+**
- **GitHub Desktop**
- **VS Code**

### Passo a passo

#### 1. Clone o repositório

```bash
git clone https://github.com/pixies0/web-dev-day.git
cd web-dev-day
```

#### 2. Crie sua branch de trabalho

No **GitHub Desktop** (ou terminal):
- Partindo da branch `main`, crie uma nova branch com o padrão:
  ```bash
  git checkout -b dev/seu-nome-sobrenome
  ```
  > Use apenas letras minúsculas e hífens (ex: `dev/john-doe`).
- Publique a branch: `git push -u origin dev/seu-nome-sobrenome` (ou **Publish branch** no GitHub Desktop).
- **Importante:** Não faça commits diretamente na `main`. Trabalhe sempre na sua branch.

> **Sem acesso de escrita no repositório original?** Faça um **Fork** no GitHub primeiro, clone *o seu fork* e crie a branch lá.

#### 3. Crie e ative o ambiente virtual

**Windows (PowerShell):**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (cmd.exe):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux / macOS (bash / zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> **Dica:** Se o PowerShell bloquear a execução de scripts, use `cmd` ou execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` antes de ativar.

#### 4. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

#### 5. Suba a API

```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000**

- Documentação interativa (Swagger UI): **http://127.0.0.1:8000/docs**
- Documentação alternativa (ReDoc): **http://127.0.0.1:8000/redoc**

---

## Endpoints

Base URL: `http://127.0.0.1:8000`

### Sistema

| Método | Rota     | Descrição           | Respostas |
|--------|----------|---------------------|-----------|
| GET    | `/saude` | Verifica saúde da API | `200` |

**Exemplo de resposta (200):**
```json
{
  "status": "ok"
}
```

---

### Chamados

#### Listar todos os chamados

| Método | Rota         | Parâmetros | Respostas |
|--------|--------------|------------|-----------|
| GET    | `/chamados`  | —          | `200` |

**Exemplo de resposta (200):**
```json
[
  {
    "id": 1,
    "titulo": "Impressora sem conexão",
    "descricao": "Impressora do setor financeiro offline",
    "solicitante": "Ana",
    "status": "aberto"
  },
  {
    "id": 2,
    "titulo": "Atualizar navegador",
    "descricao": "Atualizar navegador da recepção",
    "solicitante": "Bruno",
    "status": "em_andamento"
  },
  {
    "id": 3,
    "titulo": "Acesso ao sistema",
    "descricao": "Permissão para consultar relatório",
    "solicitante": "Carla",
    "status": "concluido"
  }
]
```

---

#### Filtrar chamados por status

| Método | Rota                          | Parâmetros (query)           | Respostas |
|--------|-------------------------------|------------------------------|-----------|
| GET    | `/chamados?status=aberto`     | `status`: `aberto \| em_andamento \| concluido` | `200` |

**Exemplo de requisição:**
```bash
curl "http://127.0.0.1:8000/chamados?status=aberto"
```

**Exemplo de resposta (200):**
```json
[
  {
    "id": 1,
    "titulo": "Impressora sem conexão",
    "descricao": "Impressora do setor financeiro offline",
    "solicitante": "Ana",
    "status": "aberto"
  }
]
```

**Comportamento:**
- Retorna **lista vazia `[]`** (200) quando o status é válido mas não há chamados correspondentes.
- Retorna **`422 Unprocessable Entity`** se o valor de `status` não for um dos valores válidos do enum.

---

#### Buscar um chamado por ID

| Método | Rota                  | Parâmetros (path) | Respostas |
|--------|-----------------------|-------------------|-----------|
| GET    | `/chamados/{chamado_id}` | `chamado_id`: inteiro | `200`, `404` |

**Exemplo de resposta (200):**
```json
{
  "id": 1,
  "titulo": "Impressora sem conexão",
  "descricao": "Impressora do setor financeiro offline",
  "solicitante": "Ana",
  "status": "aberto"
}
```

**Exemplo de erro (404):**
```json
{
  "detail": "Chamado não encontrado"
}
```

---

#### Criar um novo chamado

| Método | Rota        | Corpo da requisição | Respostas |
|--------|-------------|---------------------|-----------|
| POST   | `/chamados` | JSON (ver abaixo)   | `201`, `422` |

**Corpo da requisição:**
```json
{
  "titulo": "Solicitar mouse",
  "descricao": "Mouse do laboratório não funciona",
  "solicitante": "Marina"
}
```

**Validações:**
- `titulo`: 3 a 120 caracteres
- `descricao`: mínimo 5 caracteres
- `solicitante`: 3 a 80 caracteres
- **Espaços em branco no início/fim são removidos automaticamente** (normalização no serviço)

**Exemplo de resposta (201):**
```json
{
  "id": 4,
  "titulo": "Solicitar mouse",
  "descricao": "Mouse do laboratório não funciona",
  "solicitante": "Marina",
  "status": "aberto"
}
```

**Exemplo de erro (422):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "titulo"],
      "msg": "String should have at least 3 characters",
      "input": "ab"
    }
  ]
}
```

---

#### Concluir um chamado

| Método | Rota                          | Respostas |
|--------|-------------------------------|-----------|
| PATCH  | `/chamados/{chamado_id}/concluir` | `200`, `404`, `409` |

**Observações:**
- Não recebe corpo JSON (body vazio).
- Altera o status do chamado para `concluido`.
- Retorna o chamado atualizado.

**Exemplo de resposta (200) — sucesso:**
```json
{
  "id": 1,
  "titulo": "Impressora sem conexão",
  "descricao": "Impressora do setor financeiro offline",
  "solicitante": "Ana",
  "status": "concluido"
}
```

**Exemplo de erro (404) — chamado não existe:**
```json
{
  "detail": "Chamado não encontrado"
}
```

**Exemplo de erro (409) — chamado já concluído:**
```json
{
  "detail": "Chamado já concluído"
}
```

**Cenários testados:**
```bash
# Concluir chamado aberto (ID 1) → 200
curl -X PATCH http://127.0.0.1:8000/chamados/1/concluir

# Tentar concluir novamente o mesmo chamado → 409
curl -X PATCH http://127.0.0.1:8000/chamados/1/concluir

# Concluir ID inexistente → 404
curl -X PATCH http://127.0.0.1:8000/chamados/999/concluir
```

---

## Testes

### Como executar

Com o ambiente virtual ativo, em um terminal separado:

```bash
python -m pytest -v
```

Ou para saída mais concisa:
```bash
python -m pytest -q
```

### Cobertura dos testes

| Arquivo de teste | Cenários cobertos |
|------------------|-------------------|
| `tests/test_api.py` | |
| `test_saude` | GET `/saude` retorna 200 e `{"status": "ok"}` |
| `test_listagem_inicial` | GET `/chamados` retorna 3 chamados iniciais |
| `test_criar_e_buscar_chamado` | POST cria chamado, normaliza espaços, GET por ID retorna 200 |
| `test_chamado_inexistente` | GET `/chamados/999` retorna 404 |
| `test_filtrar_chamados_por_status_aberto` | Filtro `status=aberto` retorna apenas chamados abertos |
| `test_filtrar_chamados_por_status_em_andamento` | Filtro `status=em_andamento` retorna apenas em andamento |
| `test_filtrar_chamados_por_status_concluido` | Filtro `status=concluido` retorna apenas concluídos |
| `test_filtrar_chamados_status_sem_resultados` | Filtro válido sem resultados retorna lista vazia (200) |
| `test_listagem_sem_filtro_retorna_todos` | GET `/chamados` sem parâmetro retorna todos |
| `test_concluir_chamado_sucesso` | PATCH `/chamados/1/concluir` retorna 200 e status `concluido` |
| `test_concluir_chamado_inexistente` | PATCH `/chamados/999/concluir` retorna 404 |
| `test_concluir_chamado_ja_concluido` | PATCH em chamado já concluído retorna 409 |

**Total: 12 testes** cobrendo:
- ✅ Health check
- ✅ Listagem (com e sem filtro)
- ✅ Busca por ID (sucesso e 404)
- ✅ Criação (com normalização de entrada)
- ✅ Conclusão (sucesso, 404, 409)

---

## Arquitetura

O projeto segue uma arquitetura em camadas inspirada em **MVC adaptado para APIs**, com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────────┐
│                        REQUISIÇÃO HTTP                           │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  CONTROLADOR (app/controladores/chamados.py)                    │
│  • Recebe requisições HTTP                                      │
│  • Valida parâmetros de rota/query via FastAPI                  │
│  • Delega regras de negócio para o Serviço                      │
│  • Traduz exceções de domínio/serviço em status HTTP            │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  SERVIÇO (app/servicos/chamados.py)                             │
│  • Contém regras de negócio e casos de uso                      │
│  • Normaliza dados de entrada (strip em strings)                │
│  • Coordena operações: busca → regra de domínio → persistência  │
│  • Depende do CONTRATO (TAD) do repositório, não da implementação│
│  • Lança exceções de negócio: ChamadoNaoEncontrado              │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  DOMÍNIO (app/dominio/chamado.py)                               │
│  • Entidade `Chamado` (dataclass)                               │
│  • Enum `StatusChamado`: ABERTO, EM_ANDAMENTO, CONCLUIDO        │
│  • Encapsula regra: `concluir()` lança `ChamadoJaConcluido`     │
│  • Exceção de domínio: `ChamadoJaConcluido`                     │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  CONTRATO DO REPOSITÓRIO (app/repositorios/contrato.py)         │
│  • TAD (Tipo Abstrato de Dados): `RepositorioChamados` (ABC)    │
│  • Métodos: `listar()`, `buscar_por_id()`, `criar()`, `salvar()`│
│  • Define O QUÊ, não COMO                                       │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  IMPLEMENTAÇÃO CONCRETA (app/repositorios/memoria.py)           │
│  • `RepositorioMemoria` implementa o contrato                   │
│  • Armazenamento em dicionário Python (em memória)              │
│  • Dados são reiniciados a cada restart da API                  │
└─────────────────────────────────────────────────────────────────┘
```

### Injeção de Dependências (`app/dependencias.py`)

```python
_repositorio_compartilhado = RepositorioMemoria()

def obter_repositorio() -> RepositorioChamados:
    return _repositorio_compartilhado

def obter_servico(
    repositorio: RepositorioChamados = Depends(obter_repositorio),
) -> ServicoChamados:
    return ServicoChamados(repositorio)
```

- **Uma única instância** de `RepositorioMemoria` é compartilhada durante a execução (singleton por processo).
- O **Serviço recebe o contrato**, não a implementação concreta → permite trocar persistência (ex: PostgreSQL) sem alterar o serviço.
- FastAPI resolve as dependências automaticamente via `Depends`.

### Modelos / Schemas (`app/modelos/schemas.py`)

| Schema | Uso | Campos |
|--------|-----|--------|
| `ChamadoCriacao` | Entrada (POST) | `titulo`, `descricao`, `solicitante` |
| `ChamadoResposta` | Saída (GET, POST, PATCH) | herda de `ChamadoCriacao` + `id`, `status` |

---

## Padrão de Commits

Este projeto adota **Conventional Commits** (formato angular). Cada ticket da sprint corresponde a **um commit** com tipo semântico:

| Tipo | Quando usar | Exemplo |
|------|-------------|---------|
| `fix` | Correção de bug | `fix(chamados): corrigir filtro por status` |
| `refactor` | Reorganização sem mudança de comportamento | `refactor(chamados): mover normalizacao para servico` |
| `feat` | Nova funcionalidade | `feat(chamados): permitir concluir chamados` |
| `docs` | Apenas documentação | `docs(readme): documentar arquitetura e conclusao` |

**Estrutura da mensagem:**
```
<tipo>(<escopo>): <descrição no imperativo>
```

**Regras:**
- Um commit por ticket (não misture `fix` + `feat` no mesmo commit).
- Escopo opcional, mas recomendado (`chamados`, `readme`, `testes`).
- Descrição no imperativo: "corrigir", "mover", "permitir", "documentar" (não "corrigido", "movido").
- Commits de `docs` **não devem conter alterações de código-fonte**.

---

## Observações

- **Persistência em memória:** Os dados são armazenados em um dicionário Python (`RepositorioMemoria`). Ao reiniciar a API (`Ctrl+C` + `uvicorn ...`), **todos os chamados voltam ao estado inicial** (3 exemplos pré-cadastrados).
- **Sem banco de dados:** PostgreSQL não é necessário para este sprint. A arquitetura com TAD permite adicionar persistência real futuramente sem quebrar o serviço.
- **Validação automática:** FastAPI + Pydantic validam automaticamente o corpo das requisições (422 para dados inválidos).
- **Documentação interativa:** Use `/docs` (Swagger) para testar endpoints manualmente com o botão "Try it out".

---

## Licença

Projeto educacional — Web Dev Day. Uso livre para fins de aprendizado.