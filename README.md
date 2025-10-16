# Sistema de Gestão Hospitalar - Backend

Backend de um Sistema de Gestão Hospitalar moderno desenvolvido com Django e Django REST Framework. Esta API oferece recursos completos para gerenciamento de:

- **Pacientes** - Cadastro, histórico médico, admissões
- **Agendamentos** - Consultas, exames, procedimentos
- **Departamentos** - Gestão de setores hospitalares
- **Medicamentos** - Inventário, prescrições, administração
- **Funcionários** - Médicos, enfermeiros, administradores
- **Operações** - Tarefas, processos e workflows
- **IA Integrada** - RAG (Retrieval-Augmented Generation) para consultas inteligentes

## Tecnologias Utilizadas

- **Django 5.2.7** - Framework web principal
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados principal (SQLite para desenvolvimento)
- **Sentence Transformers** - Embeddings para busca semântica
- **FAISS** - Indexação vetorial para RAG
- **PyTorch** - Machine Learning backend

## Pré-requisitos

- **Python 3.8+** (recomendado Python 3.11+)
- **Git** para versionamento
- **PostgreSQL** (opcional, para produção)

## Guia de Instalação e Execução

### 1. Clone o Repositório

```bash
git clone https://github.com/tonyzinh/system-hospital-backend.git
cd system-hospital-backend
```

### 2. Crie e Ative o Ambiente Virtual

#### Windows (PowerShell/CMD)
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# PowerShell:
.venv\Scripts\Activate.ps1
# CMD:
.venv\Scripts\activate
```

#### Linux/macOS
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **💡 Dica para PyTorch**: Para acelerar a instalação ou usar GPU, instale o PyTorch apropriado primeiro:
> ```bash
> # CPU apenas
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> # CUDA 12.1 (exemplo)
> pip install torch --index-url https://download.pytorch.org/whl/cu121
> ```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=America/Sao_Paulo

# Database (opcional - deixe vazio para usar SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/hospital_db

# CORS (opcional)
# CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Executar Migrações do Banco de Dados

```bash
# Criar migrações para os apps customizados
python manage.py makemigrations core patients medicaments ops

# Aplicar todas as migrações
python manage.py migrate
```

### 6. Criar Superusuário (Opcional)

```bash
python manage.py createsuperuser
```

### 7. Executar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://127.0.0.1:8000/**

## Estrutura da API

### Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/admin/` | GET | Interface administrativa Django |
| `/api/v1/patients/` | GET, POST | Lista e cria pacientes |
| `/api/v1/appointments/` | GET, POST | Gerencia agendamentos |
| `/api/v1/medications/` | GET, POST | Inventário de medicamentos |
| `/api/v1/prescriptions/` | GET, POST | Prescrições médicas |
| `/api/v1/departments/` | GET, POST | Departamentos hospitalares |

### Autenticação

A API utiliza autenticação baseada em sessão do Django. Para acessar endpoints protegidos:

1. Faça login via `/admin/` ou
2. Use autenticação programática via DRF

## Funcionalidades de IA

### RAG (Retrieval-Augmented Generation)

O sistema inclui capacidades de busca inteligente e geração de respostas:

```bash
# Ingerir conteúdo web para a base de conhecimento
python manage.py ingest_web https://example.com/medical-info

# Fazer consulta inteligente
python manage.py query "Quais são os efeitos colaterais do ibuprofeno?"
```

## Estrutura do Projeto

```
system-hospital-backend/
├── apps/
│   ├── core/           # Modelos base (User, AuditLog)
│   ├── patients/       # Gestão de pacientes
│   ├── medicaments/    # Medicamentos e prescrições
│   ├── ops/           # Operações e tarefas
│   └── ai/            # IA e RAG
├── config/
│   ├── settings/      # Configurações por ambiente
│   ├── urls.py        # URLs principais
│   └── wsgi.py        # WSGI para produção
├── api/
│   └── urls.py        # URLs da API
├── requirements.txt   # Dependências Python
└── manage.py         # Utilitário Django
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Comandos Úteis

```bash
# Fazer backup do banco
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json

# Coletar arquivos estáticos (produção)
python manage.py collectstatic

# Verificar problemas de configuração
python manage.py check

# Shell interativo do Django
python manage.py shell
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Tony** - [@tonyzinh](https://github.com/tonyzinh)
