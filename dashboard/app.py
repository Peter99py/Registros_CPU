# App Streamlit: Monitoramento do Processador
# Construção do Dashboard com filtros (ano/mês/dia), séries temporais e relações

import streamlit as st
from src.charts.charts import grafico_linhas, grafico_colunas
from src.queries.queries import time_vs_temp, temp_vs_speed, time_vs_power, temp_vs_power, faixas_temp, anos_disponiveis, meses_disponiveis, dias_disponiveis, resumo_temp

# Configuração da página (título e layout)
st.set_page_config(page_title="Meu Processador", layout="wide")

# Título da aplicação (HTML simples)
st.markdown("<h1 style='text-align: center; color: black;'>Meu Processador</h1>", unsafe_allow_html=True)

# Barra lateral: filtros de data e granularidade
with st.sidebar:
    st.header("Filtros de Data")

    # Opções de ano disponíveis para filtragem
    years = anos_disponiveis()
    # Seletor de ano (habilita filtros de mês e dia)
    sel_year = st.selectbox(
        "Ano",
        options=["Todos"] + years,
        index=0,
        help="Selecione um ano para habilitar o filtro de mês e dia."
    )

    # Converte "Todos" -> None
    # Normaliza "Todos" -> None para consultas
    year_val = None if sel_year == "Todos" else int(sel_year)

    # Opções de mês condicionadas ao ano
    months = meses_disponiveis(year=year_val)
    # Seletor de mês
    sel_month = st.selectbox(
        "Mês",
        options=["Todos"] + months if months else ["Todos"],
        index=0,
        help="Selecione um mês (opcional)."
    )
    # Normaliza mês selecionado
    month_val = None if sel_month == "Todos" else int(sel_month)

    # Opções de dia condicionadas a ano/mês
    days = dias_disponiveis(year=year_val, month=month_val)
    # Seletor de dia
    sel_day = st.selectbox(
        "Dia",
        options=["Todos"] + days if days else ["Todos"],
        index=0,
        help="Selecione um dia (opcional, depende do mês)."
    )
    # Normaliza dia selecionado
    day_val = None if sel_day == "Todos" else int(sel_day)


# Carregando dataframes
df_faixas_temp = faixas_temp(year=year_val, month=month_val, day=day_val)
df_temp_vs_speed = temp_vs_speed(year=year_val, month=month_val, day=day_val)
df_time_vs_temp = time_vs_temp(year=year_val, month=month_val, day=day_val)
df_time_vs_power = time_vs_power(year=year_val, month=month_val, day=day_val)
df_temp_vs_power = temp_vs_power(year=year_val, month=month_val, day=day_val)
df_resumo_temp = resumo_temp(year=year_val, month=month_val, day=day_val)

# Layout principal: abas (Resumo, Séries por Hora, Relações)
aba_resumo, aba_series, aba_relacoes = st.tabs(["Resumo", "Séries por Hora", "Relações"])

# Aba "Resumo": visão geral e distribuição de faixas de temperatura
with aba_resumo:

    # Duas colunas: KPIs (esquerda) e gráfico (direita)
    col1, col2 = st.columns([1, 2])  # esquerda menor, direita maior

    # Coluna 1: cartões de métricas
    with col1: 
        st.subheader("Visão geral de temperaturas")
        # Estatísticas básicas de temperatura
        max_val = df_resumo_temp["core temp"].max()
        min_val = df_resumo_temp["core temp"].min()
        media_val = df_resumo_temp["core temp"].mean()
        mediana_val = df_resumo_temp["core temp"].median()

        st.metric(label="🌡️ Máxima", value=f"{max_val:.2f} ºC") # Aqui descobri que dava pra usar emoticon dentro de código, LOL
        st.metric(label="❄️ Mínima", value=f"{min_val:.2f} ºC")
        st.metric(label="📊 Média", value=f"{media_val:.2f} ºC")
        st.metric(label="⚖️ Mediana", value=f"{mediana_val:.2f} ºC")

    # Coluna 2: gráfico de linhas com nível de detalhe (Dia/Mês/Ano)
    with col2:
        st.subheader("Evolução da Temperatura ao Longo do Tempo")
        st.markdown("""<style>div[data-baseweb="select"] {max-width: 150px;}</style>""", unsafe_allow_html=True)

        # Controle de granularidade do gráfico
        nivel = st.selectbox("Nível de detalhe", ["Dia", "Mês", "Ano"])

        # Agrega máximo por dia e tipo
        if nivel == "Dia":
            df_plot = df_resumo_temp.groupby(["dia", "type"], as_index=False)["core temp"].max()
            x_col = "dia"
        # Agrega máximo por mês e tipo
        elif nivel == "Mês":
            df_plot = df_resumo_temp.groupby(["mes", "type"], as_index=False)["core temp"].max()
            x_col = "mes"
        # Caso padrão: agrega máximo por ano e tipo
        else: 
            df_plot = df_resumo_temp.groupby(["ano", "type"], as_index=False)["core temp"].max()
            x_col = "ano"

        # Monta objeto de gráfico e renderiza com Altair
        grafico = grafico_linhas(
            df_plot,
            coluna_x=x_col,
            coluna_y="core temp",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) ao Longo do Tempo"
        )
        st.altair_chart(grafico, use_container_width=True)

# Separador visual
    st.markdown("---")
    # Barras: média diária de minutos por faixa de temperatura
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

# Aba "Séries por Hora": padrões ao longo do dia
with aba_series:
    st.subheader("Padrões ao longo do dia")
    # Duas colunas: Gráficos de linhas
    col1, col2 = st.columns(2, gap="medium")

    # Série temporal: temperatura ao longo do dia
    with col1:
        # Monta objeto de gráfico e renderiza com Altair
        grafico = grafico_linhas(
            df_time_vs_temp,
            coluna_x="time of day",
            coluna_y="core temp",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) ao Longo do Dia"
        )
        st.altair_chart(grafico, use_container_width=True)

    # Coluna 2: gráfico de linhas com nível de detalhe (Dia/Mês/Ano)
    # Série temporal: energia do CPU ao longo do dia
    with col2:
        # Monta objeto de gráfico e renderiza com Altair
        grafico = grafico_linhas(
            df_time_vs_power,
            coluna_x="time of day",
            coluna_y="cpu power",
            coluna_categoria="type",
            titulo="Energia do CPU ao Longo do Dia"
        )
        st.altair_chart(grafico, use_container_width=True)

    st.caption("Padrões da temperatura e consumo de energia durante o dia.")


# Aba "Relações": correlação visual entre variáveis
with aba_relacoes:
    st.subheader("Relações entre variáveis")
    # Duas colunas: Gráficos de linhas
    col1, col2 = st.columns(2, gap="medium")

    # Relação temperatura vs velocidade do núcleo
    with col1:
        # Monta objeto de gráfico e renderiza com Altair
        grafico = grafico_linhas(
            df_temp_vs_speed,
            coluna_x="core temp",
            coluna_y="core speed",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) vs Velocidade do Núcleo"
        )
        st.altair_chart(grafico, use_container_width=True)

    # Relação temperatura vs energia do CPU
    with col2:
        # Monta objeto de gráfico e renderiza com Altair
        grafico = grafico_linhas(
            df_temp_vs_power,
            coluna_x="core temp",
            coluna_y="cpu power",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo(ºC) vs Energia do CPU"
        )
        st.altair_chart(grafico, use_container_width=True)

    st.caption("Variações da velocidade e energia do CPU em relação à temperatura.")