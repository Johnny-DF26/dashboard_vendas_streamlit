import streamlit as st
import pandas as pd
import requests
from pages.graph import formata_numero
from pages.aba_receita import graficos_coluna1, graficos_coluna2
from pages.dataframe import dados
import plotly.express as px
from pages.aba_vendedores import grafico_vendedores

# ==================================================================================================
# Titulo do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide", page_title='Dashboard de Vendas')
st.title("DASHBOARD DE VENDAS :shopping_cart:", text_alignment='center')


receita = dados['preco'].sum()
qtd_vendas = dados.shape[0]


# ==================================================================================================
# Visualização dos KPIs e do gráfico
# ==================================================================================================
aba1, aba2, aba3 = st.tabs(['💲 Receita', '📈 Quantidade de vendas', '🧑‍💼 Vendedores'], )

with aba1:
    # Dashboard sobre a receita gerada, com gráficos de linha e mapa
    col1, col2 = st.columns(2)
    # Busca grafico de receita na pasta receita
    with col1:
        graficos_coluna1()
    with col2:
        graficos_coluna2()


with aba2:
    # Dashboard sobre a quantidade de vendas, com gráficos de linha e mapa
    col1, col2 = st.columns(2)
    with col1:
        pass
        #st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
    with col2:
        pass
        #st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))


with aba3:
    # Dashboard sobre os vendedores, com gráficos de barras
    col1, col2 = st.columns(2)
    qtd_vendedores = st.number_input('Quantidade de Vendedores', min_value=2, max_value=10, value=2)

    with col1:
        st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
        grafico_vendedores(qtd_vendedores, tipo='sum')

    with col2:
        st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))
        grafico_vendedores(qtd_vendedores, tipo='count')


# Exibição dos dados em formato de tabela
#st.dataframe(dados)