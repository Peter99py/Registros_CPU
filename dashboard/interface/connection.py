import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_coretemp_data():
    connection = None
    cursor = None
    try:
        connection = pyodbc.connect(
            f"DRIVER={{PostgreSQL Unicode(x64)}};"
            f"SERVER={os.getenv('DB_HOST')};"
            f"PORT={os.getenv('DB_PORT')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')}"
        )
        cursor = connection.cursor()

        print("Conexão OK!")

        query = """
        SELECT
            CAST(cr.time AS DATE) AS data,
            CAST(cr.time AS TIME) AS horas,
            core_temp_0,
            core_temp_1,
            core_temp_2,
            core_temp_3,
            core_temp_4,
            core_temp_5,
            core_speed_0,
            core_speed_1,
            core_speed_2,
            core_speed_3,
            core_speed_4,
            core_speed_5
        FROM
            coretemp.raw_data AS cr
        """
        df = pd.read_sql(query, connection)
        print(df)
        return df
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        print(f"Erro de conexão: {sqlstate}")
        return None
    finally:
        if cursor:
            cursor.close()
            print("Cursor fechado.")
        if connection:
            connection.close()
            print("Conexão fechada.")