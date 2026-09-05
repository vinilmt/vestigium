import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.auth import obter_usuario_id_atual
from backend.db import conectar_banco

router = APIRouter(prefix="/investigacoes", tags=["investigacoes"])

TIPOS_ENTRADA_VALIDOS = {"url", "texto"}
STATUS_INICIAL = "em_andamento"


class InvestigacaoCreate(BaseModel):
    titulo: str
    tipo_entrada: str
    conteudo_original: str


def validar_tipo_entrada(tipo_entrada: str) -> None:
    if tipo_entrada not in TIPOS_ENTRADA_VALIDOS:
        raise HTTPException(
            status_code=422,
            detail="tipo_entrada deve ser 'url' ou 'texto'",
        )


@router.post("")
def criar_investigacao(
    dados: InvestigacaoCreate,
    usuario_id: str = Depends(obter_usuario_id_atual),
):
    if not dados.titulo.strip() or not dados.conteudo_original.strip():
        raise HTTPException(
            status_code=422,
            detail="titulo e conteudo_original não podem estar vazios",
        )

    validar_tipo_entrada(dados.tipo_entrada)

    conn = conectar_banco()
    cursor = conn.cursor()

    agora = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
    investigacao_id = uuid.uuid4()

    cursor.execute(
        """
        INSERT INTO INVESTIGACAO
        (
            id,
            usuario_id,
            titulo,
            tipo_entrada,
            conteudo_original,
            status,
            data_criacao,
            data_atualizacao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            investigacao_id,
            usuario_id,
            dados.titulo,
            dados.tipo_entrada,
            dados.conteudo_original,
            STATUS_INICIAL,
            agora,
            agora,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Investigação criada com sucesso", "id": str(investigacao_id)}
