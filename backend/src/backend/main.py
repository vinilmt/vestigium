from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.afirmacoes import router_afirmacoes, router_investigacoes
from backend.auth import router as auth_router
from backend.investigacoes import router as investigacoes_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(investigacoes_router)
app.include_router(router_investigacoes)
app.include_router(router_afirmacoes)


@app.get("/")
def inicio():
    return {"mensagem": " funcionando"}
