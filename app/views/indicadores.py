import plotly.express as px
import streamlit as st

import common

common.init_state()
common.header("Indicadores municipais")

df_all = st.session_state.base_df

with st.sidebar:
    st.header("Filtros")
    ufs = sorted(df_all["uf"].unique().tolist())
    uf_sel = st.multiselect("Estado (UF)", ufs, default=ufs, key="uf_filter")
    lo, hi = float(df_all["ideb_anos_iniciais"].min()), float(df_all["ideb_anos_iniciais"].max())
    ideb_range = st.slider("Faixa de IDEB (anos iniciais)", lo, hi, (lo, hi), step=0.1, key="ideb_filter")

df_vis = df_all[df_all["uf"].isin(uf_sel) & df_all["ideb_anos_iniciais"].between(*ideb_range)]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Municípios na seleção", len(df_vis))
m2.metric("IDEB médio (anos iniciais)", f"{df_vis['ideb_anos_iniciais'].mean():.1f}" if len(df_vis) else "–")
m3.metric("Taxa abandono média", f"{df_vis['taxa_abandono_pct'].mean():.1f}%" if len(df_vis) else "–")
m4.metric("Escolas c/ internet", f"{df_vis['escolas_internet_pct'].mean():.0f}%" if len(df_vis) else "–")

common.section("Dados — IDEB & indicadores municipais")
st.dataframe(
    df_vis.rename(columns={
        "municipio": "Município", "uf": "UF", "ideb_anos_iniciais": "IDEB Iniciais",
        "ideb_anos_finais": "IDEB Finais", "taxa_abandono_pct": "Abandono (%)",
        "escolas_internet_pct": "Internet (%)", "pib_per_capita": "PIB per capita (R$)", "ano": "Ano"}),
    use_container_width=True, hide_index=True,
)

if len(df_vis):
    common.section("IDEB por município")
    fig = px.bar(df_vis.sort_values("ideb_anos_iniciais"), x="ideb_anos_iniciais", y="municipio",
                 orientation="h", color="uf", height=420,
                 labels={"ideb_anos_iniciais": "IDEB (Anos Iniciais)", "municipio": "Município"},
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(plot_bgcolor="white", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    common.section("PIB per capita × IDEB (anos iniciais)")
    fig2 = px.scatter(df_vis, x="pib_per_capita", y="ideb_anos_iniciais", size="escolas_internet_pct",
                      color="taxa_abandono_pct", hover_name="municipio", height=420,
                      color_continuous_scale="RdYlGn_r",
                      labels={"pib_per_capita": "PIB per capita (R$)", "ideb_anos_iniciais": "IDEB (Anos Iniciais)",
                              "taxa_abandono_pct": "Abandono (%)", "escolas_internet_pct": "% Internet"})
    fig2.update_layout(plot_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Nenhum município corresponde aos filtros selecionados.")

st.download_button("⬇️ Baixar seleção atual (CSV)", df_vis.to_csv(index=False).encode("utf-8-sig"),
                   file_name="eduacesso_selecao.csv", mime="text/csv")
