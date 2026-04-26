import streamlit as st
from pages.aba_receita import graficos_receita_coluna1, graficos_receita_coluna2
from pages.aba_vendedores import grafico_vendedores
from pages.formatacao import get_receita, get_qtd_vendas


# ==================================================================================================
# Titulo do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide", page_title='Dashboard de Vendas')
st.title("DASHBOARD DE VENDAS :shopping_cart:", text_alignment='center')


# ==================================================================================================
# Visualização dos KPIs e do gráfico
# ==================================================================================================
aba1, aba2, aba3 = st.tabs(['💲 Receita', '📈 Quantidade de vendas', '🧑‍💼 Vendedores'], )

# Aba 1: Receita
with aba1:
    # Dashboard sobre a receita gerada, com gráficos de linha e mapa
    col1, col2 = st.columns(2)

    # Busca grafico de receita na pasta receita
    with col1:
        graficos_receita_coluna1()
    with col2:
        pass
        graficos_receita_coluna2()

# Aba 2: Quantidade de vendas
with aba2:
    # Dashboard sobre a quantidade de vendas, com gráficos de linha e mapa
    col1, col2 = st.columns(2)

    with col1:
        get_receita()
    with col2:
        get_qtd_vendas()

# Aba 3: Vendedores
with aba3:
    # Dashboard sobre os vendedores, com gráficos de barras
    col1, col2 = st.columns(2)
    qtd_vendedores = st.number_input('Quantidade de Vendedores', min_value=2, max_value=10, value=2)

    with col1:
        get_receita()
        grafico_vendedores(qtd_vendedores, tipo='sum')
    with col2:
        get_qtd_vendas()
        grafico_vendedores(qtd_vendedores, tipo='count')


# Exibição dos dados em formato de tabela
#st.dataframe(dados)