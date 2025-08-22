import pyodbc
import pandas as pd


conn = pyodbc.connect("DSN=PostgreSQL35W")

#Média corespeed
def corespeed_vs_temp():
    try:        
        query = """SELECT
                EXTRACT(HOUR FROM time) as time,
                MIN(core_speed_0)::INTEGER as min_corespeed,
                AVG(core_speed_0)::INTEGER as avg_corespeed,
                MAX(core_speed_0)::INTEGER as max_corespeed
                FROM coretemp.raw_data
                GROUP BY
                1
                """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None