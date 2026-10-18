import streamlit as st

import common
from src.llm.corpus import retrieve
from src.llm.prompts import PROMPTS, render

common.init_state()
common.header("Preparação para LLM")
st.write(
    "Os dados coletados até aqui já estão unificados num corpus e as tarefas de LLM da próxima "
    "etapa têm prompts definidos. **Nenhum modelo é chamado nesta página.**"
)

corpus = common.load_corpus()

common.section("Corpus unificado")
c1, c2, c3 = st.columns(3)
counts = corpus["tipo"].value_counts()
c1.metric("Textos (Wikipédia)", int(counts.get("texto", 0)))
c2.metric("Notícias", int(counts.get("noticia", 0)))
c3.metric("Indicadores (frases)", int(counts.get("indicador", 0)))
tipo = st.selectbox("Filtrar por tipo", ["todos", *sorted(corpus["tipo"].unique())])
view = corpus if tipo == "todos" else corpus[corpus["tipo"] == tipo]
st.dataframe(view, use_container_width=True, hide_index=True)
st.download_button("⬇️ Baixar corpus (CSV)", corpus.to_csv(index=False).encode("utf-8-sig"),
                   file_name="corpus_llm.csv", mime="text/csv")

common.section("Tarefas planejadas")
for key, t in PROMPTS.items():
    with st.expander(f"{t['titulo']} — tipos: {', '.join(t['tipos'])}"):
        st.write(t["descricao"])
        st.code(t["template"], language="text")

common.section("Teste de prompt (sem LLM)")
tarefa = st.selectbox("Tarefa", list(PROMPTS), format_func=lambda k: PROMPTS[k]["titulo"])
if tarefa == "qa":
    pergunta = st.text_input("Pergunta", "Qual o IDEB de Três Lagoas?")
    ctx = retrieve(pergunta, corpus, k=3)
    st.caption("Contexto recuperado por sobreposição de palavras (baseline; na próxima etapa pode virar embeddings):")
    st.dataframe(ctx[["doc_id", "tipo", "texto", "score"]] if len(ctx) else ctx, use_container_width=True, hide_index=True)
    prompt = render("qa", contexto="\n".join(ctx["texto"]) or "(nenhum documento encontrado)", pergunta=pergunta)
else:
    opcoes = corpus[corpus["tipo"].isin(PROMPTS[tarefa]["tipos"])]
    doc = st.selectbox("Documento", opcoes["doc_id"])
    prompt = render(tarefa, texto=opcoes.set_index("doc_id").loc[doc, "texto"])
st.code(prompt, language="text")
