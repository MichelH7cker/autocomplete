import redis
import json
import os
import time

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

SUGGESTIONS_KEY = "suggestions:ranking"

def populate_db():
    if r.exists(SUGGESTIONS_KEY):
        print("Redis (Ranking): Banco de dados já populado.")
        return

    print("Redis (Ranking): Populando banco de dados para ranking...")
    try:
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        
        items_to_add = {suggestion: 0 for suggestion in suggestions}
        
        if items_to_add:
            r.zadd(SUGGESTIONS_KEY, items_to_add)
        
        print(f"Redis (Ranking): {len(suggestions)} sugestões adicionadas com score 0!")

    except Exception as e:
        print(f"Redis (Ranking): Erro ao popular o banco de dados - {e}")

if __name__ == "__main__":
    populate_db()
