"""API do EduAcesso ESG (FastAPI).

Rodar (na raiz do projeto):
    uvicorn api.main:app --reload
Documentação interativa: http://localhost:8000/docs
"""

from __future__ import annotations

import json
import unicodedata

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

from src.data import store
from src.llm.corpus import build_corpus

app = FastAPI(
    title="EduAcesso ESG API",
    version="3.0.0",
    description=(
        "Consulta e envio de indicadores educacionais municipais (IDEB, abandono, "
        "internet, PIB per capita), além de notícias coletadas e corpus preparado "
        "para tarefas de LLM. Projeto de Bloco — IA Aplicada (TP3)."
    ),
)


class Municipio(BaseModel):
    municipio: str = Field(..., min_length=2, examples=["Três Lagoas"])
    uf: str = Field(..., min_length=2, max_length=2, examples=["MS"])
    ideb_anos_iniciais: float = Field(..., ge=0, le=10, examples=[5.3])
    ideb_anos_finais: float = Field(..., ge=0, le=10, examples=[4.5])
    taxa_abandono_pct: float = Field(..., ge=0, le=100, examples=[2.8])
    escolas_internet_pct: float = Field(..., ge=0, le=100, examples=[78])
    pib_per_capita: float = Field(..., ge=0, examples=[28000])
    ano: int = Field(..., ge=2000, le=2100, examples=[2024])

    @field_validator("uf")
    @classmethod
    def _uf_maiuscula(cls, v: str) -> str:
        return v.upper()


def _norm(value: str) -> str:
    """Minúsculas e sem acentos, para comparar nomes de município."""
    s = unicodedata.normalize("NFKD", str(value))
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def _records(df: pd.DataFrame) -> list[dict]:
    return json.loads(df.to_json(orient="records"))


@app.get("/", tags=["Sistema"], summary="Status da API")
def raiz() -> dict:
    return {"servico": "EduAcesso ESG API", "versao": app.version, "docs": "/docs"}


@app.get("/municipios", response_model=list[Municipio], tags=["Municípios"],
         summary="Lista indicadores municipais (GET)")
def listar_municipios(
    uf: str | None = Query(None, min_length=2, max_length=2, description="Filtra pela UF (ex.: MS)"),
    ano: int | None = Query(None, description="Filtra pelo ano"),
    ideb_min: float | None = Query(None, ge=0, le=10, description="IDEB mínimo (anos iniciais)"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros retornados"),
) -> list[dict]:
    df = store.load_all()
    if uf:
        df = df[df["uf"] == uf.upper()]
    if ano is not None:
        df = df[df["ano"] == ano]
    if ideb_min is not None:
        df = df[df["ideb_anos_iniciais"] >= ideb_min]
    return _records(df.head(limit))


@app.get("/municipios/{nome}", response_model=list[Municipio], tags=["Municípios"],
         summary="Consulta um município pelo nome (GET)")
def obter_municipio(nome: str) -> list[dict]:
    df = store.load_all()
    found = df[df["municipio"].map(_norm) == _norm(nome)]
    if found.empty:
        raise HTTPException(status_code=404, detail=f"Município '{nome}' não encontrado.")
    return _records(found)


@app.post("/municipios", response_model=Municipio, status_code=201, tags=["Municípios"],
          summary="Envia um novo registro municipal (POST)")
def criar_municipio(item: Municipio) -> Municipio:
    df = store.load_all()
    dup = (df["municipio"].map(_norm) == _norm(item.municipio)) & (df["ano"] == item.ano)
    if dup.any():
        raise HTTPException(status_code=409,
                            detail=f"Já existe registro de '{item.municipio}' para {item.ano}.")
    store.append_record(item.model_dump())
    return item


@app.get("/estatisticas", tags=["Análises"], summary="Estatísticas agregadas da base")
def estatisticas() -> dict:
    df = store.load_all()
    por_uf = (df.groupby("uf")
                .agg(municipios=("municipio", "count"),
                     ideb_medio=("ideb_anos_iniciais", "mean"),
                     abandono_medio=("taxa_abandono_pct", "mean"))
                .round(2))
    return {
        "total_registros": int(len(df)),
        "municipios_unicos": int(df["municipio"].nunique()),
        "ideb_medio_anos_iniciais": round(float(df["ideb_anos_iniciais"].mean()), 2),
        "abandono_medio_pct": round(float(df["taxa_abandono_pct"].mean()), 2),
        "por_uf": json.loads(por_uf.to_json(orient="index")),
    }


@app.get("/noticias", tags=["Conteúdo web"], summary="Notícias coletadas (Beautiful Soup)")
def listar_noticias(limit: int = Query(20, ge=1, le=100)) -> dict:
    df, coletado = store.load_news()
    return {"fonte_real": coletado, "total": int(len(df)),
            "noticias": _records(df.head(limit).fillna(""))}


@app.get("/corpus", tags=["LLM"], summary="Documentos preparados para tarefas de LLM")
def listar_corpus(
    tipo: str | None = Query(None, pattern="^(texto|noticia|indicador)$"),
    limit: int = Query(20, ge=1, le=500),
) -> dict:
    df = build_corpus()
    if tipo:
        df = df[df["tipo"] == tipo]
    return {"total": int(len(df)), "documentos": _records(df.head(limit))}
