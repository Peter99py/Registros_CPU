import streamlit as st
from src.charts.line_charts import grafico_linhas_personalizado
from src.queries.queries import time_vs_temp

# Título da aplicação
st.title("Meu Processador")












df_core_temp_vs_time = time_vs_temp()
grafico = grafico_linhas_personalizado(df_core_temp_vs_time, "time of day", "core temp", 'type', titulo='Temperatura do Núcleo ao Longo do Dia')
st.altair_chart(grafico, use_container_width=True)