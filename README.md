# Sistema de Gestão Hospitalar - Backend

Este repositório contém o backend para um Sistema de Gestão Hospitalar, desenvolvido com Django e Django REST Framework. A API RESTful permite o gerenciamento de pacientes, agendamentos, filas de atendimento e funcionários.

## Funcionalidades

  - **Gestão de Pacientes:** API completa para criar, listar, atualizar e apagar registos de pacientes.
  - **Autenticação Segura:** Sistema de autenticação baseado em tokens para proteger os endpoints da API.
  - **Painel de Administração:** Interface de administração completa e pronta a usar, fornecida pelo Django Admin, para uma gestão de dados fácil e rápida.
  - **Pronto para Docker:** Inclui ficheiros `Dockerfile` e `docker-compose.yml` para configurar e executar o ambiente de desenvolvimento de forma rápida e consistente.

## 🛠️ Tecnologias Utilizadas

  - **Backend:**
      - Python
      - Django
      - Django REST Framework
  - **Base de Dados:**
      - PostgreSQL
  - **Ambiente de Desenvolvimento:**
      - Docker & Docker Compose

## Como Executar o Projeto

Existem duas formas de executar o projeto: localmente com um ambiente virtual Python ou utilizando Docker.

### Pré-requisitos

  - Python 3.10+
  - Git
  - Docker e Docker Compose (para o método com Docker)

### 1\. Configuração com Docker (Recomendado)

Este é o método mais simples e rápido para iniciar.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/system-hospital-backend.git
    cd system-hospital-backend
    ```

2.  **Crie o ficheiro de ambiente:**
    Copie o conteúdo do seu ficheiro `.env` para um novo ficheiro com o mesmo nome na raiz do projeto. Certifique-se de que as variáveis da base de dados correspondem às do `docker-compose.yml`.

3.  **Inicie os contentores:**
    Este comando irá construir a imagem do Django e iniciar o contentor da aplicação e da base de dados PostgreSQL.

    ```bash
    docker-compose up --build
    ```

4.  **A aplicação estará disponível em:**

      - API: `http://localhost:8000/api/patients/`
      - Painel de Administração: `http://localhost:8000/admin/`

### 2\. Configuração Local (Sem Docker)

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/system-hospital-backend.git
    cd system-hospital-backend
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um ficheiro `.env` na raiz do projeto e adicione as variáveis necessárias, como `SECRET_KEY` e `DATABASE_URL`.

5.  **Aplique as migrações da base de dados:**

    ```bash
    python manage.py migrate
    ```

6.  **Crie um superutilizador:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicie o servidor de desenvolvimento:**

    ```bash
    python manage.py runserver
    ```

## Como Usar a API

A API está protegida e requer um token de autenticação para ser acedida.

### 1\. Obter um Token de Autenticação

Execute o seguinte comando no terminal para gerar um token para um utilizador existente (substitua `seu_username`):

```bash
python manage.py drf_create_token seu_username
```

Copie o token gerado.

### 2\. Fazer Requisições (Exemplo com Postman)

  - **Listar Pacientes (GET):**

      - **URL:** `http://127.0.0.1:8000/api/patients/`
      - **Authorization:** `Bearer Token`
      - **Token:** Cole o seu token aqui.

  - **Criar um Novo Paciente (POST):**

      - **URL:** `http://127.0.0.1:8000/api/patients/`
      - **Authorization:** `Bearer Token`
      - **Body:** `raw`, `JSON`
      - **Conteúdo do Body:**
        ```json
        {
            "full_name": "Nome Completo do Paciente",
            "birth_date": "YYYY-MM-DD",
            "cpf": "123.456.789-00"
        }
        ```

-----