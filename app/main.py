"""EduAcesso ESG — ponto de entrada do app (TP3).

Define o menu de navegação multipágina. Rodar com:
    streamlit run app/main.py
"""

import streamlit as st

st.set_page_config(page_title="EduAcesso ESG", page_icon="🎓", layout="wide")

pages = {
    "Visão geral": [
        st.Page("views/home.py", title="Início", icon="🏠", default=True),
    ],
    "Análises": [
        st.Page("views/indicadores.py", title="Indicadores", icon="📊"),
        st.Page("views/noticias.py", title="Notícias & Nuvem de Palavras", icon="📰"),
    ],
    "Dados & API": [
        st.Page("views/dados.py", title="Upload / Download", icon="📤"),
        st.Page("views/api.py", title="API FastAPI", icon="🔌"),
    ],
    "Inteligência Artificial": [
        st.Page("views/llm.py", title="Preparação para LLM", icon="🤖"),
    ],
}

st.sidebar.caption("EduAcesso ESG · TP3 · CRISP-DM + TDSP")
st.navigation(pages).run()
