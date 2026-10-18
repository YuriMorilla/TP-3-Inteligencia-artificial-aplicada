# Documentação da API — EduAcesso ESG (TP3)

API REST construída com **FastAPI** que expõe os dados do projeto. Código em `api/main.py`;
a lógica de dados é compartilhada com o app Streamlit (`src/data/store.py`).

## Como rodar

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload        # na raiz do projeto
```

- Swagger interativo: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Rotas

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Status do serviço |
| GET | `/municipios` | Lista indicadores. Filtros: `uf`, `ano`, `ideb_min`, `limit` (padrão 100) |
| GET | `/municipios/{nome}` | Consulta por nome (ignora acentos e maiúsculas). 404 se não existir |
| POST | `/municipios` | Cadastra novo registro. 201 em sucesso, 409 se (município, ano) já existe, 422 se inválido |
| GET | `/estatisticas` | Totais, IDEB/abandono médios e agregados por UF |
| GET | `/noticias` | Notícias coletadas via Beautiful Soup (`fonte_real` indica se veio do scraper ou da amostra) |
| GET | `/corpus` | Documentos prontos para LLM. Filtro `tipo` = `texto`, `noticia` ou `indicador` |

## Exemplos

```bash
# Consulta com filtros
curl "http://localhost:8000/municipios?uf=MS&ideb_min=5.2"

# Consulta por nome
curl "http://localhost:8000/municipios/tres%20lagoas"

# Envio de novo registro
curl -X POST http://localhost:8000/municipios -H "Content-Type: application/json" -d '{
  "municipio": "Aparecida do Taboado", "uf": "MS",
  "ideb_anos_iniciais": 5.1, "ideb_anos_finais": 4.2,
  "taxa_abandono_pct": 3.0, "escolas_internet_pct": 70,
  "pib_per_capita": 25000, "ano": 2024
}'
```

## Validações do POST

| Campo | Regra |
|---|---|
| `municipio` | texto, mínimo 2 caracteres |
| `uf` | 2 letras (convertida para maiúscula) |
| `ideb_anos_iniciais`, `ideb_anos_finais` | 0 a 10 |
| `taxa_abandono_pct`, `escolas_internet_pct` | 0 a 100 |
| `pib_per_capita` | ≥ 0 |
| `ano` | 2000 a 2100 |

## Persistência

Registros enviados via POST são gravados em `data/processed/municipios_api.csv`
(ignorado pelo Git; caminho configurável pela variável `EDUACESSO_API_CSV`).
O dashboard lê esse arquivo junto com a base de amostra, então um POST aparece
no app após "Recarregar base" na página Upload / Download.

## Testes

```bash
pip install -r requirements-dev.txt
python -m pytest -q tests
```
