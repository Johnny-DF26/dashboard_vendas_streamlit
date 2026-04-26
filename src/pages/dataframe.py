import requests
import pandas as pd

# ==================================================================================================
# Carregamento dos dados
# ==================================================================================================
url = "https://labdados.com/produtos"
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados.columns = ['produto', 'categoria','preco', 'frete', 'data_compra', 'vendedor',
                 'local_compra', 'avaliacao', 'tipo_pagamento', 'parcelas', 'lat', 'long']
dados['data_compra'] = pd.to_datetime(dados['data_compra'], format='%d/%m/%Y')