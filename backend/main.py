from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import redis
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

SUGGESTIONS_KEY = "suggestions:ranking"

@app.get("/suggestions")
def get_suggestions(term: str):
    if not term:
        return []
    
    try:
        all_suggestions = r.zrange(SUGGESTIONS_KEY, 0, -1)
        
        term_lower = term.lower()
        matches = [s for s in all_suggestions if s.lower().startswith(term_lower)]
        
        if not matches:
            return []

        pipe = r.pipeline()
        for match in matches:
            pipe.zscore(SUGGESTIONS_KEY, match)
        scores = pipe.execute()

        suggestions_with_scores = sorted(zip(matches, scores), key=lambda item: item[1], reverse=True)
        
        final_suggestions = [suggestion for suggestion, score in suggestions_with_scores]

        return [{"text": suggestion} for suggestion in final_suggestions[:20]]
    except Exception as e:
        print(f"Erro na busca: {e}")
        return []

@app.post("/suggestions/increment")
async def increment_suggestion_score(payload: dict = Body(...)):
    term = payload.get("term")
    if not term:
        return {"status": "error", "message": "Termo não fornecido"}
    
    try:
        r.zincrby(SUGGESTIONS_KEY, 1, term)
        return {"status": "success", "term": term}
    except Exception as e:
        print(f"Erro ao incrementar score: {e}")
        return {"status": "error", "message": str(e)}
