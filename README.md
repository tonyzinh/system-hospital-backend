# Sistema Hospitalar - Backend

> **Sistema de gestão hospitalar inteligente com IA integrada para otimização de processos médicos e administrativos**

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-yellow.svg)

---

## Descrição

O **Sistema Hospitalar Backend** é uma solução completa para gestão de instituições de saúde, desenvolvido com Django e integrando tecnologias de Inteligência Artificial para otimizar processos médicos e administrativos.

### Link do Vídeo
Youtube:

### Objetivos

- **Gestão Completa**: Administração de pacientes, funcionários, medicamentos e operações hospitalares
- **IA Integrada**: Utilização de modelos de linguagem (LLM) via Ollama para assistência médica inteligente
- **Escalabilidade**: Arquitetura modular e API RESTful para integração com diferentes sistemas
- **Eficiência**: Automação de processos repetitivos e otimização do fluxo de trabalho hospitalar

### Funcionalidades Principais

- **Gestão de Pacientes**: Cadastro, histórico médico e acompanhamento
- **Controle de Medicamentos**: Prescrições, estoque e interações medicamentosas
- **Agendamento**: Sistema inteligente de consultas e procedimentos
- **Internações**: Controle de admissões e altas hospitalares
- **IA Médica**: Assistente virtual para diagnósticos e recomendações
- **API RESTful**: Endpoints completos para integração com aplicações frontend
- **Relatórios**: Análises e métricas de desempenho hospitalar

---

## Tecnologias Utilizadas

### Backend & Framework
- ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.9+**
- ![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white) **Django 5.2+**
- ![DRF](https://img.shields.io/badge/-Django_REST_Framework-092E20?style=flat&logo=django&logoColor=white) **Django REST Framework**

### Banco de Dados
- ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white) **PostgreSQL** (Produção)
---

## Equipe

### Desenvolvedores
- **Bernardo Antônio Merlo Soares**
- **Bruno Emanuel Sales Rocha**
- **Entony Jovino dos Santos**
- **Kaio Barbosa Linhares**
- **Raphael Simões Gomes**
- **Rikelme Mindelo Biague**
- **Rafael Barcelos de Aquino Moura**

### Orientação Acadêmica
- **Prof. Howard Cruz Roatti** - *Orientador* - FAESA Centro Universitário

---

## Como Executar o Projeto

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Ollama (para funcionalidades de IA)

### 1. Clonar o Repositório

```bash
# Clone o repositório
git clone https://github.com/tonyzinh/system-hospital-backend.git

# Entre no diretório
cd system-hospital-backend
```

### 2. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
# Instalar todas as dependências
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados

```bash
# Executar migrações
python manage.py makemigrations
python manage.py migrate

# (Opcional) Carregar dados de exemplo
python manage.py loaddata fixtures/sample_data.json

# Criar superusuário
python manage.py createsuperuser
```

### 5. Configurar Ollama (IA)

```bash
# Instalar Ollama
# Visite: https://ollama.com/download

# Baixar modelo recomendado
ollama pull llama3.1

# Iniciar servidor Ollama
ollama serve
```

### 6. Executar o Projeto

```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# O servidor estará disponível em:
# http://127.0.0.1:8000/
```

### 7. Executar Testes (Opcional)

```bash
# Executar todos os testes
python -m pytest

# Executar testes com cobertura
python -m pytest --cov=apps

# Executar testes de uma app específica
python -m pytest tests/test_patients.py
```

---

## 📁 Estrutura do Projeto

```
system-hospital-backend/
├── 📁 api/                 # Configuração da API
├── 📁 apps/                # Aplicações Django
│   ├── core/           # Funcionalidades centrais
│   ├── ai/             # Integração com IA/LLM
│   ├── medicaments/    # Gestão de medicamentos
│   ├── ops/            # Operações hospitalares
│   └── patients/       # Gestão de pacientes
├── 📁 config/             # Configurações Django
│   ├── settings/          # Configurações por ambiente
│   ├── settings.py        # Configurações principais
│   └── urls.py           # URLs principais
├── 📁 fixtures/           # Dados de exemplo
├── 📁 tests/             # Testes automatizados
├── 📄 manage.py          # Comando principal Django
├── 📄 requirements.txt   # Dependências Python
└── 📄 README.md         # Este arquivo
```

### Descrição dos Módulos

| Módulo | Descrição |
|--------|-----------|
| `core` | Autenticação, usuários e funcionalidades base |
| `patients` | Gestão completa de pacientes e internações |
| `medicaments` | Controle de medicamentos e prescrições |
| `ops` | Operações e procedimentos hospitalares |
| `ai` | Integração com IA para assistência médica |

---

## Endpoints da API

### Pacientes

- `GET /api/v1/patients/` - Listar pacientes
- `POST /api/v1/patients/` - Criar paciente
- `GET /api/v1/patients/{id}/` - Detalhes do paciente
- `PUT /api/v1/patients/{id}/` - Atualizar paciente

### Medicamentos
- `GET /api/v1/medicaments/` - Listar medicamentos
- `POST /api/v1/medicaments/prescription/` - Nova prescrição

### IA Médica
- `POST /api/v1/ai/chat/` - Chat com assistente médico
- `POST /api/v1/ai/diagnosis/` - Sugestões de diagnóstico

### Relatórios
- `GET /api/v1/reports/patients/` - Relatório de pacientes
- `GET /api/v1/reports/operations/` - Relatório de operações

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/hospital_db

# Ollama IA
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.1
OLLAMA_TIMEOUT=120
OLLAMA_SYSTEM="Você é um assistente médico especializado."

# Cache
CACHE_ENABLED=True
CACHE_SIZE_LIMIT=100
```

---

## Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2024 Sistema Hospitalar Backend

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Links Úteis

- 📚 **[Repositório no GitHub Backend](https://github.com/tonyzinh/system-hospital-backend)**
- 📚 **[Repositório no GitHub Frontend](https://github.com/tonyzinh/system-hospital-frontend)**

### Documentação Técnica
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Ollama Documentation](https://github.com/ollama/ollama)

---

## Contribuições

Contribuições são sempre bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/['Sua Branch']`)
3. Commit suas mudanças (`git commit -m 'Sua Mensagem'`)
4. Push para a branch (`git push origin feature/['Sua Branch']`)
5. Abra um Pull Request

---
