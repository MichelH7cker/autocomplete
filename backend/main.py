from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import os

app = FastAPI()

# configuração do CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

SUGGESTIONS_KEY = "suggestions_v1"

@app.get("/suggestions")
def get_suggestions(term: str):
    if not term:
        return []

    try:
        # O truque `\xff` é um caractere que representa o "final" do range da busca
        results = r.zrangebylex(
            SUGGESTIONS_KEY,
            f"[{term.lower()}",
            f"[{term.lower()}\xff"
        )
        
        all_suggestions = r.zrange(SUGGESTIONS_KEY, 0, -1)
        matches = [s for s in all_suggestions if s.lower().startswith(term.lower())]

        return [{"text": suggestion} for suggestion in matches[:20]]
    except Exception:
        return []

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend-api"}
