import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException

from backend.auth import obter_usuario_id_atual
from backend.db import conectar_banco
from backend.gemini_service import (
    GeminiIndisponivelError,
    GeminiRespostaVaziaError,
    identificar_afirmacoes,
)

router_investigacoes = APIRouter(prefix="/investigacoes", tags=["afirmacoes"])
router_afirmacoes = APIRouter(prefix="/afirmacoes", tags=["afirmacoes"])


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
