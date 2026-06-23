from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.github_controller import router as github_router
import config

app = FastAPI(title="Prisma Insight API")

# Segurança: Protegendo contra chamadas externas indesejadas
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",      # VS Code Live Server
        "http://localhost:5500",
        "https://unb-mds.github.io"   # Futuro ambiente de produção do GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Registrando o controller corretamente
app.include_router(github_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "PRISMA Analytics Engine Operacional", "version": "1.0.0"}