import redis
import json
import os
import time

redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("A variável de ambiente REDIS_URL não foi definida.")
r = redis.from_url(redis_url, decode_responses=True)
r.ping() 

SUGGESTIONS_KEY = "suggestions:ranking"

def populate_db():
    if r.scard(SUGGESTIONS_KEY) > 1000:
        print(f"Redis (Ranking): Banco de dados já parece estar populado com {r.scard(SUGGESTIONS_KEY)} itens.")
        return

    print("Redis (Ranking): Limpando e populando o banco de dados...")
    r.flushdb()
    
    try:
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        
        if not suggestions:
            print("Arquivo de sugestões está vazio.")
            return

        batch_size = 500
        total_suggestions = len(suggestions)
        
        print(f"Iniciando população de {total_suggestions} sugestões em lotes de {batch_size}...")

        for i in range(0, total_suggestions, batch_size):
            batch = suggestions[i:i + batch_size]
            
            items_to_add = {suggestion: 0 for suggestion in batch}
            
            if items_to_add:
                r.zadd(SUGGESTIONS_KEY, items_to_add)
            
            print(f"Lote {i//batch_size + 1} de {total_suggestions//batch_size + 1} processado com sucesso.")
            time.sleep(0.1)
        
        print(f"Redis (Ranking): {total_suggestions} sugestões adicionadas com sucesso!")

    except Exception as e:
        print(f"Redis (Ranking): Erro ao popular o banco de dados - {e}")

if __name__ == "__main__":
    populate_db()
