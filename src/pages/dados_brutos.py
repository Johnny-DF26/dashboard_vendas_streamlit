import streamlit as st
import pandas as pd
import requests


# ==================================================================================================
# Título do Dashboard
# ==================================================================================================
st.set_page_config(layout="wide", page_title='Dashboard de Vendas')
st.title("Dados Brutos", text_alignment='center')

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


with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as colunas', list(dados.columns), list(dados.columns)
    )


st.sidebar.title('Filtros')

with st.sidebar.expander('Nome do Produto'):
    todos_produtos = dados['produto'].unique()

    selecao_produtos = st.multiselect('Selecione os produtos', todos_produtos)
    produtos = selecao_produtos if selecao_produtos else todos_produtos

with st.sidebar.expander('Preco do Produto'):
    preco = st.slider('Selecione o Preço', 0, 5000, (0, 5000))

with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input('Selecione a data de compra', 
                                value=(dados['data_compra'].min(), dados['data_compra'].max()),
                                min_value=dados['data_compra'].min(), 
                                max_value=dados['data_compra'].max())


with st.sidebar.expander('Estado de Compra'):
    # Pegamos a lista de todos os vendedores únicos
    todos_estados = dados['local_compra'].unique()
    # Criamos o multiselect SEM o parâmetro default (ele inicia vazio)
    selecao_estados = st.multiselect('Selecione o Estado', todos_estados)
    # Lógica: se o usuário não selecionou nada, usamos a lista de todos
    estados = selecao_estados if selecao_estados else todos_estados


with st.sidebar.expander('Vendedor'):
    # Pegamos a lista de todos os vendedores únicos
    todos_vendedores = dados['vendedor'].unique()
    # Criamos o multiselect SEM o parâmetro default (ele inicia vazio)
    selecao_vendedor = st.multiselect('Selecione o Vendedor', todos_vendedores)
    # Lógica: se o usuário não selecionou nada, usamos a lista de todos
    vendedor = selecao_vendedor if selecao_vendedor else todos_vendedores

with st.sidebar.expander('Tipo de Pagamento'):
    tipo_pagamento = st.multiselect('Selecione o Tipo de Pagamento', dados['tipo_pagamento'].unique())
    tipo_pagamento = tipo_pagamento if tipo_pagamento else dados['tipo_pagamento'].unique()


with st.sidebar.expander('Limpar Filtros'):
    if st.button('Limpar Filtros'):
        produtos = []
        preco = (0, 5000)
        data_compra = (dados['data_compra'].min(), dados['data_compra'].max())
        estado_compra = ['BR']
        vendedor = todos_vendedores
        tipo_pagamento = []

# ==================================================================================================
# Lógica de Filtragem
# ==================================================================================================

# Aplicando os filtros sequencialmente
query = (
    "produto in @produtos and "
    "@preco[0] <= preco <= @preco[1] and "
    "@data_compra[0] <= data_compra <= @data_compra[1] and "
    "local_compra in @estados and "
    "vendedor in @vendedor and "
    "tipo_pagamento in @tipo_pagamento"
    
)

# Criamos o dataframe filtrado
# O try/except evita erro caso o usuário apague as datas no widget
try:
    dados_filtrados = dados.query(query)
    dados_filtrados = dados_filtrados[colunas] # Aplica seleção de colunas
except:
    st.error("Error ao filtrar os dados. Por favor, tente novamente.")
    dados_filtrados = dados[colunas]

# ==================================================================================================
# Exibição dos Dados
# ==================================================================================================
st.dataframe(dados_filtrados, use_container_width=True)

# Mostra a quantidade de linhas filtradas (Opcional, mas ajuda muito o usuário)
st.markdown(f"Mostrando **{dados_filtrados.shape[0]}** linhas.")