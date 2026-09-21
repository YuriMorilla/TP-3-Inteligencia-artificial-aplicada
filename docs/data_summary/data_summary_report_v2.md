# Data Summary Report — v2 (TP2)

**Projeto:** EduAcesso ESG
**Versão:** 2.0
**Data:** 2026-09-20

> Este documento complementa o `data_summary_report_v1.md`. As fontes já
> descritas na v1 (INEP, IBGE, IDEB, Portal da Transparência) permanecem
> válidas; aqui são documentadas as duas novas fontes coletadas via
> **Beautiful Soup** no TP2, além do que mudou na estratégia de coleta.

---

## 1. Novas Fontes de Dados (TP2)

| # | Fonte | Tipo | Formato | Acesso | Objetivo de Uso |
|---|-------|------|---------|--------|-----------------|
| 6 | Wikipédia (pt) — artigos sobre educação no Brasil | Texto não estruturado | HTML | Público | Insumo para nuvem de palavras e estatística de frequência de termos |
| 7 | Google News RSS — busca "educação municípios Brasil" | Notícias | XML (RSS) | Público | Tabela de notícias recentes exibida no dashboard |

---

## 2. Detalhamento das Novas Fontes

### 2.1 Wikipédia — Educação no Brasil
- **URLs coletadas:** `Educação_no_Brasil`, `Índice_de_Desenvolvimento_da_Educação_Básica`
- **Método:** `requests` + `BeautifulSoup` (parser `html.parser`), extraindo apenas `<p>` de primeiro nível dentro de `div.mw-parser-output` (evita infoboxes, tabelas e notas de rodapé)
- **Pós-processamento:** remoção de marcadores de referência (`[1]`, `[2]`...) via regex
- **Volume:** texto corrido (poucos KB), atualizado a cada execução do scraper
- **Qualidade:** boa para fins didáticos; texto enciclopédico, não é dado estatístico oficial
- **Desafios:** conteúdo pode mudar entre execuções; layout da Wikipédia é estável, baixo risco de quebra

### 2.2 Google News RSS
- **URL base:** `https://news.google.com/rss/search?q=<query>&hl=pt-BR&gl=BR&ceid=BR:pt-BR`
- **Método:** `requests` + `BeautifulSoup` (parser `xml`), iterando sobre tags `<item>`
- **Campos extraídos:** `titulo`, `fonte`, `data`, `link`
- **Cobertura temporal:** notícias recentes (janela rotativa do feed, não histórico)
- **Qualidade:** alta atualidade, porém sem garantia de estabilidade do endpoint no longo prazo
- **Desafios:** feed pode não retornar itens para consultas muito específicas; sem paginação

### 2.3 Estratégia de Fallback
Ambas as coletas gravam em `data/raw/` (`wiki_educacao.txt`,
`noticias_educacao.csv`). Arquivos de amostra equivalentes
(`*_sample.txt`, `*_sample.csv`) foram versionados no repositório para que
o dashboard funcione mesmo sem executar o scraper ou sem acesso à
internet no momento da avaliação — o app (`app/main.py`) prioriza o
arquivo real e usa a amostra apenas como fallback, sinalizando isso na
interface.

---

## 3. Uso no Dashboard

| Elemento da interface | Fonte | Processamento |
|---|---|---|
| Nuvem de palavras | Wikipédia | Tokenização simples + lista de stopwords em português + `WordCloud` |
| Tabela "palavras mais frequentes" | Wikipédia | `collections.Counter` sobre tokens filtrados |
| Tabela de notícias + gráfico por veículo | Google News RSS | Leitura direta do CSV coletado |

---

## 4. Cache e Estado de Sessão

- `st.cache_data` — usado nas funções de carregamento (amostra IDEB, texto,
  notícias, frequência de palavras): evita reprocessamento a cada
  interação do usuário nos filtros.
- `st.cache_resource` — usado na geração do objeto `WordCloud`, que é mais
  custoso de montar e não muda entre reruns para o mesmo texto.
- `st.session_state` — mantém a base de dados (`base_df`) e o contador de
  uploads (`uploads_count`) vivos entre interações, permitindo que os CSVs
  enviados pelo usuário persistam durante a sessão até serem
  explicitamente restaurados.

---

## 5. Próximos Passos (TP3 e além)

- [x] Implementar pipeline de coleta web (Beautiful Soup) — TP2
- [x] Implementar cache e estado de sessão — TP2
- [x] Serviço de upload/download de CSV — TP2
- [ ] Calcular score ESG-educação composto
- [ ] Integrar LLM para geração de análises textuais por município
- [ ] Migrar de amostra estática para coleta completa via API do INEP/SIDRA
