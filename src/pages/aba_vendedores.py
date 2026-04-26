
"""
Módulo de gráficos para análise de vendedores no Dashboard de Vendas.

Contém função para exibir ranking dos melhores vendedores por receita ou quantidade de vendas.
"""

import streamlit as st
import pandas as pd
from pages.dataframe import dados
import plotly.express as px

# Agrupa os dados por vendedor, calculando soma e contagem de vendas
vendedores = pd.DataFrame(dados.groupby('vendedor')['preco'].agg(['sum', 'count']))

def grafico_vendedores(qtd_vendedores, tipo='sum') -> None:
    """
    Exibe um gráfico de barras com os top vendedores por receita ou quantidade de vendas.

    Args:
        qtd_vendedores (int): Quantidade de vendedores a exibir no ranking.
        tipo (str): 'sum' para receita, 'count' para quantidade de vendas.
    """
    # Seleciona os top vendedores conforme o critério
    vend = vendedores[tipo].sort_values(ascending=False).head(qtd_vendedores)

    fig_vendedores = px.bar(
        vend,
        x=tipo,
        y=vend.index,
        text_auto=True,
        title=f'Top {qtd_vendedores} Vendedores por Receita' if tipo=='sum' else f'Top {qtd_vendedores} Vendedores por Quantidade',
        template='seaborn',
        color=vend.index,
        color_continuous_scale='spectral'
    )
    
    fig_vendedores.update_xaxes(title='Receita (R$)' if tipo=='sum' else 'Quantidade de Vendas')
    fig_vendedores.update_yaxes(title='Vendedor')
    fig_vendedores.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_vendedores, use_container_width=True)
