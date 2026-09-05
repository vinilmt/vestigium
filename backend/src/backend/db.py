import os

import psycopg2


def conectar_banco():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
