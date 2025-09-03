import pandas as pd
import os
import shutil

raw_data_path = "data/raw"

loaded_data_path = "data/loaded_raw"

processed_data_path = "data/processed"

os.makedirs(loaded_data_path, exist_ok=True)
os.makedirs(processed_data_path, exist_ok=True)

def process_file(file_path, output_path): # type: ignore
    print(f"Lendo o arquivo: {os.path.basename(file_path)}") # type: ignore
    
    dados = pd.read_csv(file_path, encoding="latin1", skiprows=7) # type: ignore
    
    linhas_iniciais = len(dados)
    print(f"\nQtd. linhas antes do processamento: {linhas_iniciais}")

    # Remove colunas que começam com "Unnamed"
    dados = dados.loc[:, ~dados.columns.str.startswith("Unnamed")]

    # Remove colunas específicas de "Core"
    cols_to_drop = ["Core 0", "Core 1", "Core 2", "Core 3", "Core 4", "Core 5"]

    dados = dados.drop(columns=cols_to_drop)
    
    # Remove colunas que são completamente vazias
    dados = dados.dropna(axis=1, how='all') # type: ignore

    # Converte a coluna 'Time' para o formato datetime
    dados["Time"] = pd.to_datetime(dados["Time"], format="%H:%M:%S %m/%d/%y", errors="coerce")
    
    # Remove linhas que são completamente vazias
    dados = dados.dropna(axis=0, how='all') # type: ignore

    # Remove qualquer linha que tenha pelo menos um valor vazio
    dados = dados.dropna(axis=0, how='any') # type: ignore

    try:
        dados = dados[['Time',
                       'Core 0 Temp. (°)', 'Low temp. (°)', 'High temp. (°)', 'Core load (%)', 'Core speed (MHz)',
                       'Core 1 Temp. (°)', 'Low temp. (°).1', 'High temp. (°).1', 'Core load (%).1', 'Core speed (MHz).1',
                       'Core 2 Temp. (°)', 'Low temp. (°).2', 'High temp. (°).2', 'Core load (%).2', 'Core speed (MHz).2',
                       'Core 3 Temp. (°)', 'Low temp. (°).3', 'High temp. (°).3', 'Core load (%).3', 'Core speed (MHz).3',
                       'Core 4 Temp. (°)', 'Low temp. (°).4', 'High temp. (°).4', 'Core load (%).4', 'Core speed (MHz).4',
                       'Core 5 Temp. (°)', 'Low temp. (°).5', 'High temp. (°).5', 'Core load (%).5', 'Core speed (MHz).5',
                       'CPU 0 Power']]
    except KeyError as e:
        print(f"  Aviso: Coluna não encontrada durante a reordenação: {e}. O arquivo pode ter um formato diferente.")
        pass

    # Renomeando colunas
    renomear_colunas = {
        "Time": "time",
        "Core 0 Temp. (°)": "core_temp_0", "Low temp. (°)": "low_temp_0", "High temp. (°)": "high_temp_0", "Core load (%)": "core_load_0", "Core speed (MHz)": "core_speed_0",
        "Core 1 Temp. (°)": "core_temp_1", "Low temp. (°).1": "low_temp_1", "High temp. (°).1": "high_temp_1", "Core load (%).1": "core_load_1", "Core speed (MHz).1": "core_speed_1",
        "Core 2 Temp. (°)": "core_temp_2", "Low temp. (°).2": "low_temp_2", "High temp. (°).2": "high_temp_2", "Core load (%).2": "core_load_2", "Core speed (MHz).2": "core_speed_2",
        "Core 3 Temp. (°)": "core_temp_3", "Low temp. (°).3": "low_temp_3", "High temp. (°).3": "high_temp_3", "Core load (%).3": "core_load_3", "Core speed (MHz).3": "core_speed_3",
        "Core 4 Temp. (°)": "core_temp_4", "Low temp. (°).4": "low_temp_4", "High temp. (°).4": "high_temp_4", "Core load (%).4": "core_load_4", "Core speed (MHz).4": "core_speed_4",
        "Core 5 Temp. (°)": "core_temp_5", "Low temp. (°).5": "low_temp_5", "High temp. (°).5": "high_temp_5", "Core load (%).5": "core_load_5", "Core speed (MHz).5": "core_speed_5",
        "CPU 0 Power": "cpu_power"
    }
    
    dados.rename(columns=renomear_colunas, inplace=True)

    linhas_finais = len(dados)
    print(f"\nLinhas após o processamento: {linhas_finais} (removidas {linhas_iniciais - linhas_finais} linhas)")

    dados.to_csv(output_path, index=False)  # type: ignore
    print(f"\nArquivo processado e salvo em: {output_path}")

def pipeline():
    print("\n--- Iniciando o processo de ETL para os arquivos CSV ---")
    
    files_to_process = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
    
    if not files_to_process:
        print("\nNenhum arquivo .csv encontrado na pasta 'data/raw'.")
        return

    print(f"Encontrados {len(files_to_process)} arquivos para processar.")
    
    for file_name in files_to_process:
        source_file_path = os.path.join(raw_data_path, file_name)
        destination_file_path = os.path.join(loaded_data_path, file_name)
        output_file_path = os.path.join(processed_data_path, file_name)
        
        print(f"\n--- Processando: {file_name} ---")
        
        try:
            process_file(source_file_path, output_file_path)
            
            shutil.move(source_file_path, destination_file_path)
            print(f"Arquivo original movido para: {destination_file_path}")
            
        except Exception as e:
            # Em caso de erro, exibe a mensagem e continua para o próximo arquivo
            print(f"!!! ERRO ao processar o arquivo {file_name}: {e}")
            print("!!! O arquivo não será movido.")
            return

    print("\n--- Processo finalizado! ---")