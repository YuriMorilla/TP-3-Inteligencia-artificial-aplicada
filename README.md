# EduAcesso ESG

Dashboard analítico para monitoramento de indicadores educacionais municipais com foco em equidade e ODS 4.

## Estrutura 

```
tp1_esg/
├── app/                    # Aplicação Streamlit
├── data/
│   ├── raw/                # Dados brutos (não versionados)
│   ├── processed/          # Dados limpos e transformados
│   └── external/           # Dados de terceiros
├── docs/
│   ├── project_charter/    # Project Charter
│   └── data_summary/       # Data Summary Report
├── notebooks/              # Exploração e análise
├── src/
│   ├── data/               # Scripts de coleta e limpeza
│   ├── features/           # Engenharia de features
│   ├── models/             # Modelagem e scoring
│   └── visualization/      # Componentes visuais
├── reports/figures/        # Gráficos exportados
├── tests/
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```


