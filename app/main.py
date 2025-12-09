from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth_router
from app.api.routes.donor_router import router as donor_router

app = FastAPI(title="API Extensão")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(donor_router)

@app.get("/")
def root():
    return {"message": "Servidor rodando com sucesso 🚀"}
