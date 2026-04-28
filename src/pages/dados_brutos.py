"""Página que exibe os dados brutos e controles de filtragem.

Este módulo carrega os dados a partir de uma API externa, expõe widgets de
filtro no `sidebar` e apresenta a tabela filtrada e estatísticas resumidas.

Principais responsabilidades:
    - `carregar_dados`: buscar e preparar o DataFrame com caching do Streamlit.
    - Widgets de filtro: seleção de produtos, preço, avaliação, data, estado,
        vendedor e tipo de pagamento.
    - Construção de uma query para filtrar o DataFrame e exibição das estatísticas.

Dependências: streamlit, pandas, requests
"""

import streamlit as st
import pandas as pd
import requests

# ==================================================================================================
# Título do Dashboard
# ==================================================================================================
# Configurações da página Streamlit (layout e título)
st.set_page_config(layout="wide", page_title='Dados Brutos')
st.title("Dados Brutos 🎲".upper(), text_alignment='center')

# ==================================================================================================
# Carregamento dos dados da API
# ==================================================================================================
@st.cache_data  # Cachea o resultado para evitar múltiplas requisições à API
def carregar_dados() -> pd.DataFrame:
    """Faz requisição à API externa e retorna um DataFrame preparado.

    A função realiza uma chamada HTTP GET para obter os dados brutos, renomeia
    as colunas para nomes amigáveis e converte a coluna de datas para
    `datetime`.

    Returns:
        pandas.DataFrame: DataFrame com colunas renomeadas e `data_compra` em
        formato datetime.
    """
    url = "https://labdados.com/produtos"
    response = requests.get(url)
    dados = pd.DataFrame.from_dict(response.json())

    dados.columns = [
        'produto', 'categoria', 'preco', 'frete', 'data_compra', 'vendedor',
        'local_compra', 'avaliacao', 'tipo_pagamento', 'parcelas', 'lat', 'long'
    ]
    # Normaliza formato de data para permitir manipulações temporais
    dados['data_compra'] = pd.to_datetime(dados['data_compra'], format='%d/%m/%Y')
    return dados

# Para usar, basta chamar a função
dados = carregar_dados()


with st.expander('Colunas'):
    # Permite ao usuário escolher quais colunas exibir na tabela
    colunas = st.multiselect(
        'Selecione as colunas', list(dados.columns), list(dados.columns)
    )


st.sidebar.title('Filtros :arrow_down_small:')

with st.sidebar.expander(':shopping_cart: Nome do Produto '):
    todos_produtos = dados['produto'].unique()
    selecao_produtos = st.multiselect('Selecione os produtos', todos_produtos)
    produtos = selecao_produtos if selecao_produtos else todos_produtos

with st.sidebar.expander(':moneybag: Preco do Produto '):
    preco = st.slider('Selecione o Preço', 0, 5000, (0, 5000))

with st.sidebar.expander(':star: Avaliação do Produto '):
    # Opcional: Adicionar um checkbox para "Mostrar Todos"
    todos = st.checkbox('Mostrar todas as avaliações', value=True)
    val_selecionado = st.slider('Selecione a Avaliação', 0, 5, 5)
    if todos:
        avaliacao = (0, 5) # Se "Todos" marcar, o range é total
    else:
        avaliacao = (val_selecionado, val_selecionado) # Se escolher 3, vira (3, 3)

with st.sidebar.expander(':calendar: Data da Compra '):
    data_compra = st.date_input('Selecione a data de compra', 
                                value=(dados['data_compra'].min(), dados['data_compra'].max()),
                                min_value=dados['data_compra'].min(), 
                                max_value=dados['data_compra'].max())

with st.sidebar.expander(':triangular_flag_on_post: Estados'):
    # Pegamos a lista de todos os vendedores únicos
    todos_estados = dados['local_compra'].unique()
    # Criamos o multiselect SEM o parâmetro default (ele inicia vazio)
    selecao_estados = st.multiselect('Selecione o Estado', todos_estados)
    # Lógica: se o usuário não selecionou nada, usamos a lista de todos
    estados = selecao_estados if selecao_estados else todos_estados

with st.sidebar.expander(':man: Vendedor'):
    # Pegamos a lista de todos os vendedores únicos
    todos_vendedores = dados['vendedor'].unique()
    # Criamos o multiselect SEM o parâmetro default (ele inicia vazio)
    selecao_vendedor = st.multiselect('Selecione o Vendedor', todos_vendedores)
    # Lógica: se o usuário não selecionou nada, usamos a lista de todos
    vendedor = selecao_vendedor if selecao_vendedor else todos_vendedores

with st.sidebar.expander(':credit_card: Tipo de Pagamento'):
    tipo_pagamento = st.multiselect('Selecione o Tipo de Pagamento', dados['tipo_pagamento'].unique())
    tipo_pagamento = tipo_pagamento if tipo_pagamento else dados['tipo_pagamento'].unique()

# ==================================================================================================
# Lógica de Filtragem
# ==================================================================================================
# Construção da query para filtrar o DataFrame usando pandas.DataFrame.query.
# As variáveis com @ (ex: @produtos) fazem referência ao escopo local.
query = (
    "produto in @produtos and "
    "@preco[0] <= preco <= @preco[1] and "
    "@avaliacao[0] <= avaliacao <= @avaliacao[1] and "
    "@data_compra[0] <= data_compra <= @data_compra[1] and "
    "local_compra in @estados and "
    "vendedor in @vendedor and "
    "tipo_pagamento in @tipo_pagamento"
)

# Aplicamos a query ao DataFrame. Usamos try/except para capturar possíveis
# erros de avaliação (por exemplo, se o usuário limpar os filtros de data).
try:
    dados_filtrados = dados.query(query)
    dados_filtrados = dados_filtrados[colunas]  # Aplica seleção de colunas
except Exception:
    st.error("Error ao filtrar os dados. Por favor, tente novamente.")
    dados_filtrados = dados[colunas]

# ==================================================================================================
# Exibição dos Dados
# ==================================================================================================
st.subheader(':date: Tabela de Dados ')
st.dataframe(dados_filtrados, use_container_width=True)

# Exibe a quantidade de linhas resultantes após filtragem
st.markdown(f"Mostrando :red[**{dados_filtrados.shape[0]}**]:red linhas.")


# ==================================================================================================
# Estatísticas
# ==================================================================================================
# Cálculo de estatísticas resumidas a partir do DataFrame filtrado
produto_mais_vendido = dados_filtrados['produto'].mode().tolist()
produto_mais_vendido = ", ".join(produto_mais_vendido)

categoria_mais_vendida = dados_filtrados['categoria'].mode().tolist()
categoria_mais_vendida = ", ".join(categoria_mais_vendida)

# Soma das vendas formatada em BRL (troca de separadores para padrão brasileiro)
soma_vendas = dados_filtrados['preco'].sum()
soma_vendas = f'{soma_vendas:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',')

avaliacao = dados_filtrados['avaliacao'].mean()
avaliacao = f'{avaliacao:,.2f}'

tipo_de_pagamento = dados_filtrados['tipo_pagamento'].mode().tolist()
tipo_de_pagamento = ", ".join(tipo_de_pagamento).replace('_', ' ')

st.subheader(':bar_chart: Estatísticas')
tabela_estatistica = pd.DataFrame({
    'Produto Mais Vendido': [produto_mais_vendido],
    'Categoria Mais Vendida': [categoria_mais_vendida],
    'Soma das Vendas': [soma_vendas],
    'Média Avaliacao': [avaliacao],
    'Forma de Pagamento mais utilizada': [tipo_de_pagamento]
})

st.table(tabela_estatistica)