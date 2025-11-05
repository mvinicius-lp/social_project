from fastapi import FastAPI
from app.api.routes import auth_router

app = FastAPI(title="API Extensão")

app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "Servidor rodando com sucesso 🚀"}
