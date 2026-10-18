import os

import requests
import streamlit as st

import common

common.init_state()
common.header("API FastAPI")

st.write("A API expõe os mesmos dados do dashboard. Para subir localmente (na raiz do projeto):")
st.code("uvicorn api.main:app --reload", language="bash")
st.caption("Documentação interativa (Swagger): `/docs`")

common.section("Rotas")
st.markdown(
    """
| Método | Rota | Função |
|---|---|---|
| GET | `/municipios` | Lista indicadores (filtros `uf`, `ano`, `ideb_min`, `limit`) |
| GET | `/municipios/{nome}` | Consulta um município (ignora acentos/maiúsculas) |
| POST | `/municipios` | Envia novo registro (validado; 409 se duplicado) |
| GET | `/estatisticas` | Agregados gerais e por UF |
| GET | `/noticias` | Notícias coletadas com Beautiful Soup |
| GET | `/corpus` | Documentos preparados para tarefas de LLM |
"""
)

common.section("Testador")
base_url = st.text_input("URL da API", os.getenv("EDUACESSO_API_URL", "http://localhost:8000")).rstrip("/")


def chamar(method: str, path: str, **kwargs):
    try:
        resp = requests.request(method, f"{base_url}{path}", timeout=10, **kwargs)
    except requests.RequestException:
        st.warning("API fora do ar neste endereço. Suba com `uvicorn api.main:app --reload` e tente de novo.")
        return
    (st.success if resp.ok else st.error)(f"HTTP {resp.status_code}")
    st.json(resp.json())


tab_get, tab_post = st.tabs(["GET /municipios", "POST /municipios"])
with tab_get:
    uf = st.text_input("UF (opcional)", max_chars=2)
    ideb_min = st.number_input("IDEB mínimo", 0.0, 10.0, 0.0, 0.1)
    if st.button("Consultar"):
        params = {"ideb_min": ideb_min, **({"uf": uf} if uf else {})}
        chamar("GET", "/municipios", params=params)

with tab_post:
    with st.form("novo_municipio"):
        c1, c2, c3 = st.columns(3)
        municipio = c1.text_input("Município")
        uf_n = c2.text_input("UF", max_chars=2)
        ano = c3.number_input("Ano", 2000, 2100, 2024)
        i1 = c1.number_input("IDEB anos iniciais", 0.0, 10.0, 5.0, 0.1)
        i2 = c2.number_input("IDEB anos finais", 0.0, 10.0, 4.0, 0.1)
        ab = c3.number_input("Abandono (%)", 0.0, 100.0, 3.0, 0.1)
        net = c1.number_input("Escolas com internet (%)", 0.0, 100.0, 70.0, 1.0)
        pib = c2.number_input("PIB per capita (R$)", 0.0, 1_000_000.0, 25000.0, 1000.0)
        enviado = st.form_submit_button("Enviar")
    if enviado:
        chamar("POST", "/municipios", json={
            "municipio": municipio, "uf": uf_n, "ideb_anos_iniciais": i1, "ideb_anos_finais": i2,
            "taxa_abandono_pct": ab, "escolas_internet_pct": net, "pib_per_capita": pib, "ano": int(ano)})
        st.caption("Registros enviados aparecem em Upload / Download após \"Recarregar base\".")
