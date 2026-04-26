import streamlit as st
from pages.dataframe import dados

def formata_numero(numero, casas_decimais=2):
    
    if numero >= 1e6:
        return f"{round(numero / 1e6, casas_decimais)}Mi"
    elif numero >= 1e3:
        return f"{round(numero / 1e3, casas_decimais)}Mil"
    else:
        return f"{numero}"
    
def get_receita():
    receita = dados['preco'].sum()
    receita_total = st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
    return receita_total

def get_qtd_vendas():
    qtd_vendas = dados.shape[0]
    qtd_vendas_total = st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))
    return qtd_vendas_total