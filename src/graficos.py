import streamlit as st
import plotly.express as px


"""Módulo de utilitários para criação de gráficos Plotly usados no dashboard.

Contém funções que geram figuras Plotly prontas para exibição em Streamlit
(`st.plotly_chart`). As funções esperam DataFrames com colunas específicas
documentadas em cada função.

Dependências:
    - streamlit
    - plotly
"""


# ==================================================================================================
# Gráficos
# ==================================================================================================
def grafico_mapa(df, titulo, coluna):
    """Gera um mapa de pontos dimensionados e coloridos por uma métrica.

    A função cria uma figura Plotly `scatter_mapbox` centralizada nos dados
    passados em ``df``. Ideal para visualizar intensidades por localização.

    Args:
        df (pandas.DataFrame): Fonte de dados; deve conter pelo menos as colunas
            ``'Latitude'`` e ``'Longitude'`` (números) e a coluna numérica indicada
            por ``coluna``.
        titulo (str): Texto do título exibido no gráfico.
        coluna (str): Nome da coluna numérica usada para definir tamanho e cor dos pontos.

    Returns:
        plotly.graph_objs._figure.Figure: Objeto figura Plotly configurado.

    Example:
        >>> fig = grafico_mapa(df, 'Mapa de Vendas', 'receita')
        >>> st.plotly_chart(fig)
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
    """Cria um gráfico de barras com layout consistente para o dashboard.

    O gráfico utiliza cores qualitativas e remove a legenda por padrão para
    manter uma aparência limpa quando integrado em painéis.

    Args:
        df (pandas.DataFrame): Dados contendo as colunas referenciadas por ``x`` e ``y``.
        titulo (str): Texto do título exibido no gráfico.
        x (str): Nome da coluna para o eixo x (usada também para colorir barras).
        y (str): Nome da coluna para o eixo y (valores mostrados nas barras).
        orientacao (str, optional): 'v' (vertical) ou 'h' (horizontal). Padrão: 'v'.

    Returns:
        plotly.graph_objs._figure.Figure: Objeto figura Plotly do gráfico de barras.

    Example:
        >>> fig = grafico_barras(df, 'Receita por Categoria', 'categoria', 'receita')
        >>> st.plotly_chart(fig)
    """

    fig = px.bar(df, x=x, y=y, title=titulo,
                text_auto=True, orientation= orientacao,
                template='seaborn',
                color_discrete_sequence=px.colors.qualitative.Set3)
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
    """Gera um gráfico de linhas com recursos de seleção temporal.

    Inclui marcadores, `rangeslider` e botões para seleção rápida de janelas
    temporais (1m, 6m, YTD, tudo). Caso exista uma coluna ``'ano'`` no DataFrame,
    ela será usada para colorir as séries.

    Args:
        df (pandas.DataFrame): Dados contendo as colunas referenciadas por ``x`` e ``y``.
        titulo (str): Texto do título exibido no gráfico.
        x (str): Coluna do eixo x (tipicamente datas/períodos).
        y (str): Coluna do eixo y (métrica a ser exibida).

    Returns:
        plotly.graph_objs._figure.Figure: Objeto figura Plotly do gráfico de linhas.

    Notes:
        - Recomenda-se que a coluna `x` esteja no tipo datetime para melhor
          comportamento do `rangeslider`.

    Example:
        >>> fig = grafico_linhas(df_serie, 'Receita Mensal', 'data', 'receita')
        >>> st.plotly_chart(fig)
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
    """Plota e exibe o ranking dos principais vendedores.

    A função espera receber um objeto ``dataset`` já agrupado/ordenado em que o
    índice seja o nome do vendedor e existam colunas numéricas agregadas
    (por exemplo, soma de receita ou contagem de vendas). A função constrói um
    `px.bar` e renderiza diretamente em Streamlit.

    Args:
        dataset (pandas.DataFrame): DataFrame agrupado por vendedor (index = vendedor).
        qtd_vendedores (int): Número de vendedores a exibir (top N).
        titulo (str): Texto do título que complementa o ranking.
        tipo (str, optional): Chave da coluna usada como valor no eixo x; por
            convenção usa-se 'sum' para receita e 'count' para quantidade.

    Returns:
        None: O gráfico é exibido inline em Streamlit com `st.plotly_chart`.

    Example:
        >>> top = df.groupby('vendedor').receita.sum().nlargest(10)
        >>> grafico_vendedores(top, 10, 'Receita', tipo='sum')
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
