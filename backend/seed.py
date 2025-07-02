import redis
import json
import os
import time

redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("A variável de ambiente REDIS_URL não foi definida.")

r = None
retries = 5
while retries > 0:
    try:
        print(f"Redis: Conectando à instância em {redis_url}")
        r = redis.from_url(redis_url, decode_responses=True)
        r.ping() 
        print("Redis: Conexão bem-sucedida!")
        break
    except redis.exceptions.ConnectionError as e:
        retries -= 1
        print(f"Redis: Falha na conexão, tentando novamente em 5 segundos... ({retries} tentativas restantes)")
        time.sleep(5)

if r is None:
    print("Redis: Não foi possível estabelecer conexão após várias tentativas. Abortando script.")
    exit(1)

SUGGESTIONS_KEY = "suggestions:ranking"

def populate_db():
    try:
        if r.zcard(SUGGESTIONS_KEY) > 0:
            print(f"Redis (Ranking): Banco de dados já populado com {r.zcard(SUGGESTIONS_KEY)} itens. Nenhuma ação necessária.")
            return

        print("Redis (Ranking): Banco de dados vazio. Populando com dados iniciais...")
        
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        
        if not suggestions:
            print("Arquivo de sugestões está vazio. Nada a fazer.")
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
        print(f"Redis (Ranking): Erro inesperado ao popular o banco de dados - {e}")

if __name__ == "__main__":
    populate_db()
