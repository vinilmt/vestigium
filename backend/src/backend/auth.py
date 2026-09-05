import secrets
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import bcrypt
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from backend.db import conectar_banco

router = APIRouter(prefix="/auth", tags=["auth"])

TOKENS: dict[str, str] = {}


class RegistroRequest(BaseModel):
    email: str
    senha: str


class LoginRequest(BaseModel):
    email: str
    senha: str


def obter_usuario_id_atual(x_token: str = Header(...)) -> str:
    usuario_id = TOKENS.get(x_token)

    if usuario_id is None:
        raise HTTPException(status_code=403, detail="Token inválido")

    return usuario_id


@router.post("/register")
def registrar(dados: RegistroRequest):
    senha_hash = bcrypt.hashpw(dados.senha.encode("utf-8"), bcrypt.gensalt())

    conn = conectar_banco()
    cursor = conn.cursor()

    agora = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
    usuario_id = uuid.uuid4()

    cursor.execute(
        """
        INSERT INTO USUARIO (id, email, senha_hash, data_criacao)
        VALUES (%s, %s, %s, %s)
        """,
        (str(usuario_id), dados.email, senha_hash.decode("utf-8"), agora),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"id": str(usuario_id), "email": dados.email, "data_criacao": agora}


@router.post("/login")
def login(dados: LoginRequest):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, senha_hash FROM USUARIO WHERE email = %s",
        (dados.email,),
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is None:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    usuario_id, senha_hash = resultado

    if not bcrypt.checkpw(dados.senha.encode("utf-8"), senha_hash.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = secrets.token_hex(32)
    TOKENS[token] = str(usuario_id)

    return {"token": token}


@router.get("/me")
def me(usuario_id: str = Depends(obter_usuario_id_atual)):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, data_criacao FROM USUARIO WHERE id = %s",
        (usuario_id,),
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is None:
        raise HTTPException(status_code=403, detail="Token inválido")

    return {
        "id": str(resultado[0]),
        "email": resultado[1],
        "data_criacao": resultado[2],
    }


@router.post("/logout")
def logout(x_token: str = Header(...)):
    TOKENS.pop(x_token, None)

    return {"mensagem": "Sessão encerrada"}
