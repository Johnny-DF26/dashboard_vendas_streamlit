import streamlit as st
import pandas as pd
import requests
from pages.graph import grafico_mapa, grafico_linhas, grafico_barras, formata_numero
from pages.dataframe import dados

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
def graficos_coluna1():
    # Apenas execute os comandos. Não precisa de return.
    st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
    
    fig_mapa = grafico_mapa(receita_estados, 'Receita Total por Estado', 'Receita')
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    fig_barras = grafico_barras(receita_estados.head(), 'Receita de Vendas por Estado', 'Estado', 'Receita')
    st.plotly_chart(fig_barras, use_container_width=True)

    
def graficos_coluna2():
    
    st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))

    fig_linhas = grafico_linhas(receita_mensal, 'Receita Mensal por Categoria','mes','preco')
    st.plotly_chart(fig_linhas, use_container_width=True)

    fig_barras = grafico_barras(receita_categoria, 'Receita por Categoria','preco','categoria','h')
    st.plotly_chart(fig_barras, use_container_width=True)