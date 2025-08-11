import pandas as pd
import os
import shutil

# Definindo os caminhos das pastas
datapath = "data_raw"
outputpath = "data_processed"
loaded_raw_path = "data_loaded_raw"

# Define o mapeamento de renomeação de colunas
renomear_colunas = {
    "Time": "time",
    "Core 0 Temp. (°)": "core_temp_0",
    "Low temp. (°)": "low_temp_0",
    "High temp. (°)": "high_temp_0",
    "Core load (%)": "core_load_0",
    "Core speed (MHz)": "core_speed_0",
    "Core 1 Temp. (°)": "core_temp_1",
    "Low temp. (°).1": "low_temp_1",
    "High temp. (°).1": "high_temp_1",
    "Core load (%).1": "core_load_1",
    "Core speed (MHz).1": "core_speed_1",
    "Core 2 Temp. (°)": "core_temp_2",
    "Low temp. (°).2": "low_temp_2",
    "High temp. (°).2": "high_temp_2",
    "Core load (%).2": "core_load_2",
    "Core speed (MHz).2": "core_speed_2",
    "Core 3 Temp. (°)": "core_temp_3",
    "Low temp. (°).3": "low_temp_3",
    "High temp. (°).3": "high_temp_3",
    "Core load (%).3": "core_load_3",
    "Core speed (MHz).3": "core_speed_3",
    "Core 4 Temp. (°)": "core_temp_4",
    "Low temp. (°).4": "low_temp_4",
    "High temp. (°).4": "high_temp_4",
    "Core load (%).4": "core_load_4",
    "Core speed (MHz).4": "core_speed_4",
    "Core 5 Temp. (°)": "core_temp_5",
    "Low temp. (°).5": "low_temp_5",
    "High temp. (°).5": "high_temp_5",
    "Core load (%).5": "core_load_5",
    "Core speed (MHz).5": "core_speed_5",
    "CPU 0 Power": "cpu_power"
}

for filename in os.listdir(datapath): # Busca todos os arquivos na pasta data_raw
    if filename.endswith(".csv"):
        filepath = os.path.join(datapath, filename)
        print(f"Processando arquivo: {filename}")

        try:
            dados = pd.read_csv(filepath, encoding="latin1", skiprows=7) #type: ignore

            dados = dados.loc[:, ~dados.columns.str.startswith("Unnamed")]
            dados = dados.drop(columns=["Core 0", "Core 1", "Core 2", "Core 3", "Core 4", "Core 5"], errors='ignore')
            
            dados["Time"] = pd.to_datetime(dados["Time"], format="%H:%M:%S %m/%d/%y", errors="coerce")

            colunas_esperadas = [
                'Time',
                'Core 0 Temp. (°)', 'Low temp. (°)', 'High temp. (°)', 'Core load (%)', 'Core speed (MHz)',
                'Core 1 Temp. (°)', 'Low temp. (°).1', 'High temp. (°).1', 'Core load (%).1', 'Core speed (MHz).1',
                'Core 2 Temp. (°)', 'Low temp. (°).2', 'High temp. (°).2', 'Core load (%).2', 'Core speed (MHz).2',
                'Core 3 Temp. (°)', 'Low temp. (°).3', 'High temp. (°).3', 'Core load (%).3', 'Core speed (MHz).3',
                'Core 4 Temp. (°)', 'Low temp. (°).4', 'High temp. (°).4', 'Core load (%).4', 'Core speed (MHz).4',
                'Core 5 Temp. (°)','Low temp. (°).5','High temp. (°).5','Core load (%).5','Core speed (MHz).5',
                'CPU 0 Power'
            ]

            dados = dados[colunas_esperadas]

            dados.rename(columns=renomear_colunas, inplace=True)

            output_filepath = os.path.join(outputpath, filename)
            dados.to_csv(output_filepath, index=False)
            print(f"Arquivo processado salvo em: {output_filepath}")

            shutil.move(filepath, os.path.join(loaded_raw_path, filename))
            print(f"Arquivo original movido para: {os.path.join(loaded_raw_path, filename)}")

        except Exception as e:
            print(f"Erro ao processar o arquivo {filename}: {e}")

print("Processamento de todos os arquivos concluído.")
