
"""
Módulo utilitário para formatação de números e exibição de KPIs no Dashboard de Vendas.
Inclui funções para formatar valores e mostrar métricas no Streamlit.
"""

import streamlit as st
from pages.dataframe import dados

def formata_numero(numero, casas_decimais=2) -> str:
    """
    Formata um número para exibição compacta (Mil, Mi).

    Args:
        numero (float): Valor a ser formatado.
        casas_decimais (int): Casas decimais para arredondamento.

    Returns:
        str: Número formatado como string.
    """
    if numero >= 1e6:
        return f"{round(numero / 1e6, casas_decimais)}Mi"
    elif numero >= 1e3:
        return f"{round(numero / 1e3, casas_decimais)}Mil"
    else:
        return f"{numero}"

def get_receita() -> st.delta_generator.DeltaGenerator:
    """
    Exibe o KPI de receita total no Streamlit.

    Returns:
        streamlit.delta_generator.DeltaGenerator: Objeto de métrica exibida.
    """
    receita = dados['preco'].sum()
    receita_total = st.metric('Receita', f'R$ {formata_numero(receita, casas_decimais=2)}')
    return receita_total

def get_qtd_vendas() -> st.delta_generator.DeltaGenerator:
    """
    Exibe o KPI de quantidade total de vendas no Streamlit.

    Returns:
        streamlit.delta_generator.DeltaGenerator: Objeto de métrica exibida.
    """
    qtd_vendas = dados.shape[0]
    qtd_vendas_total = st.metric('Quantidade de Vendas', formata_numero(qtd_vendas, casas_decimais=2))
    return qtd_vendas_total