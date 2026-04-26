import streamlit as st
from pages.dataframe import dados
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

qtd_vendas_estado = dados.groupby('local_compra')[['preco', 'lat', 'long']].agg({'preco': 'count', 'lat': 'mean', 'long': 'mean'})
qtd_vendas_estado = qtd_vendas_estado.sort_values(by='preco', ascending=False).reset_index()

categoria_mais_vendida = dados.groupby('categoria')[['preco']].agg({'preco': 'count'})
categoria_mais_vendida = categoria_mais_vendida.sort_values(by='preco', ascending=True).reset_index()


produtos_mais_vendidos = dados.groupby('produto').agg({'preco': 'count'}).sort_values(by='preco', ascending=False).reset_index()
tipo_pagamento_mais_utilizado = dados.groupby('tipo_pagamento').agg({'preco': 'count'}).sort_values(by='preco', ascending=False).reset_index()
periodo_mais_vendido = dados.groupby(dados['data_compra'].dt.to_period('M')).agg({'preco': 'count'}).sort_values(by='data_compra').reset_index()

st.write(dados)
st.write(qtd_vendas_estado)
st.write(categoria_mais_vendida)
st.write(produtos_mais_vendidos)
st.write(tipo_pagamento_mais_utilizado)
st.write(periodo_mais_vendido)


def figura1():
    sns.set_theme()
    fig1, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=qtd_vendas_estado.head(10), x='local_compra', y='preco', ax=ax)
    ax.set_title('Quantidade de Vendas por Estado', loc='left', fontsize=18, fontweight='bold')
    ax.set_ylim(0, qtd_vendas_estado['preco'].max() * 1.1)
    ax.set_xlabel('Estado')
    ax.set_ylabel('Quantidade de Vendas')

    for p in ax.patches:
        label = f'{p.get_height():.0f}'
        ax.annotate(label, (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
    
    return fig1

def figura2():
    fig2 = px.scatter_mapbox(
            qtd_vendas_estado,
            lat="lat",
            lon="long",
            size="preco",
            color="preco",
            hover_name="local_compra",
            zoom=3,
            title="Distribuição de Vendas por Estado",
            mapbox_style="open-street-map",
            color_continuous_scale="Jet"
        )
    # AJUSTE DE CORES DO LAYOUT
    fig2.update_layout(
        #title={'text': "<b>Distribuição de Vendas por Estado</b>", 'x': 0.5}, # Título centralizado e em negrito
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor="white",    # Cor da área externa (lateral/fundo)
        plot_bgcolor="white",     # Cor da área interna
        font_color="black",       # Cor do título e legendas
        title_font_size=20,       # Opcional: destaca mais o título
        coloraxis_showscale=True
    )

    return fig2
    

def figura3():
    fig3, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=categoria_mais_vendida.head(10),
                y='categoria',
                x='preco',
                orient='h',
                ax=ax)
    ax.set_title('Categorias Mais Vendidas', loc='left', fontsize=18, fontweight='bold')
    ax.set_xlabel('Quantidade de Vendas')
    ax.set_ylabel('Categoria')
    return fig3
    
