# Project Charter — EduAcesso ESG

**Versão:** 3.0  
**Data:** 2026-10-18  
**Metodologia:** TDSP + CRISP-DM  

> Changelog v3: app Streamlit reorganizado em múltiplas páginas com menu de
> navegação (`st.navigation`); API FastAPI com 6 rotas (GET/POST) documentada
> em `docs/api/`; avaliação formal do Selenium (não adotado, ver seção 9);
> corpus unificado e templates de prompt preparados para as tarefas de LLM do
> TP4; testes automatizados (pytest). Problema de negócio reavaliado (seção 1.1).
> Seções 5, 7, 8 atualizadas e seção 9 (decisões técnicas) adicionada.
>
> Changelog v2: ambiente de desenvolvimento configurado (branch `tp2`,
> `requirements.txt` ampliado); interface Streamlit evoluída para abas
> dinâmicas com cache e estado de sessão; nova fonte de dados via
> Beautiful Soup (Wikipédia + Google News RSS); serviço de upload/download
> de CSV adicionado. Seções 1–4 e 6 mantidas da v1; seções 5, 7 e 8
> atualizadas para refletir o escopo do TP2.

---

## 1. Problema de Negócio

O Brasil apresenta profundas desigualdades no acesso à educação de qualidade, especialmente em municípios de pequeno porte e regiões periféricas. Estudantes de baixa renda enfrentam barreiras como ausência de internet, falta de dispositivos e escassez de conteúdo adequado. Dados do IBGE (2023) apontam que mais de 4 milhões de crianças e adolescentes estão fora da escola.

**Problema central:** Ausência de uma ferramenta analítica integrada que permita monitorar indicadores educacionais municipais com foco em equidade, subsidiando decisões de gestores públicos, ONGs e pesquisadores.

### 1.1 Reavaliação do problema de negócio (TP3)

Com a API e o corpus preparado, o problema deixa de ser só "visualizar indicadores"
e passa a incluir **integrar os dados a outros sistemas** (a API permite que
secretarias, ONGs ou outros painéis consultem e enviem registros) e **gerar
interpretação textual** sobre eles (LLM, TP4). A meta 3 (insights via LLM)
permanece, agora com base de dados e prompts definidos. Nenhum objetivo foi
removido; a meta 1 (cobertura ≥ 90% dos municípios) segue dependente da coleta
completa via INEP/SIDRA, hoje representada por uma amostra de 15 municípios.

---

## 2. Objetivos do Projeto

| # | Objetivo | Indicador de Sucesso |
|---|----------|----------------------|
| 1 | Consolidar dados educacionais públicos (INEP, IBGE) por município | Dataset limpo com cobertura ≥ 90% dos municípios brasileiros |
| 2 | Identificar municípios em situação crítica de acesso | Ranking com score ESG-educação por município |
| 3 | Gerar insights via LLM sobre causas e recomendações | Relatórios automatizados aprovados em testes qualitativos |
| 4 | Dashboard interativo para tomada de decisão | NPS ≥ 8 em teste com usuários-alvo |

---

## 3. ODS Atendido

**ODS 4 — Educação de Qualidade**  
*"Assegurar a educação inclusiva e equitativa e de qualidade, e promover oportunidades de aprendizagem ao longo da vida para todas e todos."*

**Justificativa:** O projeto endereça diretamente as metas 4.1 (educação primária e secundária gratuita, equitativa e de qualidade) e 4.5 (eliminação de disparidades de gênero e garantia de acesso igualitário para grupos vulneráveis), usando dados públicos para tornar visível o que hoje é invisível para gestores municipais.

**ODS Secundário:** ODS 10 — Redução das Desigualdades (monitoramento de equidade por renda e raça).

---

## 4. Público-Alvo

| Perfil | Necessidade |
|--------|-------------|
| Gestores municipais de educação | Comparar seu município com pares e identificar gaps |
| ONGs e institutos sociais | Priorizar alocação de recursos em regiões críticas |
| Pesquisadores e jornalistas de dados | Acesso rápido a séries históricas e análises contextualizadas |
| Formuladores de políticas públicas | Embasamento para programas nacionais |

---

## 5. Escopo

