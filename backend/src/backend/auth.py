import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import bcrypt
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from backend.db import conectar_banco

router = APIRouter(prefix="/auth", tags=["auth"])

TOKENS: dict[str, str] = {}


class RegistroRequest(BaseModel):
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
        (usuario_id, dados.email, senha_hash.decode("utf-8"), agora),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"id": str(usuario_id), "email": dados.email, "data_criacao": agora}
