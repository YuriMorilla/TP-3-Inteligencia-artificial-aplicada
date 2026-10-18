import plotly.express as px
import streamlit as st

import common

common.init_state()
common.header("Notícias & Nuvem de Palavras")

text, text_live = common.load_text_source()
news_df, news_live = common.load_news_source()

common.section("Nuvem de palavras — texto sobre educação no Brasil")
st.caption("Fonte: Wikipédia (Beautiful Soup, src/data/scrape_web.py)."
           + ("" if text_live else " Exibindo texto de amostra — rode o script de coleta."))
st.image(common.build_wordcloud(text).to_array(), use_container_width=True)

col_freq, col_stats = st.columns([2, 1])
freq_df = common.word_frequencies(text)
with col_freq:
    common.section("Palavras mais frequentes")
    st.dataframe(freq_df, use_container_width=True, hide_index=True)
with col_stats:
    common.section("Resumo do texto")
    st.metric("Total de palavras", len(text.split()))
    st.metric("Termos exibidos", len(freq_df))

common.section("Notícias sobre educação municipal")
st.caption("Fonte: Google News RSS (Beautiful Soup)."
           + ("" if news_live else " Exibindo notícias de amostra — rode o script de coleta."))
st.dataframe(news_df, use_container_width=True, hide_index=True)
if "fonte" in news_df.columns and len(news_df):
    fig = px.bar(news_df["fonte"].value_counts().reset_index(), x="fonte", y="count",
                 labels={"fonte": "Veículo", "count": "Nº de notícias"},
                 color_discrete_sequence=["#2e7d5e"], height=320)
    st.plotly_chart(fig, use_container_width=True)
