# 📊 DASHBOARD DE VENDAS

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/plotly-3F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly Dash">
</p>


### 📝 Resumo
Dashboard interativo desenvolvido em **Streamlit** para análise detalhada de vendas por produto, categoria, vendedor e região. O projeto foca em fornecer insights rápidos através de KPIs, gráficos interativos e mapeamento geográfico.

### ✨ Recursos principais
* ✅ **KPIs Financeiros:** Visualização imediata de faturamento e contagem de vendas.
* 📈 **Visualizações Ricas:** Séries temporais, gráficos de barras, mapas de calor e rankings.
* 🎛️ **Filtros Dinâmicos:** Refine os dados por região, ano, vendedor, data, preço e avaliação.
* 🔍 **Inspeção de Dados:** Página dedicada para visualização de dados brutos com filtros avançados.
* ⚡ **Alta Performance:** Uso de `st.cache_data` para carregamento otimizado e baixa latência.

### 🛠️ Requisitos
* Python 3.8+
* Dependências listadas em `requirements.txt`

### 🚀 Instalação
1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd Streamlit
   ```
2. **Crie e ative um ambiente virtual (Windows):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### 🔗 Demonstração Online
O dashboard está publicado e pode ser acessado em tempo real:
👉 [**Acesse o Streamlit App aqui**] ([https://github.com](https://dashboardvendasapp-alura.streamlit.app/)

> *Nota: Caso o link não abra imediatamente, o Streamlit pode estar "acordando" o servidor. Aguarde alguns segundos.*

### 💻 Execução
Inicie o app localmente:
```bash
streamlit run src/dashboard.py
```
Abra a URL exibida (padrão: `http://localhost:8501`).

### 📂 Estrutura do Repositório
* `README.md` — Documentação do projeto.
* `requirements.txt` — Dependências Python.
* `src/dashboard.py` — Ponto de entrada e composição do app.
* `src/formatacao.py` — Utilitários para formatação e cálculos de KPIs.
* `src/graficos.py` — Lógica de geração dos gráficos (Plotly).
* `src/pages/dados_brutos.py` — Interface de filtros e tabelas brutas.

### 💾 Fonte de Dados
Os dados são consumidos via API do endpoint público [://labdados.com](https://://labdados.com). O tratamento (limpeza, renomeação e conversão) ocorre durante o carregamento no diretório `src/`.

### 🤝 Como contribuir
1. Abra uma **Issue** relatando o problema ou sugestão.
2. Crie uma branch: `git checkout -b feat/minha-melhoria`.
3. Faça o commit: `git commit -m 'Adiciona nova funcionalidade'`.
4. Abra um **Pull Request**.

### ⚖️ Licença
Uso livre para fins educacionais e pessoais.
