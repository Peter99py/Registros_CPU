from sqlalchemy import create_engine, text
import pandas as pd


def get_engine():
    # ajuste com suas credenciais
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = 5432
    db = "pessoal"
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

# temperatura vs core speed
def temp_vs_speed():
    engine = get_engine()

    query = """
        SELECT
            core_temp_0 as "core temp",
            MIN(core_speed_0)::INTEGER as "core speed",
            'MIN' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            AVG(core_speed_0)::INTEGER as "core speed",
            'AVG' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            MAX(core_speed_0)::INTEGER as "core speed",
            'MAX' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn) # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None

# tempo vs temperatura
def time_vs_temp():
    engine = get_engine()

    query = """
        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MIN(core_temp_0)::INTEGER as "core temp",
            'MIN' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            AVG(core_temp_0)::INTEGER as "core temp",
            'AVG' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MAX(core_temp_0)::INTEGER as "core temp",
            'MAX' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn) # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None

# tempo vs energia
def time_vs_power():
    engine = get_engine()

    query = """
        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MIN(cpu_power)::INTEGER as "cpu power",
            'MIN' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            AVG(cpu_power)::INTEGER as "cpu power",
            'AVG' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MAX(cpu_power)::INTEGER as "cpu power",
            'MAX' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn) # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None

# temperatura vs energia
def temp_vs_power():
    engine = get_engine()

    query = """
        SELECT
            core_temp_0 as "core temp",
            MIN(cpu_power)::INTEGER as "cpu power",
            'MIN' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            AVG(cpu_power)::INTEGER as "cpu power",
            'AVG' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            MAX(cpu_power)::INTEGER as "cpu power",
            'MAX' AS "type"
        FROM coretemp.raw_data
        GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn) # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None