**Incluído:**
- Coleta automatizada via APIs do INEP (Censo Escolar) e IBGE (SIDRA)
- Coleta de conteúdo web via Beautiful Soup (Wikipédia e Google News RSS) para nuvem de palavras e tabela de notícias
- Dashboard Streamlit com filtros dinâmicos (UF, faixa de IDEB) por estado, município e ano
- Cache (`st.cache_data`/`st.cache_resource`) e estado de sessão (`st.session_state`) para performance e persistência
- Serviço de upload (CSV) e download (CSV) de dados diretamente na interface
- Aplicação Streamlit multipágina (Início, Indicadores, Notícias, Upload/Download, API, Preparação para LLM)
- API FastAPI (`api/main.py`) com consulta (GET) e envio (POST) de dados, documentada em `docs/api/`
- Corpus unificado (`data/processed/corpus_llm.*`) e templates de prompt (`src/llm/prompts.py`) para resumo, sentimento, Q&A e geração de texto
- Score ESG-educação composto por múltiplos indicadores
- Execução das tarefas de LLM (TP4; em TP3 apenas a preparação)

**Excluído:**
- Dados privados de escolas particulares
- Recomendações pedagógicas específicas por escola

---

## 6. Stakeholders

| Papel | Responsabilidade |
|-------|-----------------|
| Desenvolvedor / Data Scientist | Coleta, análise, modelagem e dashboard |
| Orientador (Infnet) | Revisão técnica e metodológica |
| Usuário final (gestores/ONGs) | Validação de usabilidade e relevância |

---

## 7. Fases TDSP × CRISP-DM

| TDSP | CRISP-DM | Entregável |
|------|----------|-----------|
| Business Understanding | Business Understanding | Este Project Charter |
| Data Acquisition | Data Understanding | Data Summary Report v1, v2 e v3 |
| Modeling | Modeling | Score ESG + análise LLM (TP4) |
| Deployment | Evaluation + Deployment | App Streamlit publicado (Community Cloud) |
| Acceptance | — | Relatório final + documentação |

**Progresso no TP2:** ambiente de desenvolvimento e Git configurados;
interface interativa (filtros, abas, upload/download) implementada;
coleta de conteúdo web (Beautiful Soup) integrada como segunda fonte de
dados; cache e estado de sessão implementados para performance.

**Progresso no TP3:** app multipágina; API FastAPI com testes; corpus e prompts
para LLM; documentação revisada (Charter v3, Data Summary v3, `docs/api/`).

---

## 8. Riscos

| Risco | Probabilidade | Mitigação |
|-------|--------------|-----------|
| API do INEP indisponível | Média | Cache local em CSV + dados do repositório oficial |
| Dados municipais incompletos | Alta | Imputação estatística + flag de qualidade |
| Escopo crescente | Média | Foco no MVP para TP1; features avançadas em TPs futuros |
| Mudança de layout do site coletado (Wikipédia/Google News) | Baixa-Média | Arquivos de amostra em `data/raw/*_sample.*` garantem funcionamento do app mesmo se o scraper falhar |
| Upload de CSV com schema inválido | Média | Validação de colunas obrigatórias antes de mesclar os dados |
| API não disponível no deploy do Streamlit Community Cloud | Alta | A página "API FastAPI" informa quando a API está fora do ar; o dashboard lê os mesmos dados direto de `src/data/store.py`, sem depender da API em execução |
| Custo/limites de LLM na próxima etapa | Média | Corpus pequeno e fragmentado em trechos curtos; recuperação de contexto antes do prompt reduz tokens |
| Respostas de LLM sem lastro nos dados (alucinação) | Média | Prompt de Q&A restringe a resposta ao contexto e exige "Não sei" quando ausente |

---

## 9. Decisões técnicas (TP3)

| Decisão | Justificativa |
|---|---|
| **Selenium não adotado** | Todas as fontes atuais (Wikipédia, Google News RSS, amostra IDEB) são estáticas e atendidas por `requests` + Beautiful Soup. Selenium exige navegador/driver, torna o deploy mais frágil e é mais lento. Será reavaliado se uma fonte de dados passar a depender de JavaScript (ex.: portais com filtros dinâmicos do INEP). |
| `st.navigation` em vez de pasta `pages/` | Menu agrupado por seção, controle explícito de ordem e ícones, entrada única (`app/main.py`) |
| Camada de dados única (`src/data/store.py`) | Streamlit, API e scripts compartilham a mesma lógica sem depender de Streamlit/FastAPI, o que simplifica testes |
| Persistência em CSV para o POST | Suficiente para o escopo acadêmico e coerente com o requisito de dados em `data/`; migrar para banco se houver uso concorrente |
| Corpus com 3 tipos de documento (texto, notícia, indicador) | Cobre as 4 tarefas de LLM previstas: resumo, sentimento, Q&A e geração |
