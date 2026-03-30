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
  </p>
</div>

This repository contains the Back-End of <a href="https://github.com/paulo-campos-57" target="_blank">Paulo Campos</a>'s Final Graduation Project (TCC).<br>
The full project documentation can be found at this <a href="https://docs.google.com/document/d/1WqyVEorM9IbZZ5CjwYWsqjv00DI9vhe-/edit?usp=sharing&ouid=104768249469194230645&rtpof=true&sd=true" target="_blank">link</a>.

---

## Project Structure

```
src/
├── models/
│   ├── user.py           # SQLAlchemy user model
│   ├── bairro.py         # Neighbourhood data model
│   ├── ingrediente.py    # Ingredient catalogue (server-side only)
│   └── sessao_jogo.py    # In-memory game session state
├── routes/
│   ├── user_routes.py    # Auth & profile endpoints (/user)
│   ├── bairro_routes.py  # Neighbourhood endpoints (/bairro)
│   └── jogo_routes.py    # Game session endpoints (/jogo)
├── services/
│   ├── user_service.py   # User business logic
│   ├── bairro_service.py # Neighbourhood business logic
│   └── jogo_service.py   # Game simulation business logic
├── database.py           # SQLAlchemy instance
└── app.py                # Application factory & blueprint registry
```

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| [Python](https://www.python.org/) | 3.12 | Primary language |
| [Flask](https://flask.palletsprojects.com/) | 3.x | Web framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.x | ORM |
| [PostgreSQL](https://www.postgresql.org/) | 17 | Relational database |
| [bcrypt](https://pypi.org/project/bcrypt/) | 4.x | Password hashing |
| [PyJWT](https://pyjwt.readthedocs.io/) | — | JWT authentication |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | — | Cross-origin resource sharing |
| [Ruff](https://docs.astral.sh/ruff/) | — | Linter & formatter |

---

## Requirements

To run this project locally, make sure you have the following installed:

- **Python** 3.12 or higher
- **pip** (bundled with Python)
- **PostgreSQL** 17 or higher (or Docker)

> Don't have PostgreSQL? Run it with Docker: `docker run --name tcc-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:17`

---

## Environment Variables

Create a `.env` file inside the `src/` directory with the following variables:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tcc_db
JWT_KEY=your_secret_key_here
```

---

## How to Run

### <img src="https://skillicons.dev/icons?i=github" height="20" style="vertical-align: middle;" /> 1. Clone the repository

```bash
git clone https://github.com/paulo-campos-57/Projeto-TCC-BackEnd.git
cd Projeto-TCC-BackEnd
```

### <img src="https://skillicons.dev/icons?i=python" height="20" style="vertical-align: middle;" /> 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 📦 3. Install dependencies

```bash
pip install -r src/requirements.txt
```

### ▶️ 4. Start the development server

```bash
python src/app.py
```

The Back-End will be available at **http://localhost:5000**.

---

## API Overview

| Prefix | Description |
|---|---|
| `/user` | Registration, login, profile, and account management |
| `/bairro` | Neighbourhood listing and game session initialisation |
| `/jogo` | Full game session lifecycle (stock, recipe, pricing, day processing) |

---

## Available Scripts

| Command | Description |
|---|---|
| `python src/app.py` | Starts the local development server |
| `ruff check src/` | Runs the linter across all source files |
| `ruff format src/` | Formats all source files |

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
  </p>
</div>

Este repositório contém o Back-End do Trabalho de Conclusão de Curso de <a href="https://github.com/paulo-campos-57" target="_blank">Paulo Campos</a>.<br>
A documentação completa do projeto pode ser encontrada neste <a href="https://docs.google.com/document/d/1WqyVEorM9IbZZ5CjwYWsqjv00DI9vhe-/edit?usp=sharing&ouid=104768249469194230645&rtpof=true&sd=true" target="_blank">link</a>.

---

## Estrutura do Projeto

```
src/
├── models/
│   ├── user.py           # Model SQLAlchemy de usuário
│   ├── bairro.py         # Model de dados de bairro
│   ├── ingrediente.py    # Catálogo de ingredientes (somente servidor)
│   └── sessao_jogo.py    # Estado da sessão de jogo em memória
├── routes/
│   ├── user_routes.py    # Endpoints de autenticação e perfil (/user)
│   ├── bairro_routes.py  # Endpoints de bairros (/bairro)
│   └── jogo_routes.py    # Endpoints da sessão de jogo (/jogo)
├── services/
│   ├── user_service.py   # Lógica de negócio de usuários
│   ├── bairro_service.py # Lógica de negócio de bairros
│   └── jogo_service.py   # Lógica de simulação do jogo
├── database.py           # Instância do SQLAlchemy
└── app.py                # Fábrica da aplicação e registro de blueprints
```

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| [Python](https://www.python.org/) | 3.12 | Linguagem principal |
| [Flask](https://flask.palletsprojects.com/) | 3.x | Framework web |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.x | ORM |
| [PostgreSQL](https://www.postgresql.org/) | 17 | Banco de dados relacional |
| [bcrypt](https://pypi.org/project/bcrypt/) | 4.x | Hash de senhas |
| [PyJWT](https://pyjwt.readthedocs.io/) | — | Autenticação JWT |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | — | Controle de origem cruzada |
| [Ruff](https://docs.astral.sh/ruff/) | — | Linter e formatador |

---

## Requisitos

Para rodar o projeto localmente, certifique-se de ter instalado:

- **Python** 3.12 ou superior
- **pip** (incluso com o Python)
- **PostgreSQL** 17 ou superior (ou Docker)

> Não tem o PostgreSQL? Execute com Docker: `docker run --name tcc-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:17`

---

## Variáveis de Ambiente

Crie um arquivo `.env` dentro do diretório `src/` com as seguintes variáveis:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tcc_db
JWT_KEY=sua_chave_secreta_aqui
```

---

## Como Executar

### <img src="https://skillicons.dev/icons?i=github" height="20" style="vertical-align: middle;" /> 1. Clone o repositório

```bash
git clone https://github.com/paulo-campos-57/Projeto-TCC-BackEnd.git
cd Projeto-TCC-BackEnd
```

### <img src="https://skillicons.dev/icons?i=python" height="20" style="vertical-align: middle;" /> 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 📦 3. Instale as dependências

```bash
pip install -r src/requirements.txt
```

### ▶️ 4. Inicie o servidor de desenvolvimento

```bash
python src/app.py
```

O Back-End estará disponível em **http://localhost:5000**.

---

## Visão Geral da API

| Prefixo | Descrição |
|---|---|
| `/user` | Cadastro, login, perfil e gerenciamento de conta |
| `/bairro` | Listagem de bairros e inicialização de sessão de jogo |
| `/jogo` | Ciclo completo da sessão de jogo (estoque, receita, preço, processamento do dia) |

---

## Scripts Disponíveis

| Comando | Descrição |
|---|---|
| `python src/app.py` | Inicia o servidor local de desenvolvimento |
| `ruff check src/` | Executa o linter em todos os arquivos fonte |
| `ruff format src/` | Formata todos os arquivos fonte |
