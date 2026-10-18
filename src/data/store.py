"""Camada de dados compartilhada entre Streamlit, FastAPI e scripts.

Não depende de Streamlit nem de FastAPI: só pandas. Assim a mesma lógica
alimenta o dashboard, a API e a geração do corpus para LLM.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

COLUMNS = [
    "municipio", "uf", "ideb_anos_iniciais", "ideb_anos_finais",
    "taxa_abandono_pct", "escolas_internet_pct", "pib_per_capita", "ano",
]


def seed_df() -> pd.DataFrame:
    """Amostra estática do IDEB (base inicial do projeto)."""
    return pd.DataFrame({
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
    })


def api_csv_path() -> Path:
    """Arquivo onde a API grava os registros enviados via POST."""
    return Path(os.getenv("EDUACESSO_API_CSV", PROCESSED_DIR / "municipios_api.csv"))


NUMERIC_COLUMNS = [
    "ideb_anos_iniciais", "ideb_anos_finais", "taxa_abandono_pct",
    "escolas_internet_pct", "pib_per_capita",
]


def _typed(df: pd.DataFrame) -> pd.DataFrame:
    """Garante tipos numéricos (um DataFrame vazio vem como object e contaminaria o concat)."""
    df = df.copy()
    df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].apply(pd.to_numeric)
    df["ano"] = pd.to_numeric(df["ano"]).astype(int)
    return df


def load_api_records() -> pd.DataFrame:
    path = api_csv_path()
    if path.exists() and path.stat().st_size > 0:
        return _typed(pd.read_csv(path)[COLUMNS])
    return _typed(pd.DataFrame(columns=COLUMNS))


def load_all() -> pd.DataFrame:
    """Base completa: amostra + registros enviados pela API (sem duplicatas)."""
    merged = pd.concat([seed_df(), load_api_records()], ignore_index=True)
    merged = merged.drop_duplicates(subset=["municipio", "ano"], keep="last")
    return _typed(merged).reset_index(drop=True)


def append_record(record: dict) -> None:
    """Acrescenta um registro ao CSV da API (cria o arquivo se necessário)."""
    path = api_csv_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    row = pd.DataFrame([{c: record[c] for c in COLUMNS}])
    row.to_csv(path, mode="a", header=not path.exists() or path.stat().st_size == 0,
               index=False, encoding="utf-8")


def load_text() -> tuple[str, bool]:
    """Texto coletado da web; usa amostra se o scraper não rodou."""
    real, sample = RAW_DIR / "wiki_educacao.txt", RAW_DIR / "wiki_educacao_sample.txt"
    if real.exists() and real.stat().st_size > 0:
        return real.read_text(encoding="utf-8"), True
    return sample.read_text(encoding="utf-8"), False


def load_news() -> tuple[pd.DataFrame, bool]:
    """Notícias coletadas da web; usa amostra se o scraper não rodou."""
    real, sample = RAW_DIR / "noticias_educacao.csv", RAW_DIR / "noticias_educacao_sample.csv"
    if real.exists() and real.stat().st_size > 0:
        return pd.read_csv(real), True
    return pd.read_csv(sample), False
