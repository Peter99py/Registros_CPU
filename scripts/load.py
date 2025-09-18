# Objetivo: Carregar arquivos CSV da pasta data/processed para uma tabela no PostgreSQL, de forma transacional.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
import shutil


def get_engine():
    # Configuração de conexão com o banco (ajuste conforme o ambiente)
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = 5432
    db = "pessoal"

    # URL no formato SQLAlchemy para PostgreSQL com driver psycopg
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"

    return create_engine(url)

# Recursos globais de conexão e configuração
engine = get_engine()
schema = "coretemp"
nome_tabela = "raw_data"
Session = sessionmaker(bind=engine)

# Pastas de trabalho
data_processed_path = "data/processed"  # origem dos CSVs prontos para carga
data_loaded_processed_path = "data/loaded_processed"  # destino pós-sucesso

# Garante que a pasta de destino exista
os.makedirs(data_loaded_processed_path, exist_ok=True)


def load_data_to_db():
    # Carrega todos os CSVs de data/processed para o PostgreSQL de forma transacional. 
    # Em caso de sucesso, move cada arquivo para data/loaded_processed.
    # Em caso de erro em qualquer arquivo, faz rollback e não move nenhum arquivo.

    print("\n--- Iniciando o processo de carregamento de dados para o PostgreSQL... ---")

    # Coleta apenas arquivos .csv na pasta de processados
    files_to_load = [f for f in os.listdir(data_processed_path) if f.endswith('.csv')]

    # Se não houver arquivos, encerra.
    if not files_to_load:
        print("\nNenhum arquivo .csv encontrado na pasta 'data/processed'.")
        return

    print(f"\nEncontrados {len(files_to_load)} arquivos para carregar.")

    # Contador agregado de linhas carregadas.
    total_rows_processed = 0

    # Abre uma sessão transacional
    with Session() as session:
        successfully_processed_file_paths = []  # manterá (origem, destino) para mover após commit
        try:
            # Itera sobre cada arquivo a ser carregado
            for file_name in files_to_load:
                file_path = os.path.join(data_processed_path, file_name)  # caminho completo de origem
                destination_file_path = os.path.join(data_loaded_processed_path, file_name)  # destino
                print(f"\n--- Processando e Carregando: {file_name} ---")

                try:
                    # Lê o CSV; 'parse_dates' converte a coluna 'time' para datetime
                    dados = pd.read_csv(file_path, parse_dates=['time'])  # type: ignore

                    # Número de linhas do arquivo atual
                    num_rows = len(dados)

                    # Insere em modo append na tabela alvo dentro da transação da sessão
                    dados.to_sql(
                        nome_tabela,
                        session.connection(),
                        schema=schema,
                        if_exists='append',
                        index=False
                    )

                    print(f"\nDados do arquivo '{file_name}' adicionados à transação do banco de dados.")

                    # Registra o par (origem, destino) para mover apenas se tudo der certo
                    successfully_processed_file_paths.append((file_path, destination_file_path))  # type: ignore
                    # Atualiza contadores e logs
                    total_rows_processed += num_rows
                    print(f"Total de linhas processadas deste arquivo: {num_rows}")
                    print(f"Total de linhas processadas até agora: {total_rows_processed}")

                except Exception as e:
                    # Qualquer erro no processamento de UM arquivo invalida toda a carga
                    print(f"!!! ERRO ao processar o arquivo {file_name}: {e}")
                    print("!!! Este arquivo causou uma falha. Toda a transação será revertida.")
                    raise  # propaga para o bloco externo fazer rollback

            # Caso toda a iteração tenha sido bem-sucedida, confirma a transação
            session.commit()
            print("\n--- Todos os dados foram carregados com sucesso no banco de dados! ---")

            # Move os arquivos SOMENTE após o commit bem-sucedido
            for original_path, dest_path in successfully_processed_file_paths:  # type: ignore
                shutil.move(original_path, dest_path)  # type: ignore
                print(f"Arquivo original '{os.path.basename(original_path)}' movido para: {dest_path}")  # type: ignore

        except Exception as e:
            # Reverte qualquer alteração no banco caso algo tenha falhado
            session.rollback()
            print(f"\n!!! ERRO FATAL no processo de carregamento: {e}")
            print("!!! O processo foi abortado. Todas as alterações no banco de dados foram revertidas.")
            print("!!! Nenhum arquivo foi movido para a pasta 'data/loaded_processed'.")

    print("\n--- Processo de carregamento finalizado! ---")
