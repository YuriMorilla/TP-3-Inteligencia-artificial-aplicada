"""EduAcesso ESG — Dashboard TP1 (demo)."""

import streamlit as st
import pandas as pd
import plotly.express as px


def fetch_ideb_sample() -> pd.DataFrame:
    data = {
        "municipio": [
            "São Paulo", "Rio de Janeiro", "Manaus", "Fortaleza", "Cuiabá",
            "Campo Grande", "Três Lagoas", "Dourados", "Corumbá", "Ponta Porã",
            "Porto Alegre", "Recife", "Salvador", "Belém", "Goiânia",
        ],
        "uf": ["SP","RJ","AM","CE","MT","MS","MS","MS","MS","MS","RS","PE","BA","PA","GO"],
        "ideb_anos_iniciais": [6.1,5.8,4.9,5.2,5.5,5.7,5.3,5.0,4.6,4.8,6.3,4.7,5.1,4.5,5.6],
        "ideb_anos_finais":   [5.2,4.9,4.1,4.3,4.7,4.8,4.5,4.2,3.8,4.0,5.4,3.9,4.3,3.7,4.8],
        "taxa_abandono_pct":  [1.2,1.8,4.1,3.7,2.3,2.0,2.8,3.2,5.1,4.0,0.9,4.5,3.8,5.6,2.1],
        "escolas_internet_pct":[94,88,71,76,82,85,78,74,61,68,96,72,79,63,87],
        "pib_per_capita":     [52000,41000,23000,18000,29000,31000,28000,22000,19000,21000,43000,17000,20000,16000,33000],
        "ano": [2023]*15,
    }
    return pd.DataFrame(data)


st.set_page_config(page_title="EduAcesso ESG", layout="wide")

st.markdown("""
<style>
    .ods-badge {
        display: inline-block; background: #2e7d5e; color: white;
        border-radius: 20px; padding: 4px 14px; font-size: 13px;
        font-weight: 600; margin-right: 8px;
    }
    .section-title { font-size: 1.1rem; font-weight: 700; color: #1a3c2e; margin-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("EduAcesso ESG")
st.markdown(
    '<span class="ods-badge">ODS 4 — Educação de Qualidade</span>'
    '<span class="ods-badge">ODS 10 — Redução das Desigualdades</span>',
    unsafe_allow_html=True,
)
st.markdown("---")

with st.expander("Problema de Negócio & Objetivos", expanded=True):
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        **Contexto:** O Brasil concentra mais de 4 milhões de crianças fora da escola e apresenta
        profundas desigualdades no acesso à educação de qualidade entre municípios.
        Gestores públicos e ONGs carecem de uma ferramenta analítica integrada para monitorar
        esses indicadores e tomar decisões baseadas em dados.

        **Solução proposta:** Dashboard interativo que consolida indicadores educacionais públicos
        (INEP, IBGE, IDEB) por município, calcula um **Score ESG-Educação** composto e gera
        análises automatizadas via LLM para subsidiar políticas públicas e alocação de recursos.
        """)
    with col2:
        st.markdown("**Metas do projeto:**")
        st.markdown("""
        - ✅ Cobertura ≥ 90% dos municípios BR
        - ✅ Score ESG por município (ranking)
        - ✅ Insights automáticos via LLM
        - ✅ NPS ≥ 8 com usuários-alvo
        """)
        st.markdown("**Público-alvo:**")
        st.markdown("""
        - Gestores municipais de educação
        - ONGs e institutos sociais
        - Pesquisadores e jornalistas de dados
        """)

st.markdown('<p class="section-title"> Fontes e Iniciativas de Referência</p>', unsafe_allow_html=True)
links = {
    "INEP — Dados Abertos": "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos",
    "IBGE — SIDRA API": "https://servicodados.ibge.gov.br/api/docs/agregados",
    "IDEB — Resultados": "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb",
    "ODS 4 — ONU Brasil": "https://brasil.un.org/pt-br/sdgs/4",
    "Conecta Brasil": "https://conectabrasil.org",
    "Observatório do Terceiro Setor": "https://observatorio3setor.org.br",
}
cols = st.columns(3)
for i, (label, url) in enumerate(links.items()):
    cols[i % 3].markdown(f"[ {label}]({url})")

st.markdown("---")
st.markdown('<p class="section-title"> Amostra dos Dados — IDEB & Indicadores Municipais</p>', unsafe_allow_html=True)

df = fetch_ideb_sample()

with st.sidebar:
    st.header("Filtros")
    ufs = ["Todos"] + sorted(df["uf"].unique().tolist())
    uf_sel = st.selectbox("Estado (UF)", ufs)
    st.markdown("---")
    st.markdown("**Fase TDSP atual:** Business Understanding")
    st.markdown("**Metodologia:** CRISP-DM + TDSP")
    st.markdown("**TP:** 1 — Proposta & Planejamento")

df_vis = df[df["uf"] == uf_sel] if uf_sel != "Todos" else df.copy()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Municípios na amostra", len(df_vis))
m2.metric("IDEB médio (anos iniciais)", f"{df_vis['ideb_anos_iniciais'].mean():.1f}")
m3.metric("Taxa abandono média", f"{df_vis['taxa_abandono_pct'].mean():.1f}%")
m4.metric("Escolas c/ internet", f"{df_vis['escolas_internet_pct'].mean():.0f}%")

st.dataframe(
    df_vis.rename(columns={
        "municipio": "Município", "uf": "UF",
        "ideb_anos_iniciais": "IDEB Iniciais", "ideb_anos_finais": "IDEB Finais",
        "taxa_abandono_pct": "Abandono (%)", "escolas_internet_pct": "Internet (%)",
        "pib_per_capita": "PIB per capita (R$)", "ano": "Ano",
    }),
    use_container_width=True, hide_index=True,
)

st.markdown('<p class="section-title"> IDEB por Município</p>', unsafe_allow_html=True)
fig = px.bar(
    df_vis.sort_values("ideb_anos_iniciais", ascending=True),
    x="ideb_anos_iniciais", y="municipio", orientation="h", color="uf",
    labels={"ideb_anos_iniciais": "IDEB (Anos Iniciais)", "municipio": "Município"},
    color_discrete_sequence=px.colors.qualitative.Set2, height=400,
)
fig.update_layout(showlegend=True, plot_bgcolor="white", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

st.markdown('<p class="section-title"> PIB per capita × IDEB (Anos Iniciais)</p>', unsafe_allow_html=True)
fig2 = px.scatter(
    df_vis, x="pib_per_capita", y="ideb_anos_iniciais",
    size="escolas_internet_pct", color="taxa_abandono_pct", hover_name="municipio",
    labels={"pib_per_capita": "PIB per capita (R$)", "ideb_anos_iniciais": "IDEB (Anos Iniciais)",
            "taxa_abandono_pct": "Abandono (%)", "escolas_internet_pct": "% Internet"},
    color_continuous_scale="RdYlGn_r", height=420,
)
fig2.update_layout(plot_bgcolor="white")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("Dados de amostra para demonstração (TP1). Fontes: INEP/IDEB, IBGE.")
