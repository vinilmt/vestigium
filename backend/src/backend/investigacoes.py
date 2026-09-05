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


@router.get("")
def listar_investigacoes(usuario_id: str = Depends(obter_usuario_id_atual)):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            usuario_id,
            titulo,
            tipo_entrada,
            conteudo_original,
            status,
            data_criacao,
            data_atualizacao
        FROM INVESTIGACAO
        WHERE usuario_id = %s
        """,
        (usuario_id,),
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    investigacoes = []

    for item in resultados:
        investigacoes.append(
            {
                "id": str(item[0]),
                "usuario_id": str(item[1]),
                "titulo": item[2],
                "tipo_entrada": item[3],
                "conteudo_original": item[4],
                "status": item[5],
                "data_criacao": item[6],
                "data_atualizacao": item[7],
            }
        )

    return investigacoes


@router.get("/{investigacao_id}")
def buscar_investigacao(
    investigacao_id: uuid.UUID,
    usuario_id: str = Depends(obter_usuario_id_atual),
):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            usuario_id,
            titulo,
            tipo_entrada,
            conteudo_original,
            status,
            data_criacao,
            data_atualizacao
        FROM INVESTIGACAO
        WHERE id = %s
        """,
        (str(investigacao_id),),
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Investigação não encontrada")

    if str(resultado[1]) != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return {
        "id": str(resultado[0]),
        "usuario_id": str(resultado[1]),
        "titulo": resultado[2],
        "tipo_entrada": resultado[3],
        "conteudo_original": resultado[4],
        "status": resultado[5],
        "data_criacao": resultado[6],
        "data_atualizacao": resultado[7],
    }
