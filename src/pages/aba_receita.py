import streamlit as st
from pages.dataframe import dados
import plotly.express as px

# Cálculo da receita total e quantidade de vendas
receita = dados['preco'].sum()
qtd_vendas = dados.shape[0]

# ==================================================================================================
# Tabelas
# ==================================================================================================
# Tabela de receita por estado
receita_estados = dados.groupby('local_compra').agg({
    'preco': 'sum',
    'lat': 'mean',
    'long': 'mean'
})
receita_estados = receita_estados.sort_values(by='preco', ascending=False).reset_index()
receita_estados.columns = ['Estado', 'Receita', 'Latitude', 'Longitude']

# Receita Mensal por categoria
receita_mensal = dados.groupby(dados['data_compra'].dt.to_period('M')).agg({'preco': 'sum'}).reset_index()
receita_mensal['ano'] = receita_mensal['data_compra'].dt.year
receita_mensal['mes'] = receita_mensal['data_compra'].dt.to_timestamp().dt.month_name(locale='pt_br').str[:3]  # Abreviação do mês

# Receita por categoria de produto
receita_categoria = dados.groupby('categoria').agg({'preco': 'sum'}).reset_index()
receita_categoria = receita_categoria.sort_values(by='preco', ascending=False)


# ==================================================================================================
# Gráficos
# ==================================================================================================
def grafico_mapa(df, titulo) -> px.scatter_mapbox:
    """
    Cria um mapa de calor interativo com scatter_mapbox.
    """
    fig = px.scatter_mapbox(
        df, 
        lat='Latitude', 
        lon='Longitude', 
        size='Receita', 
        color='Receita',
        size_max=20,
        color_continuous_scale="Jet", # Escala de cor mais legível
        hover_name='Estado',
        hover_data={'Receita': ':,.2f', 'Latitude': False, 'Longitude': False}, # Formata valores e limpa o hover
        title=titulo,
        zoom=3, 
        mapbox_style="open-street-map",

    )
    
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0.05,        # 0 é total esquerda, 0.05 dá um pequeno recuo
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

def grafico_linhas(df, titulo, x, y) -> px.line:
    # Garante que a coluna de data esteja no formato datetime e ordenada
    fig = px.line(
        df, 
        x=x, 
        y=y,
        color='ano',
        title=f"<b>{titulo}</b>",
        markers=True,         # Adiciona pontos na linha para facilitar a leitura
        template="plotly_white" # Fundo limpo para destacar os dados
    )

    # Aprimoramentos de Interatividade e Design
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0.05,        # 0 é total esquerda, 0.05 dá um pequeno recuo
            'y': 0.98,        # Ajusta a altura dentro da margem
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 20, 'color': 'black', 'family': 'Arial'}
        },
        xaxis_title='Período',
        yaxis_title='Receita (R$)',
        hovermode="x unified", # Exibe todos os valores daquele ponto no tempo juntos
        title_x=0.5,           # Centraliza o título
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