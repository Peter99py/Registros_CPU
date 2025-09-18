# Renderização de gráficos com Altair
# Descrição: funções utilitárias para gráficos de linhas e colunas.

import altair as alt

# Gráfico de linhas: séries com ponto e tooltip
def grafico_linhas(df, coluna_x, coluna_y, coluna_categoria, titulo=None):

    # Constrói o gráfico com Altair
    chart = (alt.Chart(df).mark_line(point=True).encode(
            # Eixo X: categórico/ordinal (O) e rótulo
            # X ordinal (categorias)
            x=alt.X(f'{coluna_x}:O', title=coluna_x),
            # Eixo Y: quantitativo (Q) e rótulo
            # Y quantitativo com título
            y=alt.Y(f'{coluna_y}:Q', title=coluna_y),
            # Cor por categoria (N) para comparar séries
            color=alt.Color(f'{coluna_categoria}:N', title=coluna_categoria),
            # Tooltip: mostra X e Y ao passar o mouse
            # Tooltip: título customizado e formatação numérica
            tooltip=[coluna_x, coluna_y])
            # Título e dimensões padrão do gráfico
            .properties(title=titulo, width=700, height=400)
            # Estilo do título (tamanho, alinhamento, cor)
            .configure_title(fontSize=20, anchor='start', color='gray')
            # Estilo dos eixos (tamanhos das fontes)
            .configure_axis(labelFontSize=12, titleFontSize=14)
            )
    # Retorna o objeto Altair configurado
    return chart


# Gráfico de colunas (barras), com rótulos opcionais
def grafico_colunas(df, coluna_x, coluna_y, titulo=None, mostrar_rotulos=True, formato_rotulo=',.0f', posicao_rotulo='fora', cor_rotulo=None, agregacao=None, largura=700, altura=400):

    # Campo do eixo Y: agrega se informado (ex: sum, mean), senão usa a coluna bruta
    y_field = f'{agregacao}({coluna_y}):Q' if agregacao else f'{coluna_y}:Q'

    # Base codificada (eixos e tooltip) reutilizada por barras e textos
    base = alt.Chart(df).encode(
            # Eixo X: categórico/ordinal (O) e rótulo
            # X ordinal (categorias), sem rotação de rótulos
        x=alt.X(f'{coluna_x}:O', title=coluna_x, axis=alt.Axis(labelAngle=0)),
            # Eixo Y: quantitativo (Q) e rótulo
            # Y quantitativo com título amigável
        y=alt.Y(y_field, title=coluna_y),
            # Tooltip: mostra X e Y ao passar o mouse
            # Tooltip: título customizado e formatação numérica
        tooltip=[
            alt.Tooltip(f'{coluna_x}:O', title=coluna_x),
            alt.Tooltip(y_field, title=coluna_y, format=formato_rotulo),])

    # Camada principal: barras
    barras = base.mark_bar()

    # Lista de camadas que comporão o gráfico (barras + textos opcionais)
    camadas = [barras]

    # Opcional: adiciona rótulos de valor nas barras
    if mostrar_rotulos:
        # Posição do rótulo: fora (acima) ou dentro da barra
        if posicao_rotulo == 'fora':
            # Baseline para texto acima da barra e deslocamento vertical
            baseline = 'bottom'
            dy = -5
            default_color = 'black'
        else:
            # Baseline para texto dentro da barra e deslocamento vertical
            baseline = 'top'
            dy = 3
            default_color = 'white'

        # Camada de texto: centraliza e aplica cor determinada
        texto = base.mark_text(
            align='center',
            baseline=baseline,
            dy=dy,
            color=cor_rotulo or default_color
        ).encode(
            # Valor formatado conforme `formato_rotulo` (ex: 1.2k, 1.000)
            text=alt.Text(y_field, format=formato_rotulo)
        )

        # Adiciona os rótulos à lista de camadas
        camadas.append(texto)

    # Combina camadas e aplica título, tamanho e estilos globais
    chart = alt.layer(*camadas).properties(title=titulo, width=largura, height=altura).configure_title(fontSize=20, anchor='start', color='gray').configure_axis(labelFontSize=12, titleFontSize=14)

    return chart