import requests
import json

IBGE_API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

OUTPUT_FILE_PATH = "suggestions.json"

def buscar_e_salvar_cidades():
    print("Buscando lista de municípios na API do IBGE...")

    try:
        response = requests.get(IBGE_API_URL)
        response.raise_for_status()

        municipios_data = response.json()
        print(f"Sucesso! {len(municipios_data)} municípios encontrados.")

        lista_de_nomes = [municipio['nome'] for municipio in municipios_data]

        lista_de_nomes.sort()

        print(f"Salvando a lista de nomes em '{OUTPUT_FILE_PATH}'...")

        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista_de_nomes, f, ensure_ascii=False, indent=2)

        print("Arquivo 'suggestions.json' criado/atualizado com sucesso!")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar com a API do IBGE: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    buscar_e_salvar_cidades()
