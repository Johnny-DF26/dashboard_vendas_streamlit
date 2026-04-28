
"""
Dashboard de Vendas com Streamlit

Este módulo inicializa o dashboard principal, organiza as abas e integra os principais KPIs e gráficos.
"""

import streamlit as st
from graficos import grafico_barras, grafico_linhas, grafico_mapa, grafico_vendedores
from formatacao import formata_numero
import pandas as pd
import requests

# ==================================================================================================
# Título do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide", page_title='Dashboard Vendas')
st.title("DASHBOARD DE VENDAS :shopping_cart:", text_alignment='center')


# ==================================================================================================
# Carregamento dos dados da API
# ==================================================================================================
url = "https://labdados.com/produtos"

regioes = ['Brasil', 'Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

st.sidebar.title("Filtros :arrow_down_small:")
regiao = st.sidebar.selectbox("Selecione a região", regioes)
if regiao == 'Brasil':
    regiao = ''

todos_anos = st.sidebar.checkbox("Dados de todo o periodo :date:", value=True)
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider("Ano", 2020, 2023)

query_string = {'regiao': regiao.lower(), 'ano': ano}

response = requests.get(url, params=query_string)

dados = pd.DataFrame.from_dict(response.json())
dados.columns = [
    'produto', 'categoria', 'preco', 'frete', 'data_compra', 'vendedor',
    'local_compra', 'avaliacao', 'tipo_pagamento', 'parcelas', 'lat', 'long'
]
# Converte a coluna de data para o formato datetime
dados['data_compra'] = pd.to_datetime(dados['data_compra'], format='%d/%m/%Y')

fitro_vendedores = st.sidebar.multiselect('Selecione os vendedores', options=dados['vendedor'].unique())
if fitro_vendedores:
    dados = dados[dados['vendedor'].isin(fitro_vendedores)]


# ==================================================================================================
# Tabela de receita por estado
# ==================================================================================================
receita_estados = dados.groupby('local_compra').agg({
    'preco': 'sum',
    'lat': 'mean',
    'long': 'mean'
})
receita_estados = receita_estados.sort_values(by='preco', ascending=False).reset_index()
receita_estados.columns = ['Estado', 'Receita', 'Latitude', 'Longitude']

# ==================================================================================================
# Receita Mensal por categoria
# ==================================================================================================
receita_mensal = dados.groupby(dados['data_compra'].dt.to_period('M')).agg({'preco': 'sum'}).reset_index()
receita_mensal['ano'] = receita_mensal['data_compra'].dt.year
receita_mensal['mes'] = receita_mensal['data_compra'].dt.to_timestamp().dt.month_name(locale='pt_br').str[:3]  # Abreviação do mês

# ==================================================================================================
# Receita por categoria de produto
# ==================================================================================================
receita_categoria = dados.groupby('categoria').agg({'preco': 'sum'}).reset_index()
receita_categoria = receita_categoria.sort_values(by='preco', ascending=False)

# ==================================================================================================
# Cálculo de Vendas
# ==================================================================================================
qtd_vendas = dados.shape[0]
qtd_vendas_estado = dados.groupby('local_compra')[['preco', 'lat', 'long']].agg({'preco': 'count', 'lat': 'mean', 'long': 'mean'})
qtd_vendas_estado = qtd_vendas_estado.sort_values(by='preco', ascending=False).reset_index()
qtd_vendas_estado.columns = ['Estado', 'Quantidade', 'Latitude', 'Longitude']

# ==================================================================================================
# Quantidade de vendas por categoria
# ==================================================================================================
categoria_mais_vendida = dados.groupby('categoria')[['preco', 'lat', 'long']].agg({'preco': 'count'})
categoria_mais_vendida = categoria_mais_vendida.sort_values(by='preco', ascending=False).reset_index()
categoria_mais_vendida.columns = ['Categoria', 'Quantidade']


# ==================================================================================================
# Quantidade de vendas por produto
# ==================================================================================================
produtos_mais_vendidos = dados.groupby('produto').agg({'preco': 'count'})
produtos_mais_vendidos = produtos_mais_vendidos.sort_values(by='preco', ascending=False).reset_index()
produtos_mais_vendidos.columns = ['Produto', 'Quantidade']

# ==================================================================================================
# Quantidade de vendas por tipo de pagamento
# ==================================================================================================
tipo_pagamento_mais_utilizado = dados.groupby('tipo_pagamento').agg({'preco': 'count'}).sort_values(by='preco', ascending=False).reset_index()
periodo_mais_vendido = dados.groupby(dados['data_compra'].dt.to_period('M')).agg({'preco': 'count'}).sort_values(by='data_compra').reset_index()


# ==================================================================================================
# Cria as abas principais do dashboard
# ==================================================================================================
aba1, aba2, aba3 = st.tabs(['💲 Receita', '📈 Quantidade de vendas', '🧑‍💼 Vendedores'])

# -----------------------------
# Aba 1: Receita
# -----------------------------
with aba1:
    # Dashboard sobre a receita gerada, com gráficos de linha e mapa
    col1, col2 = st.columns(2)

    # Gráfico de receita (coluna 1)
    with col1:
        # Exibe os KPIs de receita total e receita mensal
        receita = dados['preco'].sum()
        st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
        # Exibe o gráfico de receita mensal
        fig_mapa = grafico_mapa(receita_estados, 'Receita Total por estados', 'Receita')
        st.plotly_chart(fig_mapa, width='stretch')
        # Exibe o gráfico de barras de receita por categoria
        fig_linhas = grafico_linhas(receita_mensal, 'Receita Mensal por Categoria','mes','preco')
        st.plotly_chart(fig_linhas, width='stretch')

    # Gráfico de receita (coluna 2)
    with col2:
        # Exibe o KPI de quantidade de vendas
        qtd_vendas = dados.shape[0]
        st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))

        # Exibe o gráfico de linhas da receita mensal
        fig_barras = grafico_barras(receita_estados.head(), 'Receita de Vendas por Estado', 'Estado', 'Receita')
        st.plotly_chart(fig_barras, width='stretch')
        # Exibe o gráfico de barras de receita por categoria
        fig_barras = grafico_barras(
            receita_categoria.sort_values(by='preco', ascending=True),
            'Receita por Categoria',
            'preco',
            'categoria',
            'h'
        )
        st.plotly_chart(fig_barras, width='stretch')
        # Espaço reservado para outros gráficos ou KPIs

