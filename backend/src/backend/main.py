import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import conectar_banco

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {"mensagem": " funcionando"}


@app.post("/investigacoes")
def criar_investigacao(dados: dict):

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
            dados["usuario_id"],
            dados["titulo"],
            dados["tipo_entrada"],
            dados["conteudo_original"],
            dados["status"],
            agora,
            agora,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Investigação criada com sucesso", "id": str(investigacao_id)}


@app.get("/investigacoes")
def listar_investigacoes():

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
        """
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
