import streamlit as st
import pandas as pd
import requests
from pages.graph import grafico_mapa, grafico_linhas, grafico_barras, formata_numero
from pages.dataframe import dados
import plotly.express as px

vendedores = pd.DataFrame(dados.groupby('vendedor')['preco'].agg(['sum', 'count']))

def grafico_vendedores(qtd_vendedores, tipo='sum'):
    vend = vendedores[tipo].sort_values(ascending=False).head(qtd_vendedores)

    fig_vendedores = px.bar(vend,
                            x= tipo,
                            y= vend.index,
                            text_auto=True,
                            title= f'Top {qtd_vendedores} Vendedores por Receita',
                            template='seaborn',
                            color=vend.index,
                            color_continuous_scale='spectral')
    
    fig_vendedores.update_xaxes(title='Receita (R$)')
    fig_vendedores.update_yaxes(title='Vendedor')
    fig_vendedores.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_vendedores, use_container_width=True)
