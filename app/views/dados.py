import pandas as pd
import streamlit as st

import common
from src.data import store

common.init_state()
common.header("Upload / Download de dados")

common.section("Enviar dados complementares (CSV)")
st.write("Envie um CSV com as colunas abaixo para complementar a base exibida no dashboard.")
st.code(", ".join(common.REQUIRED_COLUMNS))

uploaded = st.file_uploader("Arquivo CSV", type=["csv"], key="uploader")
if uploaded is not None:
    try:
        new_df = pd.read_csv(uploaded)
        missing = set(common.REQUIRED_COLUMNS) - set(new_df.columns)
        if missing:
            st.error(f"Colunas ausentes no arquivo: {', '.join(sorted(missing))}")
        else:
            merged = pd.concat([st.session_state.base_df, new_df[common.REQUIRED_COLUMNS]], ignore_index=True)
            merged = merged.drop_duplicates(subset=["municipio", "ano"], keep="last")
            st.session_state.base_df = merged
            st.session_state.uploads_count += 1
            st.success(f"{len(new_df)} linha(s) mescladas à base ({len(merged)} registros no total).")
    except Exception as exc:  # noqa: BLE001 — mostra qualquer erro de leitura ao usuário
        st.error(f"Não foi possível ler o arquivo: {exc}")

if st.button("↩️ Recarregar base (descarta uploads, inclui registros da API)"):
    st.session_state.base_df = store.load_all()
    st.session_state.uploads_count = 0
    st.rerun()
if st.session_state.uploads_count:
    st.caption(f"{st.session_state.uploads_count} upload(s) nesta sessão.")

common.section("Base atual completa")
st.dataframe(st.session_state.base_df, use_container_width=True, hide_index=True)
st.download_button("⬇️ Baixar base completa (CSV)",
                   st.session_state.base_df.to_csv(index=False).encode("utf-8-sig"),
                   file_name="eduacesso_base_completa.csv", mime="text/csv")
