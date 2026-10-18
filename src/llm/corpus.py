"""Corpus de documentos para as tarefas de LLM (resumo, sentimento, Q&A, geração).

Une as três fontes do projeto num formato único (um documento por linha):

- texto:      parágrafos da Wikipédia (quebrados em trechos curtos)
- noticia:    manchetes coletadas do Google News RSS
- indicador:  frase descritiva por município gerada a partir da base IDEB

Uso:
    python src/llm/corpus.py
Gera data/processed/corpus_llm.csv e data/processed/corpus_llm.jsonl
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.data import store  # noqa: E402

TASKS_BY_TYPE = {
    "texto": "resumo;qa",
    "noticia": "sentimento;resumo;qa",
    "indicador": "qa;geracao",
}
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_TOKEN = re.compile(r"\w{3,}", re.UNICODE)


def chunk_text(text: str, max_words: int = 90) -> list[str]:
    """Quebra o texto em trechos de até ~max_words palavras, respeitando frases."""
    chunks, current, count = [], [], 0
    for sentence in _SENTENCE_SPLIT.split(" ".join(text.split())):
        n = len(sentence.split())
        if current and count + n > max_words:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.append(sentence)
        count += n
    if current:
        chunks.append(" ".join(current))
    return [c for c in chunks if c.strip()]


def indicator_sentence(row: pd.Series) -> str:
    pib = f"{row['pib_per_capita']:,.0f}".replace(",", ".")
    return (
        f"Em {int(row['ano'])}, {row['municipio']} ({row['uf']}) registrou IDEB de "
        f"{row['ideb_anos_iniciais']} nos anos iniciais e {row['ideb_anos_finais']} nos anos finais, "
        f"taxa de abandono de {row['taxa_abandono_pct']}%, {int(row['escolas_internet_pct'])}% das "
        f"escolas com internet e PIB per capita de R$ {pib}."
    )


def build_corpus() -> pd.DataFrame:
    rows: list[dict] = []

    text, _ = store.load_text()
    for i, chunk in enumerate(chunk_text(text), start=1):
        rows.append({"doc_id": f"texto-{i:03d}", "tipo": "texto", "fonte": "Wikipédia", "texto": chunk})

    news, _ = store.load_news()
    for i, r in enumerate(news.itertuples(index=False), start=1):
        rows.append({"doc_id": f"noticia-{i:03d}", "tipo": "noticia",
                     "fonte": getattr(r, "fonte", "") or "Google News", "texto": str(r.titulo)})

    for _, r in store.load_all().iterrows():
        rows.append({"doc_id": f"indicador-{r['municipio'].lower().replace(' ', '-')}-{int(r['ano'])}",
                     "tipo": "indicador", "fonte": "IDEB/IBGE (amostra)", "texto": indicator_sentence(r)})

    df = pd.DataFrame(rows)
    df["tarefas_sugeridas"] = df["tipo"].map(TASKS_BY_TYPE)
    df["n_palavras"] = df["texto"].str.split().str.len()
    return df


def retrieve(query: str, corpus: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    """Recuperação simples por sobreposição de palavras (baseline sem LLM/embeddings).

    Na próxima etapa pode ser trocada por embeddings sem mudar o formato do corpus.
    """
    q = set(_TOKEN.findall(query.lower()))
    if not q:
        return corpus.head(0)
    scores = corpus["texto"].str.lower().apply(lambda t: len(q & set(_TOKEN.findall(t))))
    top = corpus.assign(score=scores).query("score > 0").sort_values("score", ascending=False)
    return top.head(k)


def main() -> None:
    store.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = build_corpus()
    df.to_csv(store.PROCESSED_DIR / "corpus_llm.csv", index=False, encoding="utf-8-sig")
    df.to_json(store.PROCESSED_DIR / "corpus_llm.jsonl", orient="records", lines=True, force_ascii=False)
    print(f"{len(df)} documentos salvos em data/processed/corpus_llm.(csv|jsonl)")
    print(df["tipo"].value_counts().to_string())


if __name__ == "__main__":
    main()
