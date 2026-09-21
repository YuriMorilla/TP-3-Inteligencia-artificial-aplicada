"""EduAcesso ESG — Dashboard TP2.

Evolução do TP1: interface dinâmica em abas, cache e estado de sessão,
extração de conteúdo web (Beautiful Soup) para nuvem de palavras e tabela
de notícias, e serviço de upload/download de arquivos CSV.
"""

from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

STOPWORDS_PT = {
    "a", "o", "e", "de", "do", "da", "em", "um", "uma", "os", "as", "dos", "das",
    "no", "na", "nos", "nas", "para", "com", "por", "que", "se", "ao", "aos", "à",
    "às", "é", "são", "foi", "ser", "sua", "seu", "suas", "seus", "mais", "como",
    "entre", "este", "esta", "isso", "essa", "esse", "pelo", "pela", "também",
    "já", "não", "sobre", "mas", "ou", "há", "cada", "the", "of", "and", "in",
}

# ---------------------------------------------------------------------------
# Camada de dados (cacheada)
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def fetch_ideb_sample() -> pd.DataFrame:
    """Amostra estática do IDEB (mesma base do TP1)."""
    data = {
        "municipio": [
            "São Paulo", "Rio de Janeiro", "Manaus", "Fortaleza", "Cuiabá",
            "Campo Grande", "Três Lagoas", "Dourados", "Corumbá", "Ponta Porã",
            "Porto Alegre", "Recife", "Salvador", "Belém", "Goiânia",
        ],
        "uf": ["SP", "RJ", "AM", "CE", "MT", "MS", "MS", "MS", "MS", "MS", "RS", "PE", "BA", "PA", "GO"],
        "ideb_anos_iniciais": [6.1, 5.8, 4.9, 5.2, 5.5, 5.7, 5.3, 5.0, 4.6, 4.8, 6.3, 4.7, 5.1, 4.5, 5.6],
        "ideb_anos_finais": [5.2, 4.9, 4.1, 4.3, 4.7, 4.8, 4.5, 4.2, 3.8, 4.0, 5.4, 3.9, 4.3, 3.7, 4.8],
        "taxa_abandono_pct": [1.2, 1.8, 4.1, 3.7, 2.3, 2.0, 2.8, 3.2, 5.1, 4.0, 0.9, 4.5, 3.8, 5.6, 2.1],
        "escolas_internet_pct": [94, 88, 71, 76, 82, 85, 78, 74, 61, 68, 96, 72, 79, 63, 87],
        "pib_per_capita": [52000, 41000, 23000, 18000, 29000, 31000, 28000, 22000, 19000, 21000, 43000, 17000, 20000, 16000, 33000],
        "ano": [2023] * 15,
    }
    return pd.DataFrame(data)


@st.cache_data(show_spinner=False)
def load_text_source() -> tuple[str, bool]:
    """Carrega o texto coletado da web; usa amostra se o scraper não rodou."""
    real = RAW_DIR / "wiki_educacao.txt"
    sample = RAW_DIR / "wiki_educacao_sample.txt"
    if real.exists() and real.stat().st_size > 0:
        return real.read_text(encoding="utf-8"), True
    return sample.read_text(encoding="utf-8"), False


@st.cache_data(show_spinner=False)
def load_news_source() -> tuple[pd.DataFrame, bool]:
    """Carrega a tabela de notícias coletada; usa amostra se o scraper não rodou."""
    real = RAW_DIR / "noticias_educacao.csv"
    sample = RAW_DIR / "noticias_educacao_sample.csv"
    if real.exists() and real.stat().st_size > 0:
        return pd.read_csv(real), True
    return pd.read_csv(sample), False


@st.cache_data(show_spinner=False)
def word_frequencies(text: str, top_n: int = 20) -> pd.DataFrame:
    """Estatística básica: frequência das palavras mais comuns do texto."""
    words = [w.lower().strip(".,;:!?()\"'") for w in text.split()]
    words = [w for w in words if len(w) > 2 and w not in STOPWORDS_PT]
    freq = Counter(words).most_common(top_n)
    return pd.DataFrame(freq, columns=["palavra", "frequência"])


@st.cache_resource(show_spinner=False)
def build_wordcloud(text: str):
    """Gera o objeto WordCloud (cacheado como recurso — é custoso de montar)."""
    return WordCloud(
        width=900, height=420, background_color="white",
        stopwords=STOPWORDS_PT, colormap="Greens", collocations=False,
    ).generate(text)


# ---------------------------------------------------------------------------
# Estado de sessão
# ---------------------------------------------------------------------------

if "base_df" not in st.session_state:
    st.session_state.base_df = fetch_ideb_sample()
