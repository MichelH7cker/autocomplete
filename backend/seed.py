import redis
import json
import os

def populate_db():
    print("--- Verificando o banco de dados Redis ---")
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        print("!!! ERRO: Variável de ambiente REDIS_URL não está definida. Pulando o seeding.")
        return

    try:
        r = redis.from_url(redis_url, decode_responses=True)
        r.ping() 
        print("Redis: Conexão bem-sucedida.")
    except Exception as e:
        print(f"!!! ERRO: Falha ao conectar com o Redis: {e}")
        return

    SUGGESTIONS_KEY = "suggestions:ranking"

    try:
        if r.zcard(SUGGESTIONS_KEY) > 0:
            print(f"Redis: Banco de dados já populado com {r.zcard(SUGGESTIONS_KEY)} itens.")
            return

        print("Redis: Populando banco de dados com dados iniciais...")
        
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        
        if not suggestions:
            print("Arquivo de sugestões está vazio.")
            return

        items_to_add = {suggestion: 0 for suggestion in suggestions}
        
        if items_to_add:
            r.zadd(SUGGESTIONS_KEY, items_to_add)
        
        print(f"Redis: {len(suggestions)} sugestões adicionadas com sucesso!")

    except Exception as e:
        print(f"!!! ERRO inesperado ao popular o banco de dados: {e}")
