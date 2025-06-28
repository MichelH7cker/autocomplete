import redis
import json
import os
import time

time.sleep(3) 

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

SUGGESTIONS_KEY = "suggestions_v1"

def populate_db():
    if r.exists(SUGGESTIONS_KEY):
        print("Redis: Banco de dados já populado.")
        return

    print("Redis: Populando banco de dados com sugestões...")
    try:
        with open('./data/suggestions.json', 'r', encoding='utf-8') as f:
            suggestions = json.load(f)

        pipe = r.pipeline()
        for suggestion in suggestions:
            pipe.zadd(SUGGESTIONS_KEY, {suggestion: 0})
        pipe.execute()
        print(f"Redis: {len(suggestions)} sugestões adicionadas com sucesso!")
    except Exception as e:
        print(f"Redis: Erro ao popular o banco de dados - {e}")

if __name__ == "__main__":
    populate_db()
