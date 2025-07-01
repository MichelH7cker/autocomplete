import requests
import json
import time

DICIO_URL = "https://www.ime.usp.br/~pf/dicios/br-utf8.txt"

OUTPUT_FILE_PATH = "suggestions.json"

def buscar_e_salvar_dicionario():
    print(f"Iniciando download de: {DICIO_URL}")
    
    try:
        response = requests.get(DICIO_URL, timeout=30)
        response.raise_for_status()
        
        print("Download concluído. Processando palavras...")
        texto_dicionario = response.content.decode('utf-8')
        
        palavras_brutas = texto_dicionario.splitlines()
        
        palavras_limpas = {
            palavra.strip() 
            for palavra in palavras_brutas 
            if len(palavra.strip()) >= 4
        }
        
        lista_final = sorted(list(palavras_limpas))
        
        print(f"Processamento finalizado. {len(lista_final)} palavras válidas encontradas.")
        
        print(f"Salvando a lista de palavras em '{OUTPUT_FILE_PATH}'...")
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista_final, f, ensure_ascii=False, indent=2)
            
        print("\nArquivo 'suggestions.json' atualizado com sucesso com o dicionário da USP!")

    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao baixar o dicionário: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    start_time = time.time()
    buscar_e_salvar_dicionario()
    end_time = time.time()
    print(f"Processo levou {end_time - start_time:.2f} segundos.")
