<div align="center">
  <h1>
    <img src="https://skillicons.dev/icons?i=python,flask,postgres,docker" /><br>
    Back-End — Final Graduation Project 🇺🇸
  </h1>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/PostgreSQL-17-336791?style=flat&logo=postgresql&logoColor=white" />
    <img src="https://img.shields.io/badge/Docker-27.x-2496ED?style=flat&logo=docker&logoColor=white" />
    <img src="https://img.shields.io/badge/Ruff-enabled-D7FF64?style=flat&logo=ruff&logoColor=black" />
    <img src="https://img.shields.io/badge/pytest-enabled-0A9EDC?style=flat&logo=pytest&logoColor=white" />
  </p>
</div>

This repository contains the Back-End of <a href="https://github.com/paulo-campos-57" target="_blank">Paulo Campos</a>'s Final Graduation Project (TCC).<br>
The full project documentation can be found at this <a href="https://docs.google.com/document/d/1WqyVEorM9IbZZ5CjwYWsqjv00DI9vhe-/edit?usp=sharing&ouid=104768249469194230645&rtpof=true&sd=true" target="_blank">link</a>.

---

## Project Structure

```
Projeto-TCC-BackEnd/
├── src/
│   ├── controllers/          # Request handlers (business logic boundary)
│   │   ├── bairro_controller.py
|   |   ├── jogo_controller.py
|   |   ├── resultado_controller.py
│   │   └── user_controller.py
│   ├── decorators/             # Reusable decorators
│   │   ├── auth.py             # @token_required — JWT validation
│   │   ├── error_handler.py    # @handle_errors — centralised error handling
│   │   └── session_required.py # @session_required — session validation 
│   ├── models/               # SQLAlchemy models & in-memory state
│   │   ├── bairro.py         # Neighbourhood data model
│   │   ├── ingrediente.py    # Ingredient catalogue (server-side only)
│   │   ├── resultado.py      # Game result model
│   │   ├── sessao_jogo.py    # In-memory game session state
│   │   └── user.py           # User model
│   ├── routes/               # Flask blueprints
│   │   ├── bairro_routes.py  # /bairro
│   │   ├── jogo_routes.py    # /jogo
│   │   ├── resultado_routes.py # /usuarios
│   │   └── user_routes.py    # /user
│   ├── services/             # Business logic
│   │   ├── bairro_service.py
│   │   ├── jogo_service.py
│   │   ├── resultado_service.py
│   │   └── user_service.py
│   ├── tests/                # Unit tests (pytest)
│   │   ├── conftest.py
│   │   ├── test_ingrediente.py
│   │   ├── test_sessao_jogo.py
│   │   └── test_jogo_service.py
|   ├── .env                # Enviroment variables
│   ├── app.py                # Application factory & blueprint registry
│   ├── database.py           # SQLAlchemy instance
│   ├── pyproject.toml        # Ruff configuration
│   ├── pytest.ini            # Test runner configuration
│   └── requirements.txt      # Python dependencies
│
├── docker-compose.yml        # Orchestrates API + PostgreSQL services
├── Dockerfile                # API image (python:3.12-slim + gunicorn)
├── .env.docker               # Environment variables template for Docker
├── .dockerignore
└── .gitignore
```

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| [Python](https://www.python.org/) | 3.12 | Primary language |
| [Flask](https://flask.palletsprojects.com/) | 3.x | Web framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.x | ORM |
| [PostgreSQL](https://www.postgresql.org/) | 17 | Relational database |
| [Docker](https://www.docker.com/) | 27.x | Containerisation |
| [gunicorn](https://gunicorn.org/) | — | Production WSGI server |
| [bcrypt](https://pypi.org/project/bcrypt/) | 4.x | Password hashing |
| [PyJWT](https://pyjwt.readthedocs.io/) | — | JWT authentication |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | — | Cross-origin resource sharing |
| [pytest](https://pytest.org/) | — | Unit testing |
| [Ruff](https://docs.astral.sh/ruff/) | — | Linter & formatter |

---

## Requirements

- **Docker** 27.x or higher
- **Docker Compose** v2 or higher

> That's it. Python and PostgreSQL do not need to be installed locally.

---

## Environment Variables

Copy `.env.docker` to `.env.docker` and fill in your values before running:

```env
# Database
DATABASE_URL = 'postgresql://user:password@localhost:5432/postgres'

# JWT
# Generate a secure key with: python -c "import secrets; print(secrets.token_hex(32))"
JWT_KEY=your_secret_key_here
```

> The `DATABASE_URL` is assembled automatically by `docker-compose.yml` — no need to set it manually.

---

## How to Run

### <img src="https://skillicons.dev/icons?i=github" height="20" style="vertical-align: middle;" /> 1. Clone the repository

```bash
git clone https://github.com/paulo-campos-57/Projeto-TCC-BackEnd.git
cd Projeto-TCC-BackEnd
```

### 🐳 2. Configure environment variables

```bash
# Edit .env.docker with your credentials
# Generate a secure JWT key
python -c "import secrets; print(secrets.token_hex(32))"
```

### ▶️ 3. Start the services

```bash
docker compose up --build
```

The API will be available at **http://localhost:5000**.  
PostgreSQL will be available at **localhost:5432**.

---

## Docker Commands

| Command | Description |
|---|---|
| `docker compose up --build` | Build image and start all services |
| `docker compose up -d` | Start in background (detached mode) |
| `docker compose down` | Stop and remove containers (data is preserved) |
| `docker compose down -v` | Stop and **delete all data** (volume removed) |
| `docker compose logs -f` | Follow logs from all services |
| `docker compose logs -f api` | Follow logs from the API only |
| `docker compose exec api bash` | Open a shell inside the API container |
| `docker compose exec db psql -U tcc_user -d tcc_db` | Open a psql session |

---

## Running Tests

```bash
# Run all tests inside the container
docker compose exec api pytest

# Run a specific test file
docker compose exec api pytest tests/test_jogo_service.py

# Run with verbose output
docker compose exec api pytest -v
```

---

## API Overview

| Prefix | Description |
|---|---|
| `/user` | Registration, login, profile, and account management |
| `/bairro` | Neighbourhood listing and game session initialisation |
| `/jogo` | Full game session lifecycle (stock, recipe, pricing, day processing) |
| `/usuarios` | Player statistics and match history |

---

## Running Without Docker (alternative)

<details>
<summary>Click to expand</summary>

### Requirements
- Python 3.12+
- PostgreSQL 17+

### Steps

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r src/requirements.txt

# Create src/.env with your local database credentials
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tcc_db" >> src/.env
echo "JWT_KEY=your_secret_key_here" >> src/.env

# Start the development server
python src/app.py
```

</details>

---

## Available Scripts

| Command | Description |
|---|---|
| `docker compose exec api pytest` | Run the test suite |
| `docker compose exec api ruff check .` | Run the linter |
| `docker compose exec api ruff format .` | Format all source files |

---

<br>

---

<div align="center">
  <h1>
    <img src="https://skillicons.dev/icons?i=python,flask,postgres,docker" /><br>
    Projeto TCC — Back-End 🇧🇷
  </h1>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/PostgreSQL-17-336791?style=flat&logo=postgresql&logoColor=white" />
    <img src="https://img.shields.io/badge/Docker-27.x-2496ED?style=flat&logo=docker&logoColor=white" />
    <img src="https://img.shields.io/badge/Ruff-enabled-D7FF64?style=flat&logo=ruff&logoColor=black" />
    <img src="https://img.shields.io/badge/pytest-enabled-0A9EDC?style=flat&logo=pytest&logoColor=white" />
  </p>
</div>

Este repositório contém o Back-End do Trabalho de Conclusão de Curso de <a href="https://github.com/paulo-campos-57" target="_blank">Paulo Campos</a>.<br>
A documentação completa do projeto pode ser encontrada neste <a href="https://docs.google.com/document/d/1WqyVEorM9IbZZ5CjwYWsqjv00DI9vhe-/edit?usp=sharing&ouid=104768249469194230645&rtpof=true&sd=true" target="_blank">link</a>.

---

## Estrutura do Projeto

```
Projeto-TCC-BackEnd/
├── src/
│   ├── controllers/          # Manipuladores de requisição (fronteira da lógica de negócio)
│   │   ├── bairro_controller.py
|   |   ├── jogo_controller.py
|   |   ├── resultado_controller.py
│   │   └── user_controller.py
│   ├── decorators/             # Decoradores reutilizáveis
│   │   ├── auth.py             # @token_required — Validação de JWT
│   │   ├── error_handler.py    # @handle_errors — Tratamento centralizado de erros
│   │   └── session_required.py # @session_required — Validação de sessão 
│   ├── models/               # Modelos SQLAlchemy e estado em memória
│   │   ├── bairro.py         # Modelo de dados de bairro
│   │   ├── ingrediente.py    # Catálogo de ingredientes (apenas lado do servidor)
│   │   ├── resultado.py      # Modelo de resultado do jogo
│   │   ├── sessao_jogo.py    # Estado da sessão de jogo em memória
│   │   └── user.py           # Modelo de usuário
│   ├── routes/               # Blueprints do Flask
│   │   ├── bairro_routes.py  # /bairro
│   │   ├── jogo_routes.py    # /jogo
│   │   ├── resultado_routes.py # /usuarios
│   │   └── user_routes.py    # /user
│   ├── services/             # Lógica de negócio
│   │   ├── bairro_service.py
│   │   ├── jogo_service.py
│   │   ├── resultado_service.py
│   │   └── user_service.py
│   ├── tests/                # Testes unitários (pytest)
│   │   ├── conftest.py
│   │   ├── test_ingrediente.py
│   │   ├── test_sessao_jogo.py
│   │   └── test_jogo_service.py
|   ├── .env                # Variáveis de ambiente
│   ├── app.py                # Fábrica da aplicação e registro de blueprints
│   ├── database.py           # Instância do SQLAlchemy
│   ├── pyproject.toml        # Configuração do Ruff
│   ├── pytest.ini            # Configuração do executor de testes
│   └── requirements.txt      # Dependências Python
│
├── docker-compose.yml        # Orquestra os serviços da API + PostgreSQL
├── Dockerfile                # Imagem da API (python:3.12-slim + gunicorn)
├── .env.docker               # Template de variáveis de ambiente para Docker
├── .dockerignore
└── .gitignore
```

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| [Python](https://www.python.org/) | 3.12 | Linguagem principal |
| [Flask](https://flask.palletsprojects.com/) | 3.x | Framework web |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.x | ORM |
| [PostgreSQL](https://www.postgresql.org/) | 17 | Banco de dados relacional |
| [Docker](https://www.docker.com/) | 27.x | Containerização |
| [gunicorn](https://gunicorn.org/) | — | Servidor WSGI de produção |
| [bcrypt](https://pypi.org/project/bcrypt/) | 4.x | Hash de senhas |
| [PyJWT](https://pyjwt.readthedocs.io/) | — | Autenticação JWT |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | — | Controle de origem cruzada |
| [pytest](https://pytest.org/) | — | Testes unitários |
| [Ruff](https://docs.astral.sh/ruff/) | — | Linter e formatador |

---

## Requisitos

- **Docker** 27.x ou superior
- **Docker Compose** v2 ou superior

> Só isso. Não é necessário instalar Python ou PostgreSQL localmente.

---

## Variáveis de Ambiente

Edite o arquivo `.env.docker` na raiz do projeto com suas credenciais antes de subir os containers:

```env
# Banco de dados
DATABASE_URL = 'postgresql://user:password@localhost:5432/postgres'

# JWT
# Gere uma chave segura com: python -c "import secrets; print(secrets.token_hex(32))"
JWT_KEY=sua_chave_secreta_aqui
```

> A `DATABASE_URL` é montada automaticamente pelo `docker-compose.yml` — não é necessário defini-la manualmente.

---

## Como Executar

### <img src="https://skillicons.dev/icons?i=github" height="20" style="vertical-align: middle;" /> 1. Clone o repositório

```bash
git clone https://github.com/paulo-campos-57/Projeto-TCC-BackEnd.git
cd Projeto-TCC-BackEnd
```

### 🐳 2. Configure as variáveis de ambiente

```bash
# Edite o .env.docker com suas credenciais
# Gere uma JWT_KEY segura
python -c "import secrets; print(secrets.token_hex(32))"
```

### ▶️ 3. Suba os serviços

```bash
docker compose up --build
```

A API estará disponível em **http://localhost:5000**.  
O PostgreSQL estará disponível em **localhost:5432**.

---

## Comandos Docker

| Comando | Descrição |
|---|---|
| `docker compose up --build` | Build da imagem e inicialização de todos os serviços |
| `docker compose up -d` | Inicia em segundo plano (modo detached) |
| `docker compose down` | Para e remove os containers (dados preservados) |
| `docker compose down -v` | Para e **apaga todos os dados** (volume removido) |
| `docker compose logs -f` | Acompanha os logs de todos os serviços |
| `docker compose logs -f api` | Acompanha os logs somente da API |
| `docker compose exec api bash` | Abre um shell dentro do container da API |
| `docker compose exec db psql -U tcc_user -d tcc_db` | Abre uma sessão psql |

---

## Rodando os Testes

```bash
# Executar todos os testes dentro do container
docker compose exec api pytest

# Executar um arquivo específico
docker compose exec api pytest tests/test_jogo_service.py

# Executar com saída detalhada
docker compose exec api pytest -v
```

---

## Visão Geral da API

| Prefixo | Descrição |
|---|---|
| `/user` | Cadastro, login, perfil e gerenciamento de conta |
| `/bairro` | Listagem de bairros e inicialização de sessão de jogo |
| `/jogo` | Ciclo completo da sessão de jogo (estoque, receita, preço, processamento do dia) |
| `/usuarios` | Estatísticas e histórico de partidas do jogador |

---

## Executar Sem Docker (alternativa)

<details>
<summary>Clique para expandir</summary>

### Requisitos
- Python 3.12+
- PostgreSQL 17+

### Passos

```bash
# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# Instalar dependências
pip install -r src/requirements.txt

# Criar src/.env com as credenciais do banco local
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tcc_db" >> src/.env
echo "JWT_KEY=sua_chave_secreta_aqui" >> src/.env

# Iniciar o servidor de desenvolvimento
python src/app.py
```

</details>

---

## Scripts Disponíveis

| Comando | Descrição |
|---|---|
| `docker compose exec api pytest` | Executa a suíte de testes |
| `docker compose exec api ruff check .` | Executa o linter |
| `docker compose exec api ruff format .` | Formata todos os arquivos fonte |