if "uploads_count" not in st.session_state:
    st.session_state.uploads_count = 0

REQUIRED_COLUMNS = [
    "municipio", "uf", "ideb_anos_iniciais", "ideb_anos_finais",
    "taxa_abandono_pct", "escolas_internet_pct", "pib_per_capita", "ano",
]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

st.set_page_config(page_title="EduAcesso ESG", layout="wide")

st.markdown(
    """
    <style>
        .ods-badge {
            display: inline-block; background: #2e7d5e; color: white;
            border-radius: 20px; padding: 4px 14px; font-size: 13px;
            font-weight: 600; margin-right: 8px;
        }
        .section-title { font-size: 1.1rem; font-weight: 700; color: #1a3c2e; margin-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("EduAcesso ESG")
st.markdown(
    '<span class="ods-badge">ODS 4 — Educação de Qualidade</span>'
    '<span class="ods-badge">ODS 10 — Redução das Desigualdades</span>',
    unsafe_allow_html=True,
)
st.caption("TP2 — Ambiente configurado, interface dinâmica, coleta web e upload/download de dados.")
st.markdown("---")

with st.sidebar:
    st.header("Filtros")
    df_all = st.session_state.base_df

    ufs = sorted(df_all["uf"].unique().tolist())
    uf_sel = st.multiselect("Estado (UF)", ufs, default=ufs, key="uf_filter")

    ideb_min, ideb_max = float(df_all["ideb_anos_iniciais"].min()), float(df_all["ideb_anos_iniciais"].max())
    ideb_range = st.slider(
        "Faixa de IDEB (anos iniciais)", min_value=ideb_min, max_value=ideb_max,
        value=(ideb_min, ideb_max), step=0.1, key="ideb_filter",
    )

    st.markdown("---")
    st.markdown("**Fase TDSP atual:** Data Acquisition → Modeling")
    st.markdown("**Metodologia:** CRISP-DM + TDSP")
    st.markdown("**TP:** 2 — Interface, coleta web e upload/download")

df_vis = df_all[
    df_all["uf"].isin(uf_sel)
    & df_all["ideb_anos_iniciais"].between(ideb_range[0], ideb_range[1])
]

tab_indicadores, tab_noticias, tab_dados = st.tabs(
    ["📊 Indicadores", "📰 Notícias & Nuvem de Palavras", "📤 Dados Complementares"]
)

# --- Aba 1: Indicadores -----------------------------------------------------
with tab_indicadores:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Municípios na seleção", len(df_vis))
    m2.metric("IDEB médio (anos iniciais)", f"{df_vis['ideb_anos_iniciais'].mean():.1f}" if len(df_vis) else "–")
    m3.metric("Taxa abandono média", f"{df_vis['taxa_abandono_pct'].mean():.1f}%" if len(df_vis) else "–")
    m4.metric("Escolas c/ internet", f"{df_vis['escolas_internet_pct'].mean():.0f}%" if len(df_vis) else "–")

    st.markdown('<p class="section-title">Amostra dos Dados — IDEB & Indicadores Municipais</p>', unsafe_allow_html=True)
    st.dataframe(
        df_vis.rename(columns={
            "municipio": "Município", "uf": "UF",
            "ideb_anos_iniciais": "IDEB Iniciais", "ideb_anos_finais": "IDEB Finais",
            "taxa_abandono_pct": "Abandono (%)", "escolas_internet_pct": "Internet (%)",
            "pib_per_capita": "PIB per capita (R$)", "ano": "Ano",
        }),
        use_container_width=True, hide_index=True,
    )

    if len(df_vis):
        st.markdown('<p class="section-title">IDEB por Município</p>', unsafe_allow_html=True)
        fig = px.bar(
            df_vis.sort_values("ideb_anos_iniciais", ascending=True),
            x="ideb_anos_iniciais", y="municipio", orientation="h", color="uf",
            labels={"ideb_anos_iniciais": "IDEB (Anos Iniciais)", "municipio": "Município"},
            color_discrete_sequence=px.colors.qualitative.Set2, height=400,
        )
        fig.update_layout(showlegend=True, plot_bgcolor="white", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="section-title">PIB per capita × IDEB (Anos Iniciais)</p>', unsafe_allow_html=True)
        fig2 = px.scatter(
            df_vis, x="pib_per_capita", y="ideb_anos_iniciais",
            size="escolas_internet_pct", color="taxa_abandono_pct", hover_name="municipio",
            labels={"pib_per_capita": "PIB per capita (R$)", "ideb_anos_iniciais": "IDEB (Anos Iniciais)",
                    "taxa_abandono_pct": "Abandono (%)", "escolas_internet_pct": "% Internet"},
            color_continuous_scale="RdYlGn_r", height=420,
        )
        fig2.update_layout(plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Nenhum município corresponde aos filtros selecionados.")

    st.download_button(
        "⬇️ Baixar seleção atual (CSV)",
        data=df_vis.to_csv(index=False).encode("utf-8-sig"),
        file_name="eduacesso_selecao.csv",
        mime="text/csv",
    )

# --- Aba 2: Notícias & Nuvem de Palavras ------------------------------------
with tab_noticias:
    text, text_is_live = load_text_source()
    news_df, news_is_live = load_news_source()

    st.markdown('<p class="section-title">Nuvem de Palavras — Texto sobre Educação no Brasil</p>', unsafe_allow_html=True)
    st.caption(
        "Fonte: Wikipédia, coletada com Beautiful Soup (src/data/scrape_web.py)."
        + ("" if text_is_live else " Exibindo texto de amostra — rode o script de coleta para dados atualizados.")
    )
    wc = build_wordcloud(text)
    st.image(wc.to_array(), use_container_width=True)

    col_freq, col_stats = st.columns([2, 1])
    with col_freq:
        st.markdown('<p class="section-title">Estatísticas Básicas — Palavras mais frequentes</p>', unsafe_allow_html=True)
        freq_df = word_frequencies(text)
        st.dataframe(freq_df, use_container_width=True, hide_index=True)
    with col_stats:
        st.markdown('<p class="section-title">Resumo do texto</p>', unsafe_allow_html=True)
        st.metric("Total de palavras", len(text.split()))
        st.metric("Palavras únicas (após filtro)", freq_df["palavra"].nunique() if len(freq_df) else 0)

    st.markdown('<p class="section-title">Notícias sobre Educação Municipal</p>', unsafe_allow_html=True)
    st.caption(
        "Fonte: Google News RSS, coletado com Beautiful Soup."
        + ("" if news_is_live else " Exibindo notícias de amostra — rode o script de coleta para dados atualizados.")
    )
    st.dataframe(news_df, use_container_width=True, hide_index=True)
    if "fonte" in news_df.columns and len(news_df):
        fig_news = px.bar(
            news_df["fonte"].value_counts().reset_index(),
            x="fonte", y="count", labels={"fonte": "Veículo", "count": "Nº de notícias"},
            color_discrete_sequence=["#2e7d5e"], height=320,
        )
        st.plotly_chart(fig_news, use_container_width=True)

# --- Aba 3: Dados complementares (upload/download) --------------------------
with tab_dados:
    st.markdown('<p class="section-title">Enviar dados complementares (CSV)</p>', unsafe_allow_html=True)
    st.write(
        "Envie um CSV com as mesmas colunas da base principal para complementar os "
        "indicadores exibidos no dashboard. Colunas esperadas:"
    )
    st.code(", ".join(REQUIRED_COLUMNS))

    uploaded = st.file_uploader("Arquivo CSV", type=["csv"], key="uploader")
    if uploaded is not None:
        try:
            new_df = pd.read_csv(uploaded)
            missing = set(REQUIRED_COLUMNS) - set(new_df.columns)
            if missing:
                st.error(f"Colunas ausentes no arquivo: {', '.join(sorted(missing))}")
            else:
                merged = pd.concat([st.session_state.base_df, new_df[REQUIRED_COLUMNS]], ignore_index=True)
                merged = merged.drop_duplicates(subset=["municipio", "ano"], keep="last")
                st.session_state.base_df = merged
                st.session_state.uploads_count += 1
                st.success(f"{len(new_df)} linha(s) processada(s) e mescladas à base ({len(merged)} municípios no total).")
        except Exception as exc:  # noqa: BLE001 — mostrar qualquer erro de parsing ao usuário
            st.error(f"Não foi possível ler o arquivo: {exc}")

    if st.session_state.uploads_count:
        st.caption(f"{st.session_state.uploads_count} arquivo(s) enviado(s) nesta sessão.")
        if st.button("↩️ Restaurar base original (desfazer uploads)"):
            st.session_state.base_df = fetch_ideb_sample()
            st.session_state.uploads_count = 0
            st.rerun()

    st.markdown('<p class="section-title">Base atual completa</p>', unsafe_allow_html=True)
    st.dataframe(st.session_state.base_df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Baixar base completa (CSV)",
        data=st.session_state.base_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="eduacesso_base_completa.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("EduAcesso ESG — TP2. Fontes: INEP/IDEB, IBGE, Wikipédia e Google News (coleta via Beautiful Soup).")
