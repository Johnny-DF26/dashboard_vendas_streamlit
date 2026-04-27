import streamlit as st
import plotly.express as px


# ==================================================================================================
# Gráficos
# ==================================================================================================
def grafico_mapa(df, titulo, coluna):
    """
    Cria um mapa de calor interativo com scatter_mapbox.
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
