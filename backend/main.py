from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
from unidecode import unidecode

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

def normalize_text(text):
    return unidecode(text.lower())

@app.get("/suggestions")
def get_suggestions(term: str):
    print("\n--- INICIANDO BUSCA DETALHADA ---")
    
    if not term:
        print("-> Etapa 1: Termo de busca está vazio. Retornando [].")
        return []
    
    print(f"-> Etapa 1: Recebido termo de busca: '{term}'")

    try:
        normalized_term = normalize_text(term)
        print(f"-> Etapa 2: Termo normalizado para: '{normalized_term}'")

        redis_key = f"idx:{normalized_term}"
        print(f"-> Etapa 3: A chave a ser buscada no Redis é: '{redis_key}'")

        key_exists = r.exists(redis_key)
        if not key_exists:
            print(f"-> ALERTA: A chave '{redis_key}' NÃO EXISTE no Redis. O seed.py pode não ter criado este índice.")
        else:
            print(f"-> SUCESSO: A chave '{redis_key}' foi encontrada no Redis.")

        results = r.zrange(redis_key, 0, 19)
        print(f"-> Etapa 5: O comando zrange retornou uma lista com {len(results)} itens.")
        if results:
            print(f"   -> Conteúdo do resultado: {results}")

        response_data = [{"text": suggestion} for suggestion in results]
        print(f"-> Etapa 6: Resposta final formatada com {len(response_data)} itens.")
        print("--- FIM DA BUSCA ---")
        return response_data

    except Exception as e:
        print(f"!!! OCORREU UM ERRO INESPERADO: {e}")
        print("--- FIM DA BUSCA COM ERRO ---")
        return []
