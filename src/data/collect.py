"""Coleta de dados via API do IBGE SIDRA e arquivos INEP."""

import requests
import pandas as pd


SIDRA_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"


def fetch_ideb_sample() -> pd.DataFrame:
    """Retorna amostra estática do IDEB para demonstração no TP1."""
    data = {
        "municipio": [
            "São Paulo", "Rio de Janeiro", "Manaus", "Fortaleza", "Cuiabá",
            "Campo Grande", "Três Lagoas", "Dourados", "Corumbá", "Ponta Porã",
            "Porto Alegre", "Recife", "Salvador", "Belém", "Goiânia",
        ],
        "uf": ["SP","RJ","AM","CE","MT","MS","MS","MS","MS","MS","RS","PE","BA","PA","GO"],
        "ideb_anos_iniciais": [6.1, 5.8, 4.9, 5.2, 5.5, 5.7, 5.3, 5.0, 4.6, 4.8,
                               6.3, 4.7, 5.1, 4.5, 5.6],
        "ideb_anos_finais":   [5.2, 4.9, 4.1, 4.3, 4.7, 4.8, 4.5, 4.2, 3.8, 4.0,
                               5.4, 3.9, 4.3, 3.7, 4.8],
        "taxa_abandono_pct":  [1.2, 1.8, 4.1, 3.7, 2.3, 2.0, 2.8, 3.2, 5.1, 4.0,
                               0.9, 4.5, 3.8, 5.6, 2.1],
        "escolas_internet_pct":[94, 88, 71, 76, 82, 85, 78, 74, 61, 68,
                                96, 72, 79, 63, 87],
        "pib_per_capita":     [52000, 41000, 23000, 18000, 29000, 31000, 28000,
                               22000, 19000, 21000, 43000, 17000, 20000, 16000, 33000],
        "ano": [2023]*15,
    }
    return pd.DataFrame(data)


def fetch_municipios_ms() -> pd.DataFrame:
    """Busca lista de municípios do MS via API do IBGE."""
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/MS/municipios"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        muns = resp.json()
        return pd.DataFrame([{"id": m["id"], "municipio": m["nome"]} for m in muns])
    except requests.RequestException:
        return pd.DataFrame(columns=["id", "municipio"])
