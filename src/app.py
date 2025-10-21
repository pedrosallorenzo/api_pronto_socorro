# Liga a API e as rotas do sistema

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.paciente_routes import router as paciente_router
from src.routes.triagem_routes import router as triagem_router

app = FastAPI(title="API de Pronto Socorro")

# CORS: libera para testes locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção restrinja
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(paciente_router)
app.include_router(triagem_router)


# rota de saúde rápida
@app.get("/ping")
def ping():
    return {"msg": "pong"}
