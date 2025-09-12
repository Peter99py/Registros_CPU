import streamlit as st
from src.charts.charts import grafico_linhas, grafico_colunas  # type: ignore
from src.queries.queries import time_vs_temp, temp_vs_speed, time_vs_power, temp_vs_power, faixas_temp, anos_disponiveis, meses_disponiveis, dias_disponiveis, resumo_temp  # type: ignore

st.set_page_config(page_title="Meu Processador", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Meu Processador</h1>", unsafe_allow_html=True)

# Filtros
with st.sidebar:
    st.header("Filtros de Data")

    years = anos_disponiveis()
    sel_year = st.selectbox(
        "Ano",
        options=["Todos"] + years,
        index=0,
        help="Selecione um ano para habilitar o filtro de mês e dia."
    )

    # Converte "Todos" -> None
    year_val = None if sel_year == "Todos" else int(sel_year)

    months = meses_disponiveis(year=year_val)
    sel_month = st.selectbox(
        "Mês",
        options=["Todos"] + months if months else ["Todos"],
        index=0,
        help="Selecione um mês (opcional)."
    )
    month_val = None if sel_month == "Todos" else int(sel_month)

    days = dias_disponiveis(year=year_val, month=month_val)
    sel_day = st.selectbox(
        "Dia",
        options=["Todos"] + days if days else ["Todos"],
        index=0,
        help="Selecione um dia (opcional, depende do mês)."
    )
    day_val = None if sel_day == "Todos" else int(sel_day)

# carregando dataframes
df_faixas_temp = faixas_temp(year=year_val, month=month_val, day=day_val)
df_temp_vs_speed = temp_vs_speed(year=year_val, month=month_val, day=day_val)
df_time_vs_temp = time_vs_temp(year=year_val, month=month_val, day=day_val)
df_time_vs_power = time_vs_power(year=year_val, month=month_val, day=day_val)
df_temp_vs_power = temp_vs_power(year=year_val, month=month_val, day=day_val)
df_resumo_temp = resumo_temp(year=year_val, month=month_val, day=day_val)

aba_resumo, aba_series, aba_relacoes = st.tabs(["Resumo", "Séries por Hora", "Relações"])

with aba_resumo:

    col1, col2 = st.columns([1, 2])  # esquerda menor, direita maior

    with col1: # Coluna 1: Cartões de métricas
        st.subheader("Visão geral de temperaturas")
        max_val = df_resumo_temp["core temp"].max()
        min_val = df_resumo_temp["core temp"].min()
        media_val = df_resumo_temp["core temp"].mean()
        mediana_val = df_resumo_temp["core temp"].median()

        st.metric(label="🌡️ Máxima", value=f"{max_val:.2f} ºC")
        st.metric(label="❄️ Mínima", value=f"{min_val:.2f} ºC")
        st.metric(label="📊 Média", value=f"{media_val:.2f} ºC")
        st.metric(label="⚖️ Mediana", value=f"{mediana_val:.2f} ºC")

    with col2: # Coluna 2: Gráfico de linhas com "drill" simulado
        st.subheader("Evolução da Temperatura ao Longo do Tempo")
        st.markdown("""<style>div[data-baseweb="select"] {max-width: 150px;}</style>""", unsafe_allow_html=True)

        nivel = st.selectbox("Nível de detalhe", ["Dia", "Mês", "Ano"])

        if nivel == "Dia":
            df_plot = df_resumo_temp.groupby(["dia", "type"], as_index=False)["core temp"].mean()
            x_col = "dia"
        elif nivel == "Mês":
            df_plot = df_resumo_temp.groupby(["mes", "type"], as_index=False)["core temp"].mean()
            x_col = "mes"
        else: 
            df_plot = df_resumo_temp.groupby(["ano", "type"], as_index=False)["core temp"].mean()
            x_col = "ano"

        grafico = grafico_linhas(
            df_plot,
            coluna_x=x_col,
            coluna_y="core temp",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) ao Longo do Tempo"
        )
        st.altair_chart(grafico, use_container_width=True)

    # ===== BLOCO 2: SEGUNDA LINHA =====
    st.markdown("---")
    grafico_col = grafico_colunas(
        df_faixas_temp,
        coluna_x="categoria",
        coluna_y="media diaria",
        titulo="Média Diária de Minutos por Faixa de Temperatura(ºC)",
        mostrar_rotulos=True,
        posicao_rotulo="fora",
        cor_rotulo="black"
    )
    st.altair_chart(grafico_col, use_container_width=True)

    st.caption("Quanto tempo, em média por dia, o processador ficou em cada faixa de temperatura.")

with aba_series:
    st.subheader("Padrões ao longo do dia")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        grafico = grafico_linhas(
            df_time_vs_temp,
            coluna_x="time of day",
            coluna_y="core temp",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) ao Longo do Dia"
        )
        st.altair_chart(grafico, use_container_width=True)

    with col2:
        grafico = grafico_linhas(
            df_time_vs_power,
            coluna_x="time of day",
            coluna_y="cpu power",
            coluna_categoria="type",
            titulo="Energia do CPU ao Longo do Dia"
        )
        st.altair_chart(grafico, use_container_width=True)

    st.caption("Padrões da temperatura e consumo de energia durante o dia.")

with aba_relacoes:
    st.subheader("Relações entre variáveis")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        grafico = grafico_linhas(
            df_temp_vs_speed,
            coluna_x="core temp",
            coluna_y="core speed",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) vs Velocidade do Núcleo"
        )
        st.altair_chart(grafico, use_container_width=True)

    with col2:
        grafico = grafico_linhas(
            df_temp_vs_power,
            coluna_x="core temp",
            coluna_y="cpu power",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) vs Energia do CPU"
        )
        st.altair_chart(grafico, use_container_width=True)

    st.caption("Variações da velocidade e energia do CPU em relação à temperatura.")