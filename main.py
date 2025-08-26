import os
import scripts.pipeline as pipeline
import scripts.load as load

print("---Iniciando aplicação ---")

def files():

    files = ["data_loaded_processed", "data_loaded_raw", "data_processed", "data_raw"]

    for arquivos in files:
        if not os.path.exists(arquivos):
            os.makedirs(arquivos)
            print(f'Pasta {arquivos} criada com sucesso!')
        else:
            print(f'Pasta {arquivos} OK!')
    
    main()

def main():

    print('\n--- Executando pipeline ---')
    input("\nPressione Enter para iniciar o processo de ETL.")
    pipeline.pipeline()

    input("\nPressione Enter para subir os arquivos para o banco de dados.")
    load.load_data_to_db()

    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    files()