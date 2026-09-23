import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException

from backend.auth import obter_usuario_id_atual
from backend.db import conectar_banco
from backend.gemini_service import (
    GeminiIndisponivelError,
    GeminiRespostaVaziaError,
    gerar_perguntas,
    identificar_afirmacoes,
)

router_investigacoes = APIRouter(prefix="/investigacoes", tags=["afirmacoes"])
router_afirmacoes = APIRouter(prefix="/afirmacoes", tags=["afirmacoes"])


def _obter_afirmacao_com_posse(cursor, afirmacao_id: uuid.UUID, usuario_id: str):
    cursor.execute(
        """
        SELECT a.id, a.investigacao_id, a.fonte_id, a.texto, a.relevancia,
               a.data_criacao, i.usuario_id
        FROM AFIRMACAO a
        JOIN INVESTIGACAO i ON i.id = a.investigacao_id
        WHERE a.id = %s
        """,
        (str(afirmacao_id),),
    )

    resultado = cursor.fetchone()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Afirmação não encontrada")

    if str(resultado[6]) != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return {
        "id": str(resultado[0]),
        "investigacao_id": str(resultado[1]),
        "fonte_id": str(resultado[2]) if resultado[2] else None,
        "texto": resultado[3],
        "relevancia": resultado[4],
        "data_criacao": resultado[5],
    }


def _gerar_e_persistir_perguntas(cursor, afirmacao_id: str, texto_afirmacao: str):
    try:
        textos_perguntas = gerar_perguntas(texto_afirmacao)
    except GeminiRespostaVaziaError:
        raise HTTPException(
            status_code=422, detail="Nenhuma pergunta gerada"
        )
    except GeminiIndisponivelError:
        raise HTTPException(
            status_code=503, detail="Serviço de IA indisponível no momento"
        )

    agora = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
    perguntas_criadas = []

    for texto in textos_perguntas:
        pergunta_id = uuid.uuid4()

        cursor.execute(
            """
            INSERT INTO PERGUNTA
            (id, afirmacao_id, texto, resposta, tipo, data_criacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (str(pergunta_id), afirmacao_id, texto, None, None, agora),
        )

        perguntas_criadas.append(
            {
                "id": str(pergunta_id),
                "afirmacao_id": afirmacao_id,
                "texto": texto,
                "resposta": None,
                "tipo": None,
                "data_criacao": agora,
            }
        )

    return perguntas_criadas


@router_investigacoes.post("/{investigacao_id}/afirmacoes")
def criar_afirmacoes(
    investigacao_id: uuid.UUID,
    usuario_id: str = Depends(obter_usuario_id_atual),
):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT usuario_id, conteudo_original FROM INVESTIGACAO WHERE id = %s",
        (str(investigacao_id),),
    )

    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Investigação não encontrada")

    if str(resultado[0]) != usuario_id:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=403, detail="Acesso negado")

    conteudo_original = resultado[1]

    try:
        textos_afirmacoes = identificar_afirmacoes(conteudo_original)
    except GeminiRespostaVaziaError:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=422, detail="Nenhuma afirmação identificada"
        )
    except GeminiIndisponivelError:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=503, detail="Serviço de IA indisponível no momento"
        )

    agora = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
    afirmacoes_criadas = []

    for texto in textos_afirmacoes:
        afirmacao_id = uuid.uuid4()

        cursor.execute(
            """
            INSERT INTO AFIRMACAO
            (id, investigacao_id, fonte_id, texto, relevancia, data_criacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (str(afirmacao_id), str(investigacao_id), None, texto, None, agora),
        )

        afirmacoes_criadas.append(
            {
                "id": str(afirmacao_id),
                "investigacao_id": str(investigacao_id),
                "fonte_id": None,
                "texto": texto,
                "relevancia": None,
                "data_criacao": agora,
            }
        )

    conn.commit()

    cursor.close()
    conn.close()

    return afirmacoes_criadas


@router_afirmacoes.post("/{afirmacao_id}/perguntas")
def criar_perguntas(
    afirmacao_id: uuid.UUID,
    usuario_id: str = Depends(obter_usuario_id_atual),
):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        afirmacao = _obter_afirmacao_com_posse(cursor, afirmacao_id, usuario_id)
    except HTTPException:
        cursor.close()
        conn.close()
        raise

    try:
        perguntas_criadas = _gerar_e_persistir_perguntas(
            cursor, afirmacao["id"], afirmacao["texto"]
        )
    except HTTPException:
        cursor.close()
        conn.close()
        raise

    conn.commit()

    cursor.close()
    conn.close()

    return perguntas_criadas


@router_afirmacoes.post("/{afirmacao_id}/investigar")
def investigar_afirmacao(
    afirmacao_id: uuid.UUID,
    usuario_id: str = Depends(obter_usuario_id_atual),
):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        afirmacao = _obter_afirmacao_com_posse(cursor, afirmacao_id, usuario_id)
    except HTTPException:
        cursor.close()
        conn.close()
        raise

    try:
        perguntas_criadas = _gerar_e_persistir_perguntas(
            cursor, afirmacao["id"], afirmacao["texto"]
        )
    except HTTPException:
        cursor.close()
        conn.close()
        raise

    conn.commit()

    cursor.close()
    conn.close()

    afirmacao["perguntas"] = perguntas_criadas

    return afirmacao
