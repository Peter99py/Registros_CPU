
import altair as alt


def grafico_linhas(df, coluna_x, coluna_y, coluna_categoria, titulo='Gráfico de Linhas'):

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X(f'{coluna_x}:O', title=coluna_x),
            y=alt.Y(f'{coluna_y}:Q', title=coluna_y),
            color=alt.Color(f'{coluna_categoria}:N', title=coluna_categoria),
            tooltip=[coluna_x, coluna_y]
        ).properties(
            title=titulo,
            width=700,
            height=400
        ).configure_title(
            fontSize=20,
            anchor='start',
            color='gray'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
    )
    return chart