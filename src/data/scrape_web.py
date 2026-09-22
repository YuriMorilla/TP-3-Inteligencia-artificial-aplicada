"""
Coleta de conteúdo web para o EduAcesso ESG (TP2).

Duas fontes independentes, ambas via Beautiful Soup:

1. Wikipédia (texto corrido em português sobre educação no Brasil)
   -> insumo para a nuvem de palavras e estatísticas de frequência de termos.
2. Google News RSS (notícias recentes sobre educação municipal)
   -> tabela de notícias exibida no dashboard.

Uso (executar como script separado, fora do Streamlit):

    python src/data/scrape_web.py

Saída:
    data/raw/wiki_educacao.txt
    data/raw/noticias_educacao.csv

Se a coleta falhar (sem internet, mudança de layout, rate limit etc.), os
arquivos de amostra em data/raw/*_sample.* continuam disponíveis e o app
usa esses arquivos automaticamente como fallback (ver app/main.py).
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests
from bs4 import BeautifulSoup

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (EduAcessoESG/1.0; projeto academico TP2)"}

WIKI_URLS = [
    "https://pt.wikipedia.org/wiki/Educação_no_Brasil",
    "https://pt.wikipedia.org/wiki/Índice_de_Desenvolvimento_da_Educação_Básica",
]

NEWS_QUERY = "educação municípios Brasil"


def scrape_wikipedia_text(urls: list[str] = WIKI_URLS, delay: float = 1.0) -> str:
    """Extrai o texto dos parágrafos de páginas da Wikipédia.

    Pega todos os <p> dentro de div.mw-parser-output, exceto os que estão
    dentro de tabelas (infobox), evitando depender de estarem no primeiro
    nível — o HTML real da Wikipédia varia mais do que o de um exemplo
    simplificado.
    """
    all_text = []
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"[aviso] Falha ao acessar {url}: {exc}")
            continue

        resp.encoding = resp.apparent_encoding or resp.encoding
        soup = BeautifulSoup(resp.text, "html.parser")
        content = soup.select_one("div.mw-parser-output")
        if not content:
            print(f"[aviso] Estrutura inesperada em {url} (status {resp.status_code}, {len(resp.text)} bytes)")
            continue

        paragraphs = [p for p in content.find_all("p") if not p.find_parent("table")]
        text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        text = re.sub(r"\[\d+\]", "", text)  # remove marcadores de referência [1], [2]...
        text = re.sub(r"\s+", " ", text).strip()

        print(f"  {url} -> {len(paragraphs)} parágrafo(s), {len(text)} caractere(s)")
        if text:
            all_text.append(text)
        time.sleep(delay)  # cortesia com o servidor entre requisições

    return "\n\n".join(all_text)


def scrape_google_news_rss(query: str = NEWS_QUERY, max_items: int = 30) -> pd.DataFrame:
    """Extrai manchetes de notícias via feed RSS público do Google Notícias."""
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=pt-BR&gl=BR&ceid=BR:pt-BR"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"[aviso] Falha ao acessar feed de notícias: {exc}")
        return pd.DataFrame(columns=["titulo", "fonte", "data", "link"])

    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item")[:max_items]

    rows = []
    for item in items:
        title = item.title.get_text(strip=True) if item.title else ""
        link = item.link.get_text(strip=True) if item.link else ""
        pub_date = item.pubDate.get_text(strip=True) if item.pubDate else ""
        source_tag = item.find("source")
        source = source_tag.get_text(strip=True) if source_tag else ""
        rows.append({"titulo": title, "fonte": source, "data": pub_date, "link": link})

    return pd.DataFrame(rows)


def main() -> None:
    print("Coletando texto da Wikipédia...")
    text = scrape_wikipedia_text()
    if text:
        (RAW_DIR / "wiki_educacao.txt").write_text(text, encoding="utf-8")
        print(f"  -> {len(text)} caracteres salvos em data/raw/wiki_educacao.txt")
    else:
        print("  -> nenhum texto coletado; o app usará o arquivo de amostra.")

    print("Coletando notícias via Google News RSS...")
    df_news = scrape_google_news_rss()
    if not df_news.empty:
        df_news.to_csv(RAW_DIR / "noticias_educacao.csv", index=False, encoding="utf-8-sig")
        print(f"  -> {len(df_news)} notícias salvas em data/raw/noticias_educacao.csv")
    else:
        print("  -> nenhuma notícia coletada; o app usará o arquivo de amostra.")


if __name__ == "__main__":
    main()
