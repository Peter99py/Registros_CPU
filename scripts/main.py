# Objetivo: Orquestrar o fluxo ETL:
#   1) Garantir a existência das pastas de trabalho
#   2) Executar o pipeline de transformação
#   3) Carregar os dados no banco

import os 
import pipeline as pipeline
import load as load

print("---Iniciando aplicação ---")

def files():
    # Garante que as pastas usadas pelo processo existam
    files = ["data/loaded_processed", "data/loaded_raw", "data/processed", "data/raw"]
    for arquivos in files:
        if not os.path.exists(arquivos):  # verifica existência do diretório
            os.makedirs(arquivos)  # cria diretório ausente
            print(f'Pasta {arquivos} criada com sucesso!')
        else:
            print(f'Pasta {arquivos} OK!')
    main()  # chama o fluxo principal após preparar as pastas


def main():
    # Executa o pipeline e, na sequência, a carga para o banco com confirmações via Enter
    print('\n--- Executando pipeline ---')
    input("\nPressione Enter para iniciar o processo de ETL.")  # pausa antes do pipeline
    pipeline.pipeline()  # executa o pipeline de ETL

    input("\nPressione Enter para subir os arquivos para o banco de dados.")  # pausa antes da carga
    load.load_data_to_db()  # realiza a carga para o banco

    input("\nPressione Enter para sair...")  # pausa final antes de encerrar

if __name__ == "__main__":
    files()
