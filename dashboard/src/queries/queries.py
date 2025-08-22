import pyodbc
import pandas as pd


conn = pyodbc.connect("DSN=PostgreSQL35W")

#Média corespeed
def time_vs_temp():
    try:
        query = """SELECT
                EXTRACT(HOUR FROM time) as "time of day",
                MIN(core_temp_0)::INTEGER as "core temp",
                'MIN' AS "type"
                FROM coretemp.raw_data
                GROUP BY
                1

                UNION ALL

                SELECT
                EXTRACT(HOUR FROM time) as "time of day",
                AVG(core_temp_0)::INTEGER as "core temp",
                'AVG' AS "type"
                FROM coretemp.raw_data
                GROUP BY
                1

                UNION ALL
                SELECT
                EXTRACT(HOUR FROM time) as "time of day",
                MAX(core_temp_0)::INTEGER as "core temp",
                'MAX' AS "type"
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