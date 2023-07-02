from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import psycopg2

from model import database, Usuario, Agendamento, agendamento
import databases

app = FastAPI()


#auth 
# Configurações de autenticação
SECRET_KEY = "mysecretkey"  # Chave secreta para assinar o token JWT
ALGORITHM = "HS256"  # Algoritmo de criptografia para o token JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de validade do token JWT

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "clinica"
DB_USER = "postgres"
DB_PASSWORD = "524652"

# Funções auxiliares
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        user = {
            "username": user[0],
            "password": user[1],
            "role": user[2]
        }
        return user

    return None

def authenticate_user(username, password):
    user = get_user(username)
    if not user or not verify_password(password, user["password"]):
        return None

    return user

def create_access_token(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rotas
@app.post("/login")
async def login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user["username"], "role": user["role"]}, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected(credentials: HTTPAuthorizationCredentials):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Falha na autenticação")
        return {"mensagem": "Acesso autorizado", "usuario": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# start e shutdown
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

#getters 
@app.get("/agendamentos/", response_model=list[Agendamento])
async def listarAgendamentos():
    query = agendamento.select()
    return await database.fetch_all(query)


#Post

@app.post("/agendamentos", response_model=Agendamento)
async def criaAgendamento(agendamentos : Agendamento):
    query = agendamento.insert().values(nomePaciente = agendamentos.nome_paciente,
    descriçao = agendamentos.descriçao, data = agendamentos.data_hora )

    last_record_id = await database.execute(query)
    return {**agendamentos.dict(), "id": last_record_id}


