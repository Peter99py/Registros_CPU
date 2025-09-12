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

# Criação do filtro
def filtro_data(year=None, month=None, day=None):
    conds = []
    params = {}
    if year is not None:
        conds.append("EXTRACT(YEAR FROM time) = :year")
        params["year"] = int(year)
    if month is not None:
        conds.append("EXTRACT(MONTH FROM time) = :month")
        params["month"] = int(month)
    if day is not None:
        conds.append("EXTRACT(DAY FROM time) = :day")
        params["day"] = int(day)

    where_sql = f"WHERE {' AND '.join(conds)}" if conds else ""
    return where_sql, params

def anos_disponiveis():
    engine = get_engine()
    query = """
        SELECT DISTINCT EXTRACT(YEAR FROM time)::INT AS year
        FROM coretemp.raw_data
        ORDER BY year
    """
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn)  # type: ignore
    return df["year"].tolist()

def meses_disponiveis(year=None):
    engine = get_engine()
    base = "SELECT DISTINCT EXTRACT(MONTH FROM time)::INT AS month FROM coretemp.raw_data"
    where_sql, params = filtro_data(year=year)
    query = f"""
        {base}
        {where_sql}
        ORDER BY month
    """
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
    return df["month"].tolist()

def dias_disponiveis(year=None, month=None):
    engine = get_engine()
    base = "SELECT DISTINCT EXTRACT(DAY FROM time)::INT AS day FROM coretemp.raw_data"
    where_sql, params = filtro_data(year=year, month=month)
    query = f"""
        {base}
        {where_sql}
        ORDER BY day
    """
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
    return df["day"].tolist()

# descritivo da temperatura
def resumo_temp(year=None, month=None, day=None):
    engine = get_engine()
    where_sql, params = filtro_data(year, month, day)
    query = f"""
    WITH filtrado AS(
    SELECT DATE(time) AS time, core_temp_0
    FROM coretemp.raw_data
    {where_sql}
    )

    SELECT 
        EXTRACT(YEAR FROM time)::INTEGER AS "ano",
        EXTRACT(MONTH FROM time)::INTEGER AS "mes",
        EXTRACT(DAY FROM time)::INTEGER AS "dia",
        MIN(core_temp_0) AS "core temp",
        'MIN' AS "type"
    FROM filtrado
    GROUP BY 1,2,3

    UNION ALL

    SELECT 
        EXTRACT(YEAR FROM time)::INTEGER AS "ano",
        EXTRACT(MONTH FROM time)::INTEGER AS "mes",
        EXTRACT(DAY FROM time)::INTEGER AS "dia",
        AVG(core_temp_0)::INTEGER AS "core temp",
        'AVG' AS "type"
    FROM filtrado
    GROUP BY 1,2,3

    UNION ALL

    SELECT 
        EXTRACT(YEAR FROM time)::INTEGER AS "ano",
        EXTRACT(MONTH FROM time)::INTEGER AS "mes",
        EXTRACT(DAY FROM time)::INTEGER AS "dia",
        MAX(core_temp_0) AS "core temp",
        'MAX' AS "type"
    FROM filtrado
    GROUP BY 1,2,3
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta resumo_temp: {e}")
        return None

# temperatura vs core speed
def temp_vs_speed(year=None, month=None, day=None):
    engine = get_engine()
    where_sql, params = filtro_data(year, month, day)
    query = f"""
    WITH filtrado AS (
        SELECT time, core_temp_0, core_speed_0
        FROM coretemp.raw_data
        {where_sql}
    )
    SELECT
        core_temp_0 AS "core temp",
        MIN(core_speed_0)::INTEGER AS "core speed",
        'MIN' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        core_temp_0 as "core temp",
        AVG(core_speed_0)::INTEGER AS "core speed",
        'AVG' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        core_temp_0 AS "core temp",
        MAX(core_speed_0)::INTEGER AS "core speed",
        'MAX' AS "type"
    FROM filtrado
    GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta temp_vs_speed: {e}")
        return None

