# Data Summary Report — v3 (TP3)

**Projeto:** EduAcesso ESG
**Versão:** 3.0
**Data:** 2026-10-18

> Complementa as versões anteriores: v1 (INEP, IBGE, IDEB, Portal da Transparência)
> e v2 (Wikipédia e Google News via Beautiful Soup). Este documento consolida o
> inventário atual, registra a decisão sobre scraping dinâmico e descreve os novos
> dados derivados: registros enviados pela API e o corpus para LLM.

---

## 1. Inventário de fontes e arquivos

| # | Fonte / arquivo | Origem | Formato | Local | Uso |
|---|---|---|---|---|---|
| 1 | Indicadores municipais (IDEB, abandono, internet, PIB per capita) | Amostra baseada em INEP/IBGE (`store.seed_df`) | DataFrame | código | Dashboard, API, corpus |
| 2 | Texto sobre educação no Brasil | Wikipédia (Beautiful Soup) | TXT | `data/raw/wiki_educacao.txt` (amostra: `*_sample.txt`) | Nuvem de palavras, corpus |
| 3 | Notícias sobre educação municipal | Google News RSS (Beautiful Soup) | CSV | `data/raw/noticias_educacao.csv` (amostra: `*_sample.csv`) | Tabela de notícias, corpus |
| 4 | **Registros enviados via API (novo)** | `POST /municipios` | CSV | `data/processed/municipios_api.csv` | Complementa a fonte 1 |
| 5 | **Corpus para LLM (novo)** | Derivado de 1, 2 e 3 | CSV + JSONL | `data/processed/corpus_llm.csv` / `.jsonl` | Tarefas de LLM (TP4) |

As fontes 2 e 3 são regeneradas por `python src/data/scrape_web.py`; o corpus por
`python src/llm/corpus.py`.

## 2. Decisão sobre scraping dinâmico (Selenium)

Avaliado e **não adotado** neste TP. As páginas coletadas (artigos da Wikipédia e feed
RSS) entregam o conteúdo no HTML/XML inicial, sem formulários, rolagem infinita ou
carregamento assíncrono; `requests` + Beautiful Soup resolvem com menos dependências e
sem driver de navegador. Gatilho para reavaliar: incluir uma fonte cujo conteúdo só
apareça após interação em JavaScript (por exemplo, painéis do INEP com filtros).

## 3. Dicionário de dados

### 3.1 Indicadores municipais (fontes 1 e 4)

| Campo | Tipo | Descrição | Validação na API |
|---|---|---|---|
| `municipio` | texto | Nome do município | mín. 2 caracteres |
| `uf` | texto | Sigla do estado | 2 letras (maiúscula) |
| `ideb_anos_iniciais` | decimal | IDEB, anos iniciais do fundamental | 0–10 |
| `ideb_anos_finais` | decimal | IDEB, anos finais | 0–10 |
| `taxa_abandono_pct` | decimal | Taxa de abandono escolar (%) | 0–100 |
| `escolas_internet_pct` | decimal | Escolas com internet (%) | 0–100 |
| `pib_per_capita` | decimal | PIB per capita (R$) | ≥ 0 |
| `ano` | inteiro | Ano de referência | 2000–2100 |

Chave natural: (`municipio`, `ano`). Em caso de duplicata, a API recusa (409) e o upload
no dashboard mantém o registro mais recente.

### 3.2 Notícias (fonte 3)

`titulo`, `fonte` (veículo), `data` (publicação, formato RSS), `link`.

### 3.3 Corpus para LLM (fonte 5)

| Campo | Descrição |
|---|---|
| `doc_id` | Identificador (`texto-001`, `noticia-001`, `indicador-<municipio>-<ano>`) |
| `tipo` | `texto`, `noticia` ou `indicador` |
| `fonte` | Origem do documento |
| `texto` | Conteúdo: trecho de até ~90 palavras, manchete ou frase descritiva do município |
| `tarefas_sugeridas` | Tarefas de LLM aplicáveis, separadas por `;` |
| `n_palavras` | Tamanho do texto |

Volume com os arquivos de amostra: 24 documentos (15 indicadores, 6 notícias, 3 trechos
de texto; ~756 palavras). Com a coleta real o volume muda, principalmente em `texto` e `noticia`.

## 4. Mapeamento dados → tarefas de LLM (TP4)

| Tarefa | Documentos | Entrada | Saída esperada | Como avaliar |
|---|---|---|---|---|
| Resumo automático | `texto`, `noticia` | Trecho/notícia | ≤ 3 frases | Checagem manual de fidelidade (números e nomes preservados) |
| Classificação de sentimento | `noticia` | Manchete | positivo / negativo / neutro | Rotular à mão ~30 manchetes e comparar |
| Perguntas e respostas | todos | Pergunta + contexto recuperado | Resposta ancorada no contexto ou "Não sei" | Conjunto de perguntas com resposta conhecida (ex.: "Qual o IDEB de Três Lagoas?") |
| Geração de texto | `indicador` | Frases de indicadores | Parágrafo de relatório | Revisão qualitativa: sem números inventados |

Os prompts estão em `src/llm/prompts.py`, e a página "Preparação para LLM" do app permite
pré-visualizá-los. A recuperação de contexto atual (`retrieve`) usa sobreposição de
palavras como baseline; pode ser substituída por embeddings sem alterar o formato do corpus.

## 5. Qualidade e limitações

- A base de indicadores é uma **amostra de 15 municípios**, não a cobertura nacional (meta do Charter: ≥ 90%).
- Notícias refletem a janela corrente do feed RSS, sem histórico.
- Frases de indicador são geradas por template: servem a Q&A e geração, mas não contêm linguagem natural de fontes externas.
- Textos da Wikipédia são enciclopédicos, não dado estatístico oficial.

## 6. Próximos passos

- [x] Scraping com Beautiful Soup (TP2)
- [x] API FastAPI com GET/POST (TP3)
- [x] Corpus e prompts para LLM (TP3)
- [x] Avaliação do Selenium (TP3): não necessário
- [ ] Executar as 4 tarefas de LLM e avaliar resultados (TP4)
- [ ] Substituir a amostra por coleta completa INEP/SIDRA
- [ ] Calcular score ESG-educação composto
