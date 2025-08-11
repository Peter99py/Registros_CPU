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

# Engine de conexão com o PostgreSQL usando psycopg2
engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}")

# Cria uma sessão para interagir com o banco de dados.
Session = sessionmaker(bind=engine)

data_processed_path = "data_processed"

data_loaded_processed_path = "data_loaded_processed"

# Garante que o diretório de destino para os arquivos carregados exista.
os.makedirs(data_loaded_processed_path, exist_ok=True)

def load_data_to_db():

    print("\n--- Iniciando o processo de carregamento de dados para o PostgreSQL... ---")

    # Lista todos os arquivos CSV no diretório de dados processados
    files_to_load = [f for f in os.listdir(data_processed_path) if f.endswith('.csv')]

    if not files_to_load:
        print("\nNenhum arquivo .csv encontrado na pasta 'data_processed'.")
        input("\nPressione Enter para sair...")
        return

    print(f"Encontrados {len(files_to_load)} arquivos para carregar.")

    with Session() as session:
        # Lista que armazena os caminhos dos arquivos que foram *adicionados à transação*
        successfully_processed_file_paths = []
        try:
            for file_name in files_to_load:
                file_path = os.path.join(data_processed_path, file_name)
                destination_file_path = os.path.join(data_loaded_processed_path, file_name)

                print(f"\n--- Processando e Carregando: {file_name} ---")

                try:
                    dados = pd.read_csv(file_path) # type: ignore

                    dados.to_sql(nome_tabela, session.connection(), schema=schema, if_exists='append', index=False)
                    print(f"Dados do arquivo '{file_name}' adicionados à transação do banco de dados.")

                    successfully_processed_file_paths.append((file_path, destination_file_path))

                except Exception as e:
                    # Se um erro ocorrer ao processar ou adicionar UM arquivo à transação, a exceção é capturada aqui, e então lançada para o bloco `except` externo.
                    print(f"!!! ERRO ao processar o arquivo {file_name}: {e}")
                    print("!!! Este arquivo causou uma falha. Toda a transação será revertida.")
                    raise

            # Caso sucesso, a transação é comitada.
            session.commit()
            print("\n--- Todos os dados foram carregados com sucesso no banco de dados! ---")

            # Move os arquivos APENAS SE A TRANSAÇÃO GERAL FOR BEM-SUCEDIDA.
            for original_path, dest_path in successfully_processed_file_paths:
                shutil.move(original_path, dest_path)
                print(f"Arquivo original '{os.path.basename(original_path)}' movido para: {dest_path}")

        except Exception as e:
            # Em caso de qualquer erro (capturado pelo `raise` interno ou qualquer outro erro), o upload é desfeito (rollback), garantindo que nada seja salvo no banco de dados.
            session.rollback()
            print(f"\n!!! ERRO FATAL no processo de carregamento: {e}")
            print("!!! O processo foi abortado. Todas as alterações no banco de dados foram revertidas.")
            print("!!! Nenhum arquivo foi movido para a pasta 'data_loaded_processed'.")

    print("\n--- Processo de carregamento finalizado! ---")
    input("\nPressione Enter para sair...")

# Executa a função principal quando o script é chamado
if __name__ == "__main__":
    load_data_to_db()