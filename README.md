# EduAcesso ESG

Dashboard analítico para monitoramento de indicadores educacionais municipais com foco em equidade e ODS 4.

**Status:** TP2 — interface dinâmica, coleta web, cache/estado de sessão e upload/download de dados.

## Estrutura

```
.
├── app/                    # Aplicação Streamlit (main.py)
├── data/
│   ├── raw/                # Dados brutos: coleta web + amostras de fallback
│   ├── processed/          # Dados limpos e transformados
│   └── external/           # Dados de terceiros
├── docs/
│   ├── project_charter/    # Project Charter (v1 e v2)
│   └── data_summary/       # Data Summary Report (v1 e v2)
├── notebooks/              # Exploração e análise
├── src/
│   ├── data/                # Scripts de coleta e limpeza
│   │   ├── collect.py        # Coleta via API do IBGE/IDEB (TP1)
│   │   └── scrape_web.py      # Coleta via Beautiful Soup — Wikipédia + Google News RSS (TP2)
│   ├── features/            # Engenharia de features
│   ├── models/               # Modelagem e scoring
│   └── visualization/         # Componentes visuais
├── reports/figures/        # Gráficos exportados
├── tests/
└── requirements.txt
```

## Setup do ambiente

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Coleta de dados (opcional, antes de rodar o app)

O app já funciona com dados de amostra em `data/raw/*_sample.*`. Para atualizar
com conteúdo coletado ao vivo:

```bash
python src/data/scrape_web.py
```

Isso gera `data/raw/wiki_educacao.txt` (texto para a nuvem de palavras) e
`data/raw/noticias_educacao.csv` (tabela de notícias). O app detecta
automaticamente os arquivos reais e usa a amostra apenas como fallback.

## Rodar o app

```bash
streamlit run app/main.py
```

A aplicação tem três abas:

1. **Indicadores** — filtros dinâmicos (UF, faixa de IDEB), tabela e gráficos, download da seleção em CSV.
2. **Notícias & Nuvem de Palavras** — conteúdo extraído da web com Beautiful Soup: nuvem de palavras, frequência de termos e tabela de notícias.
3. **Dados Complementares** — upload de CSV para complementar a base (com validação de colunas e deduplicação), estado mantido em `st.session_state`, e download da base completa.

## Controle de versão (Git)

Fluxo sugerido para o TP2:

```bash
git checkout -b tp2
git add .
git commit -m "TP2 - interface dinâmica, coleta web, cache e upload/download"
git push origin tp2
```

Depois, abra um Pull Request de `tp2` para `main` e, ao final da avaliação,
crie uma tag de entrega:

```bash
git checkout main
git merge tp2
git tag -a tp2-entrega -m "Entrega TP2"
git push origin main --tags
```

## Preparação para deploy

O app é compatível com o **Streamlit Community Cloud**:

1. Repositório público no GitHub (já configurado).
2. Em [share.streamlit.io](https://share.streamlit.io), aponte para este
   repositório, branch `main`, arquivo principal `app/main.py`.
3. Nenhuma variável de ambiente é obrigatória nesta etapa (o app não usa
   chaves de API); `python-dotenv` já está no `requirements.txt` para quando
   a integração com LLM for adicionada em um TP futuro.

## Metodologia

Este projeto segue a estrutura **CRISP-DM + TDSP**, documentada em
`docs/project_charter/` e `docs/data_summary/`.
