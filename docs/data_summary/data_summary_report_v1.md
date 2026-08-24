# Data Summary Report — v1 (Esboço Inicial)

**Projeto:** EduAcesso ESG  
**Versão:** 1.0 — Esboço  
**Data:** 2026-08-24  

---

## 1. Visão Geral das Fontes de Dados

| # | Fonte | Tipo | Formato | Acesso | Objetivo de Uso |
|---|-------|------|---------|--------|-----------------|
| 1 | INEP — Censo Escolar | Dados administrativos | CSV / API | Público | Taxas de matrícula, aprovação, abandono por município |
| 2 | IBGE — SIDRA | Dados socioeconômicos | API REST | Público | PIB per capita, IDH, população por faixa etária |
| 3 | IBGE — Malha Municipal | Geoespacial | GeoJSON / Shapefile | Público | Mapas e visualizações geográficas |
| 4 | MEC — IDEB | Índice de qualidade | CSV | Público | IDEB por escola e município (anos iniciais e finais) |
| 5 | Portal da Transparência | Orçamento público | CSV / API | Público | Investimento federal em educação por município |

---

## 2. Detalhamento das Fontes

### 2.1 INEP — Censo Escolar
- **URL:** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
- **Granularidade:** Escola → Município → Estado → Brasil
- **Cobertura temporal:** 2015–2023 (séries anuais)
- **Variáveis-chave:** `QT_MAT_BAS`, `QT_MAT_INF`, `TP_LOCALIZACAO` (urbana/rural), `IN_INTERNET`, `IN_COMPUTADOR`
- **Volume estimado:** ~300 MB por ano (microdados completos)
- **Qualidade:** Alta — dados oficiais com dicionário publicado
- **Desafios:** Tamanho dos arquivos; necessidade de filtros por município

### 2.2 IBGE — SIDRA API
- **URL:** https://servicodados.ibge.gov.br/api/v3/agregados
- **Tabelas relevantes:** T6579 (PIB municipal), T793 (população por município)
- **Formato:** JSON via REST
- **Cobertura temporal:** Depende da tabela (2010–2022)
- **Qualidade:** Alta — fonte oficial
- **Desafios:** Rate limiting; necessidade de paginação

### 2.3 INEP — IDEB
- **URL:** https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb
- **Granularidade:** Escola e município
- **Variáveis-chave:** `VL_OBSERVADO`, `VL_PROJETADO`, ano de referência
- **Atualização:** Bienal (anos ímpares)

### 2.4 Portal da Transparência
- **URL:** https://portaldatransparencia.gov.br/download-de-dados/transferencias
- **Uso:** Correlacionar investimento público com desempenho educacional

---

## 3. Estratégia de Coleta (TP1 — MVP)

Para o TP1, será utilizado um **subconjunto** dos dados para demonstração no Streamlit:

```
Fonte prioritária:  IBGE SIDRA (API) + IDEB (CSV estático)
Municípios demo:    Todos os municípios do MS + amostra nacional
Período demo:       2019–2023
```

A coleta completa e o pipeline automatizado serão desenvolvidos nos TPs seguintes.

---

## 4. Variáveis de Interesse (Candidatas ao Score ESG-Educação)

| Variável | Fonte | Tipo | Relevância ESG |
|----------|-------|------|----------------|
| Taxa de matrícula líquida | INEP | Numérica [0–1] | Acesso |
| Taxa de abandono escolar | INEP | Numérica [0–1] | Equidade |
| IDEB (anos iniciais) | INEP | Numérica [0–10] | Qualidade |
| IDEB (anos finais) | INEP | Numérica [0–10] | Qualidade |
| % escolas com internet | INEP | Numérica [0–1] | Infraestrutura |
| PIB per capita municipal | IBGE | Numérica (R$) | Contexto socioecon. |
| Investimento federal/aluno | Transp. | Numérica (R$) | Governança |

---

## 5. Próximos Passos (TPs Futuros)

- [ ] Desenvolver pipeline de coleta automatizada (ETL com Pandas + requests)
- [ ] Implementar cache e versionamento dos dados brutos
- [ ] Calcular score ESG-educação composto
- [ ] Integrar LLM para geração de análises textuais por município
- [ ] Web scraping de notícias regionais sobre educação (contexto qualitativo)
