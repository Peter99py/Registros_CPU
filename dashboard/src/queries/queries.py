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
    
# média diária de minutos por faixa de temperatura do processador
def faixas_temp():
    engine = get_engine()

    query = """
            WITH minutos_por_dia AS (
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '<60' AS categoria
        FROM
            coretemp.raw_data
        WHERE
            core_temp_0 < 60
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=60 & <70' AS categoria
        FROM
            coretemp.raw_data
        WHERE
            core_temp_0 >= 60 AND core_temp_0 < 70
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=70 & <80' AS categoria
        FROM
            coretemp.raw_data
        WHERE
            core_temp_0 >= 70 AND core_temp_0 < 80
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=80 & <90' AS categoria
        FROM
            coretemp.raw_data
        WHERE
            core_temp_0 >= 80 AND core_temp_0 < 90
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=90' AS categoria
        FROM
            coretemp.raw_data
        WHERE
            core_temp_0 > 90
        GROUP BY
            DATE(time)
    )
    SELECT
        ROUND(AVG(minutos)) AS "media diaria",
        categoria,
		CASE 
		WHEN categoria = '<60' THEN 1
		WHEN categoria = '>=60 & <70' THEN 2
		WHEN categoria = '>=70 & <80' THEN 3
		WHEN categoria = '>=80 & <90' THEN 4
		WHEN categoria = '>=90' THEN 5
		END AS ordernar
    FROM
        minutos_por_dia
    GROUP BY
        categoria
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn) # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None