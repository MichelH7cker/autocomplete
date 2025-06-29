import redis
import json
import os
import time
from unidecode import unidecode

time.sleep(3) 

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

SUGGESTIONS_KEY = "suggestions_v1"

def normalize_text(text):
    return unidecode(text.lower())

def populate_db():
    print("--- INICIANDO PROCESSO DE SEEDING (MODO INVESTIGAÇÃO) ---")
    
    # FORÇA a limpeza do banco de dados para garantir um estado 100% limpo
    print("-> Etapa 1: Limpando o banco de dados Redis (FLUSHDB)...")
    r.flushdb()
    print("-> Etapa 1: Limpeza concluída.")

    try:
        print("-> Etapa 2: Lendo o arquivo suggestions.json...")
        file_path = '/app/data/suggestions.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)
        print(f"-> Etapa 2: {len(suggestions)} sugestões carregadas do arquivo.")

        print("-> Etapa 3: Preparando para criar índices...")
        pipe = r.pipeline()
        created_prefixes = set()

        for suggestion in suggestions:
            normalized = normalize_text(suggestion)
            for l in range(1, len(normalized) + 1):
                prefix = normalized[:l]
                # Adiciona o prefixo a um set para sabermos quais chaves deveriam ser criadas
                created_prefixes.add(f"idx:{prefix}")
                pipe.zadd(f"idx:{prefix}", {suggestion: 0})
        
        print(f"-> Etapa 3: {len(created_prefixes)} chaves de índice únicas foram preparadas.")
        
        print("-> Etapa 4: Executando o pipeline no Redis...")
        pipe.execute()
        print("-> Etapa 4: Pipeline executado com sucesso.")

        # Etapa 5: VERIFICAÇÃO FINAL
        print("-> Etapa 5: Verificando as chaves que REALMENTE foram criadas...")
        keys_in_redis = r.keys('idx:*')
        print(f"-> Etapa 5: O Redis reporta que existem {len(keys_in_redis)} chaves com o prefixo 'idx:'.")
        if keys_in_redis:
            print(f"   -> Amostra de chaves no Redis: {keys_in_redis[:5]}")
        else:
            print("   -> ALERTA MÁXIMO: Nenhuma chave de índice foi criada, mesmo após o pipeline executar.")

    except Exception as e:
        print(f"--- ERRO CRÍTICO NO PROCESSO DE SEEDING: {e} ---")

    print("--- FIM DO PROCESSO DE SEEDING ---")


if __name__ == "__main__":
    populate_db()

