import altair as alt


def grafico_linhas(df, coluna_x, coluna_y, coluna_categoria, titulo=None):

    chart = (alt.Chart(df).mark_line(point=True).encode(
            x=alt.X(f'{coluna_x}:O', title=coluna_x),
            y=alt.Y(f'{coluna_y}:Q', title=coluna_y),
            color=alt.Color(f'{coluna_categoria}:N', title=coluna_categoria),
            tooltip=[coluna_x, coluna_y])
            .properties(title=titulo, width=700, height=400)
            .configure_title(fontSize=20, anchor='start', color='gray')
            .configure_axis(labelFontSize=12, titleFontSize=14)
            )
    return chart

def grafico_colunas(df, coluna_x, coluna_y, titulo=None, mostrar_rotulos=True, formato_rotulo=',.0f', posicao_rotulo='fora', cor_rotulo=None, agregacao=None, largura=700, altura=400):

    y_field = f'{agregacao}({coluna_y}):Q' if agregacao else f'{coluna_y}:Q'

    base = alt.Chart(df).encode(
        x=alt.X(f'{coluna_x}:O', title=coluna_x, axis=alt.Axis(labelAngle=0)),
        y=alt.Y(y_field, title=coluna_y),
        tooltip=[
            alt.Tooltip(f'{coluna_x}:O', title=coluna_x),
            alt.Tooltip(y_field, title=coluna_y, format=formato_rotulo),])

    barras = base.mark_bar()

    camadas = [barras]

    if mostrar_rotulos:
        if posicao_rotulo == 'fora':
            baseline = 'bottom'
            dy = -5
            default_color = 'black'
        else:
            baseline = 'top'
            dy = 3
            default_color = 'white'

        texto = base.mark_text(
            align='center',
            baseline=baseline,
            dy=dy,
            color=cor_rotulo or default_color
        ).encode(
            text=alt.Text(y_field, format=formato_rotulo)
        )

        camadas.append(texto)

    chart = alt.layer(*camadas).properties(title=titulo, width=largura, height=altura).configure_title(fontSize=20, anchor='start', color='gray').configure_axis(labelFontSize=12, titleFontSize=14)

    return chart