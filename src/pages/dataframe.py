
"""
Módulo responsável pelo carregamento e preparação dos dados para o Dashboard de Vendas.
Os dados são obtidos via API e tratados para uso nas análises e gráficos.
"""

import requests
import pandas as pd

# ==================================================================================================
# Carregamento dos dados da API
# ==================================================================================================
url = "https://labdados.com/produtos"
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados.columns = [
    'produto', 'categoria', 'preco', 'frete', 'data_compra', 'vendedor',
    'local_compra', 'avaliacao', 'tipo_pagamento', 'parcelas', 'lat', 'long'
]
# Converte a coluna de data para o formato datetime
dados['data_compra'] = pd.to_datetime(dados['data_compra'], format='%d/%m/%Y')