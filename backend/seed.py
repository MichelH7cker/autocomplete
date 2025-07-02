import redis
import json
import os
import time

def populate_db():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise ValueError("A variável de ambiente REDIS_URL não foi definida.")

    r = None
    try:
        r = redis.from_url(redis_url, decode_responses=True)
        r.ping() 
    except redis.exceptions.ConnectionError as e:
        print(f"Redis: Falha na conexão no seed.py - {e}")
        return

    SUGGESTIONS_KEY = "suggestions:ranking"

    try:
        if r.zcard(SUGGESTIONS_KEY) > 0:
            print(f"Redis (Ranking): Banco de dados já populado com {r.zcard(SUGGESTIONS_KEY)} itens.")
            return

        print("Redis (Ranking): Populando banco de dados...")
        
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        
        if not suggestions:
            print("Arquivo de sugestões está vazio.")
            return

        items_to_add = {suggestion: 0 for suggestion in suggestions}
        
        r.zadd(SUGGESTIONS_KEY, items_to_add)
        
        print(f"Redis (Ranking): {len(suggestions)} sugestões adicionadas com sucesso!")

    except Exception as e:
        print(f"Redis (Ranking): Erro inesperado ao popular o banco de dados - {e}")
