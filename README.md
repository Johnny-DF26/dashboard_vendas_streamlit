# DASHBOARD DE VENDAS

Resumo
-------
Dashboard interativo em Streamlit para análise de vendas por produto, categoria, vendedor e região. Inclui KPIs, gráficos interativos (Plotly), mapas e uma página para inspeção de dados brutos.

Recursos principais
-------------------
- KPIs financeiros e contagem de vendas
- Visualizações: séries temporais, barras, mapas e rankings
- Filtros dinâmicos (região, ano, vendedor, data, preço, avaliação)
- Paginação/visualização dos dados brutos com filtros avançados
- Caching de dados com `st.cache_data` para reduzir latência

Requisitos
---------
- Python 3.8+
- Dependências listadas em `requirements.txt`

Instalação
---------
1. Clone o repositório:

```bash
git clone https://github.com/Johnny-DF26/Streamlit.git
cd Streamlit
```

2. Crie e ative um ambiente virtual (exemplo Windows):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

Execução
--------
Inicie o app:

```bash
streamlit run src/dashboard.py
```

Abra a URL exibida pelo Streamlit (por padrão http://localhost:8501).

Estrutura do repositório
------------------------

- `README.md` — Documentação do projeto
- `requirements.txt` — Dependências Python
- `src/dashboard.py` — Entrada do app e composição principal
- `src/formatacao.py` — Funções utilitárias para formatação e KPIs
- `src/graficos.py` — Funções que geram gráficos (Plotly)
- `src/pages/dados_brutos.py` — Página para visualização dos dados brutos e filtros

Fonte de dados
--------------
Os dados são carregados a partir do endpoint público `https://labdados.com/produtos`. A preparação do DataFrame (renomeação de colunas, conversão de datas) é feita nas funções de carregamento dentro de `src/`.

Como contribuir
---------------
1. Abra uma issue descrevendo a proposta ou bug.
2. Crie uma branch com prefixo `feat/` ou `fix/`.
3. Faça commits pequenos e claros.
4. Abra um Pull Request descrevendo as mudanças e como testar.

Sugestões de melhorias
----------------------
- Adicionar CI (GitHub Actions) para lint e testes
- Incluir `CONTRIBUTING.md` e `CODE_OF_CONDUCT.md`
- Publicar badges (build, coverage) no topo do README

Checklist antes de PR
---------------------
- Código formatado (ex.: `black`)
- Dependências atualizadas em `requirements.txt`
- Testes ou validações manuais descritas no PR

Licença
-------
Uso livre para fins educacionais e pessoais.

