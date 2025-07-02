import os
import redis
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    os.getenv("CORS_ORIGIN", "*")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("A variável de ambiente REDIS_URL não foi definida.")

r = redis.from_url(redis_url)

SUGGESTIONS_KEY = "suggestions:ranking"

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend-api"}


@app.get("/suggestions")
def get_suggestions(term: str):
    if not term:
        return []
    
    try:
        all_suggestions_bytes = r.zrange(SUGGESTIONS_KEY, 0, -1)
        
        all_suggestions = [s.decode('utf-8') for s in all_suggestions_bytes]

        term_lower = term.lower()
        matches = [s for s in all_suggestions if s.lower().startswith(term_lower)]
        
        if not matches:
            return []

        pipe = r.pipeline()
        for match in matches:
            pipe.zscore(SUGGESTIONS_KEY, match)
        scores = pipe.execute()

        suggestions_with_scores = sorted(
            [(matches[i], scores[i]) for i in range(len(matches)) if scores[i] is not None],
            key=lambda item: item[1],
            reverse=True
        )
        
        final_suggestions = [suggestion for suggestion, score in suggestions_with_scores]

        return [{"text": suggestion} for suggestion in final_suggestions[:20]]
    except Exception as e:
        print(f"Erro na busca: {e}")
        return []


@app.post("/suggestions/increment")
async def increment_suggestion_score(payload: dict = Body(...)):
    """Endpoint para incrementar o score de uma sugestão selecionada."""
    term = payload.get("term")
    if not term:
        return {"status": "error", "message": "Termo não fornecido"}
    try:
        r.zincrby(SUGGESTIONS_KEY, 1, term)
        return {"status": "success", "term": term}
    except Exception as e:
        print(f"Erro ao incrementar score: {e}")
        return {"status": "error", "message": str(e)}
