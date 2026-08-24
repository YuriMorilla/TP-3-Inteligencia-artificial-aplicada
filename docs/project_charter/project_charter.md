# Project Charter — EduAcesso ESG

**Versão:** 1.0  
**Data:** 2026-08-24  
**Metodologia:** TDSP + CRISP-DM  

---

## 1. Problema de Negócio

O Brasil apresenta profundas desigualdades no acesso à educação de qualidade, especialmente em municípios de pequeno porte e regiões periféricas. Estudantes de baixa renda enfrentam barreiras como ausência de internet, falta de dispositivos e escassez de conteúdo adequado. Dados do IBGE (2023) apontam que mais de 4 milhões de crianças e adolescentes estão fora da escola.

**Problema central:** Ausência de uma ferramenta analítica integrada que permita monitorar indicadores educacionais municipais com foco em equidade, subsidiando decisões de gestores públicos, ONGs e pesquisadores.

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
- Dashboard Streamlit com filtros por estado, município e ano
- Score ESG-educação composto por múltiplos indicadores
- Geração de análise textual via LLM (TP futuro)

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
| Data Acquisition | Data Understanding | Data Summary Report v1 |
| Modeling | Modeling | Score ESG + análise LLM |
| Deployment | Evaluation + Deployment | App Streamlit publicado |
| Acceptance | — | Relatório final + documentação |

---

## 8. Riscos

| Risco | Probabilidade | Mitigação |
|-------|--------------|-----------|
| API do INEP indisponível | Média | Cache local em CSV + dados do repositório oficial |
| Dados municipais incompletos | Alta | Imputação estatística + flag de qualidade |
| Escopo crescente | Média | Foco no MVP para TP1; features avançadas em TPs futuros |
