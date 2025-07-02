import redis, json, os, time

redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("A variável de ambiente REDIS_URL não foi definida.")
r = redis.from_url(redis_url, decode_responses=True)
r.ping()

SUGGESTIONS_KEY = "suggestions:ranking"

def populate_db():
    if r.exists(SUGGESTIONS_KEY):
        print("Redis (Ranking): Banco de dados já populado.")
        return
    print("Redis (Ranking): Populando banco de dados...")
    try:
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        items_to_add = {suggestion: 0 for suggestion in suggestions}
        if items_to_add:
            r.zadd(SUGGESTIONS_KEY, items_to_add)
        print(f"Redis (Ranking): {len(suggestions)} sugestões adicionadas!")
    except Exception as e:
        print(f"Redis (Ranking): Erro ao popular - {e}")

if __name__ == "__main__":
    populate_db()