# -----------------------------
# Aba 2: Quantidade de vendas
# -----------------------------

with aba2:
    # Dashboard sobre a quantidade de vendas, com gráficos de linha e mapa
    col1, col2 = st.columns(2)

    # KPI de receita (coluna 1)
    with col1:
        receita = dados['preco'].sum()
        st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')

        mapa_estados_mais_vendidos = grafico_mapa(qtd_vendas_estado, 'Quantidade de Vendas por Estado', 'Quantidade')
        st.plotly_chart(mapa_estados_mais_vendidos, width='stretch')

        fig_categoria_mais_vendidas = grafico_barras(categoria_mais_vendida.sort_values(by='Quantidade', ascending=True), 
                                                     'Categoria de Produtos mais vendidos', 
                                                     'Quantidade', 
                                                     'Categoria', 
                                                     orientacao='h')
        st.plotly_chart(fig_categoria_mais_vendidas, width='stretch')


    # Gráfico de barras de quantidade de vendas por categoria (coluna 2)
    with col2:
        # Exibe o gráfico de barras de quantidade de vendas por categoria
        qtd_vendas = dados.shape[0]
        st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))

        fig_barras_estados = grafico_barras(qtd_vendas_estado.head(), 'Quantidade de Vendas por Estado', 'Estado', 'Quantidade')
        st.plotly_chart(fig_barras_estados, width='stretch')

        fig_produtos_mais_vendidos = grafico_barras(produtos_mais_vendidos.head(10).sort_values(by='Quantidade', ascending=True), 
                                                     'Quantidade de Produtos mais vendidos', 
                                                     'Quantidade', 
                                                     'Produto', 
                                                     orientacao='h')
        st.plotly_chart(fig_produtos_mais_vendidos, width='stretch')

# -----------------------------
# Aba 3: Vendedores
# -----------------------------
with aba3:
    # Dashboard sobre os vendedores, com gráficos de barras
    col1, col2 = st.columns(2)
    # Input para selecionar a quantidade de vendedores exibidos
    qtd_vendedores = st.number_input('Quantidade de Vendedores', min_value=2, max_value=10, value=5)

    vendedores = pd.DataFrame(dados.groupby('vendedor')['preco'].agg(['sum', 'count']))
    vend = vendedores[['sum','count']].sort_values(by='sum', ascending=False).head(qtd_vendedores)

    # Gráfico de receita por vendedor (coluna 1)
    with col1:
        receita = dados['preco'].sum()
        st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')

        grafico_vendedores(vend, qtd_vendedores, 'Vendedores por Receita', tipo='sum')

    # Gráfico de quantidade de vendas por vendedor (coluna 2)
    with col2:
        qtd_vendas = dados.shape[0]
        qtd_vendas_total = st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))

        grafico_vendedores(vend, qtd_vendedores, 'Vendedores por Quantidade', tipo='count')

