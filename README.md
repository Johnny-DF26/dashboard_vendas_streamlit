# Dashboard de Vendas

Um dashboard interativo desenvolvido em **Streamlit** para análise de vendas, receitas, desempenho de vendedores e visualização de dados geográficos e temporais.

## Funcionalidades

- **KPIs de Receita e Quantidade de Vendas**
- **Gráficos Interativos**: Linha, barras e mapas com Plotly
- **Análise por Estado, Categoria e Vendedor**
- **Seleção dinâmica de quantidade de vendedores**
- **Visualização de dados em abas temáticas**

## Estrutura do Projeto

```
src/
  dashboard.py           # Arquivo principal do dashboard
  pages/
    aba_receita.py       # Gráficos e KPIs de receita
    aba_vendas.py        # (Vazio, pode ser expandido)
    aba_vendedores.py    # Gráficos de desempenho dos vendedores
    dataframe.py         # Carregamento e tratamento dos dados
    formatacao.py        # Funções utilitárias de formatação e KPIs
requirements.txt         # Dependências do projeto
```

## Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Johnny-DF26/Streamlit.git
   cd Streamlit
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## Como Executar

No diretório raiz do projeto, execute:
```bash
streamlit run src/dashboard.py
```

## Principais Bibliotecas

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Seaborn](https://seaborn.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Requests](https://docs.python-requests.org/)

## Fonte dos Dados

Os dados são carregados automaticamente via API:
- `https://labdados.com/produtos`

## Estrutura das Abas

- **Receita**: Gráficos de linha, barras e mapa de calor por estado.
- **Quantidade de Vendas**: KPIs e gráficos de vendas.
- **Vendedores**: Ranking dos melhores vendedores por receita e quantidade.

## Personalização

- O número de vendedores exibidos pode ser ajustado dinamicamente.
- O dashboard pode ser expandido facilmente adicionando novas páginas em `src/pages/`.

## Licença

Este projeto é livre para uso educacional e pessoal.
