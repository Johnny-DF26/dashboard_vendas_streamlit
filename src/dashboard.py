
"""
Dashboard de Vendas com Streamlit

Este módulo inicializa o dashboard principal, organiza as abas e integra os principais KPIs e gráficos.
"""

import streamlit as st
from pages.aba_receita import graficos_receita_coluna1, graficos_receita_coluna2
from pages.aba_vendedores import grafico_vendedores
from pages.formatacao import get_receita, get_qtd_vendas
from pages.dataframe import dados
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ==================================================================================================
# Título do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide", page_title='Dashboard de Vendas')
st.title("DASHBOARD DE VENDAS :shopping_cart:", text_alignment='center')



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
        graficos_receita_coluna1()
    # Gráfico de receita (coluna 2)
    with col2:
        # Espaço reservado para outros gráficos ou KPIs
        graficos_receita_coluna2()

# -----------------------------
# Aba 2: Quantidade de vendas
# -----------------------------

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

with aba2:
    # Dashboard sobre a quantidade de vendas, com gráficos de linha e mapa
    col1, col2 = st.columns(2)

    # KPI de receita (coluna 1)
    with col1:
        get_receita()
        sns.set_theme()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=qtd_vendas_estado.head(10), x='local_compra', y='preco', palette='viridis', ax=ax)
        ax.set_title('Quantidade de Vendas por Estado', loc='left', fontsize=18, fontweight='bold')
        ax.set_ylim(0, qtd_vendas_estado['preco'].max() * 1.1)
        ax.set_xlabel('Estado')
        ax.set_ylabel('Quantidade de Vendas')

        for p in ax.patches:
            label = f'{p.get_height():.0f}'
            ax.annotate(label, (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
        st.pyplot(fig)

    # KPI de quantidade de vendas (coluna 2)
    with col2:
        get_qtd_vendas()
        # 2. Criando o gráfico de mapa
        fig = px.scatter_mapbox(
            qtd_vendas_estado,
            lat="lat",
            lon="long",
            size="preco",
            color="preco",
            hover_name="local_compra",
            zoom=3,
            mapbox_style="open-street-map", 
            title="Distribuição de Vendas por Estado",
            color_continuous_scale="Jet"
        )

        # AJUSTE DE CORES DO LAYOUT
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            paper_bgcolor="white",    # Cor da área externa (lateral/fundo)
            plot_bgcolor="white",     # Cor da área interna
            font_color="black",       # Cor do título e legendas
            title_font_size=20        # Opcional: destaca mais o título
        )

        st.plotly_chart(fig, use_container_width=True)

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