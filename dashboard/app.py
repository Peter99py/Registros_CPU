import streamlit as st
from src.charts.line_charts import grafico_linhas
from src.queries.queries import time_vs_temp, temp_vs_speed, time_vs_power, temp_vs_power

# Título da aplicação
st.markdown(
    "<h1 style='text-align: center; color: black;'>Meu Processador</h1>",
    unsafe_allow_html=True
)


df_temp_vs_speed = temp_vs_speed()
grafico = grafico_linhas(df_temp_vs_speed, "core temp", "core speed", 'type', titulo='Temperatura do Núcleo vs Velocidade do Núcleo')
st.altair_chart(grafico, use_container_width=True)

df_time_vs_temp = time_vs_temp()
grafico = grafico_linhas(df_time_vs_temp, "time of day", "core temp", 'type', titulo='Temperatura do Núcleo ao Longo do Dia')
st.altair_chart(grafico, use_container_width=True)

df_time_vs_power = time_vs_power()
grafico = grafico_linhas(df_time_vs_power, "time of day", "cpu power", 'type', titulo='Energia do CPU ao Longo do Dia')
st.altair_chart(grafico, use_container_width=True)

df_temp_vs_power = temp_vs_power()
grafico = grafico_linhas(df_temp_vs_power, "core temp", "cpu power", 'type', titulo='Energia do CPU vs Temperatura do Núcleo')
st.altair_chart(grafico, use_container_width=True)