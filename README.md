# API Clínica

Esta é uma API baseada em FastAPI para um sistema de gerenciamento de clínica. Ela permite que os usuários criem e gerenciem agendamentos e fornece autenticação básica de usuários.

## Sumário

- [Instalação](#instalação)
- [Uso](#uso)
- [Autenticação](#autenticação)
- [Endpoints](#endpoints)
- [Modelos](#modelos)

## Instalação

1. Clone o repositório em sua máquina local:

```
git clone https://github.com/seu-usuário/api-clinica.git
cd api-clinica
```

2. Instale as dependências necessárias:

```
pip install -r requirements.txt
```

3. Configure o banco de dados:

   - Instale o PostgreSQL e crie um banco de dados chamado "clinica".
   - Atualize a configuração do banco de dados no arquivo `main.py`:

```python
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "clinica"
DB_USER = "postgres"
DB_PASSWORD = "sua-senha-do-postgres"
```

4. Execute a aplicação:

```
uvicorn main:app --reload
```

A API estará acessível em http://localhost:8000.

## Uso

Para utilizar a API, você pode interagir com ela programaticamente usando clientes HTTP ou testar os endpoints fornecidos através da interface Swagger do FastAPI. Acesse http://localhost:8000/docs em seu navegador para acessar a documentação interativa da API.

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação de usuários. Para acessar endpoints protegidos, você precisa obter um token de acesso enviando uma requisição POST para o endpoint `/login` com credenciais válidas de usuário (nome de usuário e senha). O token de acesso deve ser incluído no cabeçalho `Authorization` das requisições subsequentes como `Bearer <token_de_acesso>`.

## Endpoints

### Autenticação

- `POST /login`: Obtenha um token de acesso fornecendo credenciais válidas de usuário (nome de usuário e senha).

### Usuários

- `POST /users/`: Crie um novo usuário. (Requer acesso de administrador)

### Agendamentos

- `GET /agendamentos/`: Liste todos os agendamentos.
- `GET /agendamentos/{agendamento_id}`: Obtenha detalhes de um agendamento específico pelo ID.
- `POST /agendamentos`: Crie um novo agendamento.
- `PUT /agendamentos/{agendamento_id}`: Atualize um agendamento existente pelo ID.
- `DELETE /agendamentos/{agendamento_id}`: Exclua um agendamento pelo ID.

## Modelos

### Usuario

- `id` (inteiro): O identificador único do usuário.
- `username` (string): O nome de usuário do usuário.
- `password` (string): A senha criptografada do usuário.
- `role` (string): O papel do usuário (por exemplo, "admin", "médico", "paciente").

### Agendamento

- `id` (inteiro): O identificador único do agendamento.
- `nome_paciente` (string): O nome do paciente para o agendamento.
- `descriçao` (string): A descrição do agendamento.
- `data_hora` (datetime): A data e hora do agendamento.

