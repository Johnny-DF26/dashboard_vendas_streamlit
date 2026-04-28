
"""
Módulo utilitário para formatação de números e exibição de KPIs no Dashboard de Vendas.
Inclui funções para formatar valores e mostrar métricas no Streamlit.
"""

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

