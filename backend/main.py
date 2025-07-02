import uvicorn
import os
import redis
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from seed import populate_db # Importa a função do nosso outro arquivo

if __name__ == "__main__":
    populate_db()
    
    port = int(os.getenv("PORT", 8000))
    
    print(f"Iniciando servidor Uvicorn em http://0.0.0.0:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

app = FastAPI()

origins = [os.getenv("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = None
try:
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        r = redis.from_url(redis_url)
        print("Conexão com Redis estabelecida para a aplicação FastAPI.")
    else:
        print("ALERTA: Variável REDIS_URL não encontrada.")
except Exception as e:
    print(f"ALERTA: Falha ao iniciar a conexão principal com o Redis: {e}")

SUGGESTIONS_KEY = "suggestions:ranking"

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/suggestions")
def get_suggestions(term: str):
    if not term or not r: return []
    try:
        all_suggestions_bytes = r.zrange(SUGGESTIONS_KEY, 0, -1)
        all_suggestions = [s.decode('utf-8') for s in all_suggestions_bytes]

        term_lower = term.lower()
        matches = [s for s in all_suggestions if s.lower().startswith(term_lower)]
        
        if not matches: return []

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
    if not r: return {"status": "error", "message": "Redis não conectado"}
    term = payload.get("term")
    if not term: return {"status": "error", "message": "Termo não fornecido"}
    try:
        r.zincrby(SUGGESTIONS_KEY, 1, term)
        return {"status": "success", "term": term}
    except Exception as e:
        print(f"Erro ao incrementar score: {e}")
        return {"status": "error", "message": str(e)}
