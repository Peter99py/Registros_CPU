from sqlalchemy import create_engine
import pandas as pd

# Dados de conexão
usuario = "postgres"
senha = "postgres"
host = "localhost"  
porta = "5432"
banco = "pessoal"
schema = "coretemp"

# engine de conexão
engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}")

data_path = ("C:/Users/pedro/OneDrive/Área de Trabalho/Registros CPU/data_processed/CT-Log 2025-06-28 00-48-52.csv")
dados = pd.read_csv(data_path) #type: ignore
dados.columns = dados.columns.str.lower()


# Nome da tabela no banco
nome_tabela = "raw_data"

# Subindo o DataFrame para o PostgreSQL
dados.to_sql(nome_tabela, engine, schema=schema, if_exists='append', index=False)