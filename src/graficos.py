import streamlit as st
import plotly.express as px


# ==================================================================================================
# Gráficos
# ==================================================================================================
def grafico_mapa(df, titulo, coluna):
    """Cria um mapa de calor interativo usando scatter_mapbox.

    Args:
        df (pandas.DataFrame): DataFrame contendo colunas 'Latitude', 'Longitude' e a
            coluna numérica indicada por ``coluna``.
        titulo (str): Título do gráfico.
        coluna (str): Nome da coluna do DataFrame usada para dimensionar e colorir os pontos.

    Returns:
        plotly.graph_objs._figure.Figure: Figura Plotly pronta para exibição ou plotagem.
    """
    fig = px.scatter_mapbox(
        df, 
        lat='Latitude', 
        lon='Longitude', 
        size=coluna, 
        color=coluna,
        size_max=20,
        color_continuous_scale="Jet", # Escala de cor mais legível
        hover_name='Estado',
        hover_data={coluna: ':,.2f', 'Latitude': False, 'Longitude': False}, # Formata valores e limpa o hover
        title=titulo,
        zoom=3, 
        mapbox_style="open-street-map",

    )
    
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0,        # 0 é total esquerda, 0.05 dá um pequeno recuo
            'y': 0.98,        # Ajusta a altura dentro da margem
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 20, 'color': 'black', 'family': 'Arial'}
        },
        margin={"r":0,"t":40,"l":0,"b":0},
        plot_bgcolor="white",
        paper_bgcolor="white", # Fundo transparente para integrar com dashboards
        mapbox_center={"lat": df['Latitude'].mean(), "lon": df['Longitude'].mean()} # Centraliza conforme os dados
    )

    return fig

def grafico_barras(df, titulo, x, y, orientacao='v'):
    """Gera um gráfico de barras estilizado com Plotly Express.

    Args:
        df (pandas.DataFrame): Fonte de dados para o gráfico.
        titulo (str): Título do gráfico.
        x (str): Nome da coluna a usar no eixo x (também usada para colorir).
        y (str): Nome da coluna a usar no eixo y.
        orientacao (str, optional): 'v' para vertical (padrão) ou 'h' para horizontal.

    Returns:
        plotly.graph_objs._figure.Figure: Figura Plotly do gráfico de barras.
    """

    fig = px.bar(df, x=x, y=y, color=x, title=titulo,
                text_auto=True, orientation= orientacao,
                template='seaborn',
                color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=False,
                      title={
                        'text': titulo,
                        'x': 0.05,        # 0 é total esquerda, 0.05 dá um pequeno recuo
                        'y': 0.98,        # Ajusta a altura dentro da margem
                        'xanchor': 'left',
                        'yanchor': 'top',
                        'font': {'size': 20, 'color': 'black', 'family': 'Arial'}
        },)

    return fig

def grafico_linhas(df, titulo, x, y):
    """Cria um gráfico de linhas com seleção de intervalo e estilos úteis.

    Esta função assume que o DataFrame pode ter uma coluna de agregação por `ano`
    (usada como cor). Adiciona marcadores, controle de intervalo (rangeslider)
    e botões de seleção de período.

    Args:
        df (pandas.DataFrame): Dados com colunas referenciadas por ``x`` e ``y``.
        titulo (str): Título do gráfico.
        x (str): Coluna do eixo x (geralmente uma data ou período).
        y (str): Coluna do eixo y (métrica a ser exibida).

    Returns:
        plotly.graph_objs._figure.Figure: Figura Plotly do gráfico de linhas.
    """

    # Garante que a coluna de data esteja no formato datetime e ordenada
    fig = px.line(
        df, 
        x=x, 
        y=y,
        color='ano',
        markers=True,         # Adiciona pontos na linha para facilitar a leitura
        template="plotly_white" # Fundo limpo para destacar os dados
    )

    # Aprimoramentos de Interatividade e Design
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0,        # 0 é total esquerda, 0.05 dá um pequeno recuo
            'y': 0.98,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 20, 'color': 'black', 'family': 'Arial'}
        },
        xaxis_title='Período',
        yaxis_title='Receita (R$)',
        hovermode="x unified", # Exibe todos os valores daquele ponto no tempo juntos        # Centraliza o título
    )

    # Adiciona botões de seleção de tempo (1m, 6m, YTD, Tudo)
    fig.update_xaxes(
        rangeslider_visible=True, # Adiciona a barra de deslize abaixo do gráfico
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all", label="Tudo")
            ])
        )
    )

    return fig

def grafico_vendedores(dataset, qtd_vendedores, titulo, tipo='sum') -> None:
    """
    Exibe um gráfico de barras com os top vendedores por receita ou quantidade de vendas.

    Args:
        qtd_vendedores (int): Quantidade de vendedores a exibir no ranking.
        tipo (str): 'sum' para receita, 'count' para quantidade de vendas.
    """
    # Nota: a função recebe um dataset já pré-aggregado (index = vendedor,
    # colunas com valores agregados como 'sum' ou 'count') e plota os top N.
    # O gráfico é renderizado diretamente em Streamlit com `st.plotly_chart`.
    # Seleciona os top vendedores conforme o critério
    fig_vendedores = px.bar(
        dataset,
        x=tipo,
        y=dataset.index,
        text_auto=True,
        title=f'Top {qtd_vendedores} {titulo}' if tipo=='sum' else f'Top {qtd_vendedores} Vendedores por Quantidade',
        template='seaborn',
        color=dataset.index,
        color_continuous_scale='spectral'
    )
    
    fig_vendedores.update_xaxes(title='Receita (R$)' if tipo=='sum' else 'Quantidade de Vendas')
    fig_vendedores.update_yaxes(title='Vendedor')
    fig_vendedores.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    
    st.plotly_chart(fig_vendedores, use_container_width=True)
