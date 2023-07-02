from typing import List
from datetime import datetime
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel


DATABASE_URL = 'postgresql://postgres:524652@localhost/clinica'
database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()



# tabelas 
agendamento = sqlalchemy.Table(
    "agendamento",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key =True),
    sqlalchemy.Column("nomePaciente", sqlalchemy.String),
    sqlalchemy.Column("data_hora", sqlalchemy.String),
    sqlalchemy.Column("descriçao", sqlalchemy.String)
)

usuario = sqlalchemy.Table(
    "usuario",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nome", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("senha", sqlalchemy.String)
)


#modelos

class Agendamento(BaseModel):
    id : int
    nome_paciente : str
    data_hora : str
    descriçao : str 
    

class Usuario(BaseModel):
    id : int
    nome : str 
    email : str 
    senha : str 


