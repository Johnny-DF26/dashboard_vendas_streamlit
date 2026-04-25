import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import requests

# ==================================================================================================
# Titulo do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide")
st.title("DASHBOARD DE VENDAS :shopping_cart:", text_alignment='center')

# ==================================================================================================
# Carregamento dos dados
# ==================================================================================================
url = "https://labdados.com/produtos"
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados.columns = ['produto', 'categoria','preco', 'frete', 'data_compra', 'vendedor',
                 'local_compra', 'avaliacao', 'tipo_pagamento', 'parcelas', 'lat', 'long']
dados['data_compra'] = pd.to_datetime(dados['data_compra'], format='%d/%m/%Y')

# Cálculo da receita total e quantidade de vendas
receita = dados['preco'].sum()
qtd_vendas = dados.shape[0]


# ==================================================================================================
# Função para formatar números grandes
# ==================================================================================================
def formata_numero(numero, casas_decimais=2):
    if numero >= 1e6:
        return f"{numero/1e6:.{casas_decimais}f} Mi"
    elif numero >= 1e3:
        return f"{numero/1e3:.{casas_decimais}f} Mil"
    else:
        return str(numero)


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


# Tabela Vendas por estado
qtd_vendas_estado = dados.groupby('local_compra').agg({
    'preco': 'count',
    'lat': 'mean',
    'long': 'mean'})
qtd_vendas_estado = qtd_vendas_estado.sort_values(by='preco', ascending=False).reset_index()
qtd_vendas_estado.columns = ['Estado', 'Qtd_vendas', 'Latitude', 'Longitude'] 


# ==================================================================================================
# Grafico por estado
# ==================================================================================================
# 2. Criação do Gráfico
def grafico_mapa(dataset, titulo, valor_coluna='Receita'):
    fig_mapa_receita = px.scatter_geo(
        dataset, 
        lat='Latitude', 
        lon='Longitude', 
        scope='south america', 
        size=valor_coluna, 
        template='seaborn', 
        hover_name='Estado',
        # Formatação de moeda e remoção de dados irrelevantes no hover
        hover_data={'Latitude': False, 'Longitude': False, valor_coluna: ':,.2f'},
        size_max=30, # Aumenta o destaque das bolhas maiores
        title=titulo,
        color=valor_coluna, # Adiciona uma escala de cor para reforçar a intensidade
        color_continuous_scale=['green', 'yellow', 'red'], # Define a escala de cores
    )

    # 3. Ajustes finos de layout (zoom e bordas)
    fig_mapa_receita.update_geos(
        showcountries=True, 
        countrycolor="RebeccaPurple",
        lataxis_range=[-35, 5], # Foca melhor no Brasil/América do Sul
        lonaxis_range=[-75, -35]
    )
    fig_mapa_receita.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        title_font_size=15
    )
    return fig_mapa_receita

def grafico_linhas(dataset, titulo, x_coluna, y_coluna):
    fig = px.line(dataset, 
                  x=x_coluna, 
                  y=y_coluna, 
                  title=titulo,
                  range_y=[dataset[y_coluna].min(), dataset[y_coluna].max() * 1.1], # Ajusta o limite do eixo Y para melhor visualização
                  markers=True, # Adiciona marcadores nos pontos de dados
                  template='seaborn', # Define o estilo do gráfico
                  color='ano',
                  line_dash='ano',
                  
    )
    fig.update_xaxes(tickangle=-30)
    fig.update_yaxes(title='Receita (R$)') # Formata o eixo Y como moeda
    return fig

def grafico_barras(dataset, titulo, x_coluna, y_coluna, orientacao='v'):
    fig = px.bar(dataset, 
                text_auto=True,
                x=x_coluna, 
                y=y_coluna, 
                title=titulo,
                #range_y=[0, dataset[y_coluna].max() * 1.1], # Ajusta o limite do eixo Y para melhor visualização
                template='seaborn', # Define o estilo do gráfico
                color=y_coluna, # Adiciona uma escala de cor para reforçar a intensidade
                color_continuous_scale='viridis_r', # Define a escala de cores
                orientation=orientacao,
    )
    fig.update_xaxes(tickangle=-30)
    fig.update_yaxes(title='(R$) Receita Vendas') # Formata o eixo Y como quantidade
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# ==================================================================================================
# Visualização dos KPIs e do gráfico
# ==================================================================================================
col1, col2 = st.columns(2)
with col1:
    col1.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
    st.plotly_chart(grafico_mapa(receita_estados,'Receita Total por Estado','Receita'), use_container_width=True)
    st.plotly_chart(grafico_barras(receita_estados.head(),'Receita de Vendas por Estado','Estado','Receita',), use_container_width=True)
with col2:
    col2.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))
    st.plotly_chart(grafico_linhas(receita_mensal, 'Receita Mensal por Categoria','mes','preco'), use_container_width=True)
    st.plotly_chart(grafico_barras(receita_categoria, 'Receita por Categoria','preco','categoria','h'), use_container_width=True)

# Exibição dos dados em formato de tabela
st.dataframe(dados)