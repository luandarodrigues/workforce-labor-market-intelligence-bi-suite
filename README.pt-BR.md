# Workforce & Labor Market Intelligence BI Suite

Uma suite analitica com foco em BI que combina dados internos de RH, contexto do mercado de trabalho, camada de risco de turnover e entregaveis prontos para consumo em ferramentas analiticas.

## Versoes do README

- Ingles: `README.md`
- Portugues (Brasil): `README.pt-BR.md`

## Visao Geral

Este repositorio foi pensado como um produto analitico, e nao apenas como uma analise exploratoria ou um dashboard montado manualmente. A proposta e organizar dados de workforce em uma camada semantica governada, enriquecer essa base com sinais externos do mercado e entregar ativos reutilizaveis para planejamento de pessoas, retencao e custo.

Pergunta central de negocio:

Como uma empresa pode combinar sinais internos de pessoas com sinais externos do mercado para tomar decisoes melhores sobre retencao, custo de reposicao e planejamento da forca de trabalho?

## O Que O Projeto Entrega

- Um warehouse local em `DuckDB` com camadas de staging, dimensoes e fatos
- Um dataset consolidado pronto para `Power BI` e `Tableau`
- KPIs executivos voltados para workforce planning
- Score explicavel de risco de attrition com bandas de risco e recomendacoes
- Documentacao tecnica e de metricas pensada para portifolio e entrevista

## Status Atual Das Fontes

- Fonte interna de RH: CSV real do dataset IBM HR Attrition, carregado a partir de `data/raw/internal`
- Fonte externa de mercado de trabalho: estrutura modelada no formato BLS, com suporte para snapshots reais assim que o ambiente permitir persistencia completa

Hoje o pipeline ja roda de ponta a ponta com a fonte interna real e uma camada externa modelada.

## Arquitetura

O repositorio segue um fluxo analitico em camadas:

1. `raw`
   Arquivos de origem internos e externos
2. `staging`
   Padronizacao e normalizacao das fontes
3. `marts`
   Dimensoes e fatos usados pela camada de BI
4. `modeling`
   Logica explicavel de risco de attrition e recomendacoes
5. `exports`
   Arquivos prontos para BI e artefatos de documentacao

Stack principal:

- `Python` para orquestracao, ingestao, exports e geracao de documentacao
- `SQL` para staging, marts e logica de KPI
- `DuckDB` como warehouse local

## Estrutura Do Repositorio

```text
workforce-labor-market-bi-suite/
|-- data/
|   |-- raw/
|   |   |-- internal/
|   |   `-- external/
|   `-- bi_exports/
|-- docs/
|-- src/
|   |-- ingest/
|   |-- staging/
|   |-- marts/
|   |-- metrics/
|   `-- exports/
|-- tests/
`-- warehouse/
```

## Layout Dos Dados Brutos

Locais esperados para as fontes:

- `data/raw/internal/WA_Fn-UseC_-HR-Employee-Attrition.csv`
- `data/raw/external/bls_snapshot_*.json`

Comportamento de fallback:

- Se o arquivo do IBM HR estiver presente, o pipeline usa essa fonte automaticamente
- Se o arquivo do IBM HR estiver ausente, o pipeline usa um dataset demo de RH
- Se existir um snapshot do BLS, o pipeline usa o mais recente
- Se nao existir snapshot do BLS, o pipeline usa uma estrutura demo de mercado

## Como Rodar O Projeto

Executar o pipeline completo:

```bash
python -m src.app run-all
```

Buscar um snapshot externo do BLS:

```bash
python -m src.app fetch-external
```

Rodar os testes:

```bash
python -m pytest -v
```

## Artefatos Gerados

O pipeline gera estes arquivos em `data/bi_exports/`:

- `dim_employee.csv`
- `dim_department.csv`
- `dim_role.csv`
- `dim_region.csv`
- `dim_date.csv`
- `fact_employee_monthly.csv`
- `fact_attrition_risk.csv`
- `fact_labor_market_monthly.csv`
- `executive_kpis.csv`
- `tableau_ready_dataset.csv`
- `powerbi_ready_dataset.xlsx`
- `metrics_dictionary.xlsx`
- `pipeline_run_metadata.txt` gerado localmente a cada execucao

Saida do warehouse:

- `warehouse/workforce_intelligence.duckdb`

Saida de documentacao:

- `docs/business_problem.md`
- `docs/data_model.md`
- `docs/metric_definitions.md`
- `docs/model_card.md`
- `docs/external_data_sources.md`
- `docs/executive_summary.md`

## Snapshot Atual Dos Outputs

Resumo do ultimo run:

- `1.470` registros employee-month
- `16,12%` de attrition
- `6.502,93` de salario base medio mensal
- `7,01` anos de tenure medio
- `5,00` anos de tenure mediano
- `96,33%` de training participation rate
- `28,30%` de overtime rate
- `33` colaboradores em alto risco

O dataset consolidado de BI inclui campos como:

- `department_name`
- `job_role`
- `role_family`
- `occupation_group`
- `attrition_probability`
- `risk_band`
- `main_risk_driver`
- `external_pressure_score`
- `retention_priority_index`

## Conexao Com Ferramentas De BI

Para `Power BI`:

- importe `data/bi_exports/powerbi_ready_dataset.xlsx` para um dataset unico e pronto
- ou conecte diretamente em `warehouse/workforce_intelligence.duckdb` se quiser mais flexibilidade

Para `Tableau`:

- importe `data/bi_exports/tableau_ready_dataset.csv`
- ou conecte em `warehouse/workforce_intelligence.duckdb` para extracoes e joins customizados

Paginas recomendadas para dashboard:

- Executive Overview
- Attrition Risk
- Labor Market Context

## Limitacoes

- O dataset IBM HR e educacional e sintetico, nao um export real de HRIS corporativo
- O modelo de workforce usa um snapshot simplificado por colaborador e mes, nao um historico real de eventos
- A camada externa do BLS esta pronta em codigo, mas este ambiente ainda nao persistiu um snapshot live com sucesso
- A logica de risco de attrition e uma base governada e explicavel, nao um modelo calibrado para producao

## Documentacao

- Problema de negocio: [docs/business_problem.md](docs/business_problem.md)
- Modelo de dados: [docs/data_model.md](docs/data_model.md)
- Definicao de metricas: [docs/metric_definitions.md](docs/metric_definitions.md)
- Model card: [docs/model_card.md](docs/model_card.md)
- Resumo executivo: [docs/executive_summary.md](docs/executive_summary.md)

## Assets Para BI

- Guia do Tableau: [bi/tableau/tableau_build_guide.md](bi/tableau/tableau_build_guide.md)
- Blueprint do dashboard Tableau: [bi/tableau/dashboard_blueprint.md](bi/tableau/dashboard_blueprint.md)
- Calculated fields do Tableau: [bi/tableau/calculated_fields.md](bi/tableau/calculated_fields.md)
- Copy do dashboard publico: [bi/tableau/public_dashboard_copy.md](bi/tableau/public_dashboard_copy.md)
- Tema do Power BI: [bi/powerbi/workforce_intelligence_theme.json](bi/powerbi/workforce_intelligence_theme.json)
- Guia do tema Power BI: [bi/powerbi/theme_usage.md](bi/powerbi/theme_usage.md)

## Como Este Projeto Se Posiciona No Portfolio

Este projeto foi desenhado para mostrar:

- estrutura de analytics engineering
- modelagem semantica e metricas governadas
- entrega de datasets prontos para BI
- score explicavel de risco de attrition
- storytelling analitico com cara de produto
