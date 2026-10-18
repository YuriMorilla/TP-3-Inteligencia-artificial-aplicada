import streamlit as st

import common
from src.data import store

common.init_state()
common.header("EduAcesso ESG")

df = st.session_state.base_df
news, news_live = common.load_news_source()
corpus = common.load_corpus()

st.write(
    "Dashboard analítico para monitorar indicadores educacionais municipais com foco em "
    "equidade (ODS 4). Use o menu lateral para navegar entre as seções."
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros na base", len(df))
c2.metric("Municípios", df["municipio"].nunique())
c3.metric("Notícias coletadas", len(news))
c4.metric("Documentos p/ LLM", len(corpus))

common.section("O que cada página faz")
st.markdown(
    """
| Página | Função |
|---|---|
| 📊 **Indicadores** | Filtros dinâmicos, tabela e gráficos interativos (IDEB, abandono, internet, PIB) |
| 📰 **Notícias & Nuvem de Palavras** | Conteúdo coletado com Beautiful Soup: wordcloud, frequência de termos e notícias |
| 📤 **Upload / Download** | Envio de CSV complementar e download da base |
| 🔌 **API FastAPI** | Documentação das rotas e testador (GET/POST) |
| 🤖 **Preparação para LLM** | Corpus unificado, tarefas planejadas, prompts e recuperação de contexto |
"""
)

api_rows = len(store.load_api_records())
st.caption(
    f"Fontes: IDEB/IBGE (amostra), Wikipédia e Google News via Beautiful Soup"
    f"{'' if news_live else ' (usando amostra — rode src/data/scrape_web.py)'}; "
    f"{api_rows} registro(s) enviados pela API."
)
