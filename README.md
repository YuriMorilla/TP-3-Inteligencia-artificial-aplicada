# EduAcesso ESG

Dashboard analítico para monitoramento de indicadores educacionais municipais, com foco em equidade (ODS 4 e 10).

**Status:** TP3 — app multipágina, API FastAPI, corpus e prompts preparados para LLM.

## Estrutura

```
.
├── app/
│   ├── main.py             # Entrada: menu de navegação (st.navigation)
│   ├── common.py           # Cache, estado de sessão e utilidades compartilhadas
│   └── views/              # Páginas: home, indicadores, noticias, dados, api, llm
├── api/main.py             # API FastAPI (GET/POST)
├── data/
│   ├── raw/                # Coleta web + amostras de fallback
│   ├── processed/          # Corpus para LLM, registros enviados pela API
│   └── external/
├── docs/
│   ├── project_charter/    # Project Charter (v1 → v3)
│   ├── data_summary/       # Data Summary Report (v1 → v3)
│   └── api/                # Documentação da API
├── src/
│   ├── data/               # collect.py, scrape_web.py (Beautiful Soup), store.py (camada de dados)
│   └── llm/                # corpus.py e prompts.py (preparação para LLM)
├── tests/                  # pytest: API e páginas do app
├── requirements.txt / requirements-dev.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Executar

Todos os comandos na raiz do projeto.

```bash
# 1) (opcional) coletar dados reais da web — sem isso o app usa as amostras
python src/data/scrape_web.py

# 2) (opcional) regenerar o corpus para LLM com os dados coletados
python src/llm/corpus.py

# 3) app (menu lateral com as 6 páginas)
streamlit run app/main.py

# 4) API, em outro terminal — Swagger em http://localhost:8000/docs
uvicorn api.main:app --reload
```

O app funciona sem a API no ar. A página **API FastAPI** traz um testador que chama a API
local; registros enviados por POST aparecem no app após "Recarregar base" em
**Upload / Download**. Detalhes das rotas em [`docs/api/api_documentation.md`](docs/api/api_documentation.md).

## Testes

```bash
pip install -r requirements-dev.txt
python -m pytest -q tests
```

## Git

```bash
git checkout -b tp3
git add .
git commit -m "TP3 - app multipágina, API FastAPI e preparação para LLM"
git push -u origin tp3
```

## Deploy

O app (`app/main.py`) é compatível com o Streamlit Community Cloud. A API FastAPI roda
localmente nesta etapa; o app não depende dela para funcionar.

## Metodologia

CRISP-DM + TDSP, documentadas em `docs/project_charter/` e `docs/data_summary/`.