# tempo vs temperatura
def time_vs_temp(year=None, month=None, day=None):
    engine = get_engine()
    where_sql, params = filtro_data(year, month, day)
    query = f"""
    WITH filtrado AS (
        SELECT time, core_temp_0
        FROM coretemp.raw_data
        {where_sql}
    )
    SELECT
        EXTRACT(HOUR FROM time) AS "time of day",
        MIN(core_temp_0) AS "core temp",
        'MIN' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        EXTRACT(HOUR FROM time) AS "time of day",
        AVG(core_temp_0)::INTEGER AS "core temp",
        'AVG' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        EXTRACT(HOUR FROM time) AS "time of day",
        MAX(core_temp_0) AS "core temp",
        'MAX' AS "type"
    FROM filtrado
    GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta time_vs_temp: {e}")
        return None

# tempo vs energia
def time_vs_power(year=None, month=None, day=None):
    engine = get_engine()
    where_sql, params = filtro_data(year, month, day)
    query = f"""
    WITH filtrado AS (
        SELECT time, cpu_power
        FROM coretemp.raw_data
        {where_sql}
    )
    SELECT
        EXTRACT(HOUR FROM time) AS "time of day",
        MIN(cpu_power)::INTEGER AS "cpu power",
        'MIN' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        EXTRACT(HOUR FROM time) AS "time of day",
        AVG(cpu_power)::INTEGER AS "cpu power",
        'AVG' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        EXTRACT(HOUR FROM time) AS "time of day",
        MAX(cpu_power)::INTEGER AS "cpu power",
        'MAX' AS "type"
    FROM filtrado
    GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta time_vs_power: {e}")
        return None

# temperatura vs energia
def temp_vs_power(year=None, month=None, day=None):
    engine = get_engine()
    where_sql, params = filtro_data(year, month, day)
    query = f"""
    WITH filtrado AS (
        SELECT time, core_temp_0, cpu_power
        FROM coretemp.raw_data
        {where_sql}
    )
    SELECT
        core_temp_0 AS "core temp",
        MIN(cpu_power)::INTEGER AS "cpu power",
        'MIN' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        core_temp_0 AS "core temp",
        AVG(cpu_power)::INTEGER AS "cpu power",
        'AVG' AS "type"
    FROM filtrado
    GROUP BY 1
    UNION ALL
    SELECT
        core_temp_0 AS "core temp",
        MAX(cpu_power)::INTEGER AS "cpu power",
        'MAX' AS "type"
    FROM filtrado
    GROUP BY 1
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta temp_vs_power: {e}")
        return None

# média diária de minutos por faixa de temperatura do processador
def faixas_temp(year=None, month=None, day=None):
    engine = get_engine()
    where_sql, params = filtro_data(year, month, day)
    query = f"""
    WITH filtrado AS (
        SELECT time, core_temp_0
        FROM coretemp.raw_data
        {where_sql}
    ),
    minutos_por_dia AS (
        SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '<60' AS categoria
        FROM filtrado
        WHERE core_temp_0 < 60
        GROUP BY DATE(time)
        UNION ALL
        SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=60 & <70' AS categoria
        FROM filtrado
        WHERE core_temp_0 >= 60 AND core_temp_0 < 70
        GROUP BY DATE(time)
        UNION ALL
        SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=70 & <80' AS categoria
        FROM filtrado
        WHERE core_temp_0 >= 70 AND core_temp_0 < 80
        GROUP BY DATE(time)
        UNION ALL
        SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=80 & <90' AS categoria
        FROM filtrado
        WHERE core_temp_0 >= 80 AND core_temp_0 < 90
        GROUP BY DATE(time)
        UNION ALL
        SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=90' AS categoria
        FROM filtrado
        WHERE core_temp_0 > 90
        GROUP BY DATE(time)
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
    FROM minutos_por_dia
    GROUP BY categoria
    ORDER BY ordernar
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)  # type: ignore
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta faixas_temp: {e}")
        return None