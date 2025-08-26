from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
import shutil

# Conexão para o PostgreSQL
usuario = "postgres"
senha = "postgres"
host = "localhost"
porta = "5432"
banco = "pessoal"
schema = "coretemp"

nome_tabela = "raw_data"

engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}")

Session = sessionmaker(bind=engine)

data_processed_path = "data_processed"

data_loaded_processed_path = "data_loaded_processed"

os.makedirs(data_loaded_processed_path, exist_ok=True)

def load_data_to_db():

    print("\n--- Iniciando o processo de carregamento de dados para o PostgreSQL... ---")

    files_to_load = [f for f in os.listdir(data_processed_path) if f.endswith('.csv')]

    if not files_to_load:
        print("\nNenhum arquivo .csv encontrado na pasta 'data_processed'.")
        input("\nPressione Enter para sair...")
        return

    print(f"Encontrados {len(files_to_load)} arquivos para carregar.")
    total_rows_processed = 0

    with Session() as session:
        successfully_processed_file_paths = []
        try:
            for file_name in files_to_load:
                file_path = os.path.join(data_processed_path, file_name)
                destination_file_path = os.path.join(data_loaded_processed_path, file_name)

                print(f"\n--- Processando e Carregando: {file_name} ---")

                try:
                    dados = pd.read_csv(file_path) # type: ignore

                    num_rows = len(dados)

                    dados.to_sql(nome_tabela, session.connection(), schema=schema, if_exists='append', index=False)
                    print(f"Dados do arquivo '{file_name}' adicionados à transação do banco de dados.")

                    successfully_processed_file_paths.append((file_path, destination_file_path)) # type: ignore

                    total_rows_processed += num_rows
                    print(f"Total de linhas processadas deste arquivo: {num_rows}")
                    print(f"Total de linhas processadas até agora: {total_rows_processed}")

                except Exception as e:

                    print(f"!!! ERRO ao processar o arquivo {file_name}: {e}")
                    print("!!! Este arquivo causou uma falha. Toda a transação será revertida.")
                    raise

            # Caso sucesso, a transação é comitada.
            session.commit()
            print("\n--- Todos os dados foram carregados com sucesso no banco de dados! ---")

            # Move os arquivos APENAS SE A TRANSAÇÃO GERAL FOR BEM-SUCEDIDA.
            for original_path, dest_path in successfully_processed_file_paths: # type: ignore
                shutil.move(original_path, dest_path) # type: ignore
                print(f"Arquivo original '{os.path.basename(original_path)}' movido para: {dest_path}") # type: ignore

        except Exception as e:
           
            session.rollback()
            print(f"\n!!! ERRO FATAL no processo de carregamento: {e}")
            print("!!! O processo foi abortado. Todas as alterações no banco de dados foram revertidas.")
            print("!!! Nenhum arquivo foi movido para a pasta 'data_loaded_processed'.")

    print("\n--- Processo de carregamento finalizado! ---")