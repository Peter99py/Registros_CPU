import streamlit as st
from src.charts.line_charts import grafico_linhas_personalizado
from src.queries.queries import corespeed_vs_temp

# Título da aplicação
st.title("Meu Processador")


df_corespeed_vs_temp = corespeed_vs_temp()
grafico = grafico_linhas_personalizado(df_corespeed_vs_temp, 'time', 'avg_corespeed', titulo='Valor ao Longo do Tempo')
st.altair_chart(grafico, use_container_width=True)
    