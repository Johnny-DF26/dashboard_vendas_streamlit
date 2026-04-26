
"""
Dashboard de Vendas com Streamlit

Este módulo inicializa o dashboard principal, organiza as abas e integra os principais KPIs e gráficos.
"""

import streamlit as st
from pages.aba_receita import grafico_barras, grafico_linhas, grafico_mapa
from pages.aba_vendedores import grafico_vendedores
from pages.formatacao import get_receita, get_qtd_vendas
from pages.aba_receita import receita_estados, receita_mensal, receita_categoria
from pages.aba_vendas import figura1, figura2, figura3
from pages.dataframe import dados
import seaborn as sns

# ==================================================================================================
# Título do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide", page_title='Dashboard de Vendas')
st.title("DASHBOARD DE VENDAS :shopping_cart:", text_alignment='center')


qtd_vendas_estado = dados.groupby('local_compra')[['preco', 'lat', 'long']].agg({'preco': 'count', 'lat': 'mean', 'long': 'mean'})
qtd_vendas_estado = qtd_vendas_estado.sort_values(by='preco', ascending=False).reset_index()

categoria_mais_vendida = dados.groupby('categoria')[['preco', 'lat', 'long']].agg({'preco': 'count'}).sort_values(by='preco', ascending=False).reset_index()
produtos_mais_vendidos = dados.groupby('produto').agg({'preco': 'count'}).sort_values(by='preco', ascending=False).reset_index()
tipo_pagamento_mais_utilizado = dados.groupby('tipo_pagamento').agg({'preco': 'count'}).sort_values(by='preco', ascending=False).reset_index()
periodo_mais_vendido = dados.groupby(dados['data_compra'].dt.to_period('M')).agg({'preco': 'count'}).sort_values(by='data_compra').reset_index()

st.write(dados)
st.write(qtd_vendas_estado)
st.write(categoria_mais_vendida)
st.write(produtos_mais_vendidos)
st.write(tipo_pagamento_mais_utilizado)
st.write(periodo_mais_vendido)
# ==================================================================================================
# Visualização dos KPIs e dos gráficos principais
# ==================================================================================================

# Cria as abas principais do dashboard
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
        get_receita()
        # Exibe o gráfico de receita mensal
        fig_mapa = grafico_mapa(receita_estados, 'Receita Total por estados')
        st.plotly_chart(fig_mapa, width='stretch')
        # Exibe o gráfico de barras de receita por categoria
        fig_barras = grafico_barras(receita_estados.head(), 'Receita de Vendas por Estado', 'Estado', 'Receita')
        st.plotly_chart(fig_barras, width='stretch')

    # Gráfico de receita (coluna 2)
    with col2:
        # Exibe o KPI de quantidade de vendas
        get_qtd_vendas()
        # Exibe o gráfico de linhas da receita mensal
        fig_linhas = grafico_linhas(receita_mensal, 'Receita Mensal por Categoria','mes','preco')
        st.plotly_chart(fig_linhas, width='stretch')
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
        get_receita()
        st.pyplot(figura1())
        figura3 = figura3()
        st.pyplot(figura3)

    # KPI de quantidade de vendas (coluna 2)
    with col2:
        get_qtd_vendas()
        # 2. Criando o gráfico de mapa
        st.plotly_chart(figura2())

# -----------------------------
# Aba 3: Vendedores
# -----------------------------
with aba3:
    # Dashboard sobre os vendedores, com gráficos de barras
    col1, col2 = st.columns(2)
    # Input para selecionar a quantidade de vendedores exibidos
    qtd_vendedores = st.number_input('Quantidade de Vendedores', min_value=2, max_value=10, value=2)

    # Gráfico de receita por vendedor (coluna 1)
    with col1:
        get_receita()
        grafico_vendedores(qtd_vendedores, tipo='sum')
    # Gráfico de quantidade de vendas por vendedor (coluna 2)
    with col2:
        get_qtd_vendas()
        grafico_vendedores(qtd_vendedores, tipo='count')


# ==================================================================================================
# Exibição dos dados em formato de tabela (opcional)
# ==================================================================================================
# st.dataframe(dados)