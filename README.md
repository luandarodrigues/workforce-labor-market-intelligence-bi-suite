# Workforce & Labor Market Intelligence BI Suite

An end-to-end analytics engineering project that combines internal HR data, labor market context, attrition risk scoring, and BI-ready outputs for workforce planning.

## Overview

This repository is designed as a BI product, not just an exploratory analysis or dashboard mockup. The project models workforce data into governed dimensions and facts, enriches that layer with labor market signals, scores employee attrition risk, and exports ready-to-consume assets for Power BI, Tableau, and warehouse-based analytics workflows.

Core business question:

How can a company combine internal people data with external labor market signals to make better decisions about retention, labor cost, and workforce planning?

## What The Project Delivers

- A local `DuckDB` warehouse with staged, dimensional, and fact tables
- A BI-ready consolidated dataset for `Power BI` and `Tableau`
- Executive KPI outputs for workforce planning
- Explainable attrition risk bands and recommendation logic
- Reusable metric documentation and interview-defensible project artifacts

## Current Source Status

- Internal HR source: real IBM HR attrition CSV loaded from `data/raw/internal`
- External labor market source: demo BLS-shaped structure until a live snapshot is persisted successfully

The pipeline already runs end to end with the real internal source and a modeled external layer.

## Architecture

The repository follows a layered analytics workflow:

1. `raw`
   Internal and external source files or snapshots
2. `staging`
   Standardized and normalized source tables
3. `marts`
   Dimensions and fact tables used by BI outputs
4. `modeling`
   Explainable attrition scoring and recommendation logic
5. `exports`
   BI-ready CSV and XLSX datasets plus documentation assets

Core execution stack:

- `Python` for orchestration, ingestion, exports, and documentation generation
- `SQL` for staging, marts, and KPI logic
- `DuckDB` for local warehouse materialization

## Repository Layout

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

## Raw Data Layout

Expected source locations:

- `data/raw/internal/WA_Fn-UseC_-HR-Employee-Attrition.csv`
- `data/raw/external/bls_snapshot_*.json`

Fallback behavior:

- If the IBM HR file is present, the pipeline uses it automatically
- If the IBM HR file is missing, the pipeline falls back to a demo HR dataset
- If a BLS snapshot is present, the pipeline uses the latest snapshot automatically
- If no BLS snapshot is present, the pipeline falls back to a demo labor market structure

## Run The Project

Run the full pipeline:

```bash
python -m src.app run-all
```

Fetch an external BLS snapshot:

```bash
python -m src.app fetch-external
```

Run tests:

```bash
python -m pytest -v
```

## Output Artifacts

The pipeline produces these files in `data/bi_exports/`:

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
- `pipeline_run_metadata.txt` generated locally during runs

Warehouse output:

- `warehouse/workforce_intelligence.duckdb`

Documentation output:

- `docs/business_problem.md`
- `docs/data_model.md`
- `docs/metric_definitions.md`
- `docs/model_card.md`
- `docs/external_data_sources.md`
- `docs/executive_summary.md`

## Sample Output Snapshot

Current run highlights:

- `1,470` employee-month records
- `16.12%` attrition rate
- `6,502.93` average monthly base pay
- `7.01` average tenure
- `5.00` median tenure
- `96.33%` training participation rate
- `28.30%` overtime rate
- `33` high-risk employees

The consolidated BI dataset includes fields such as:

- `department_name`
- `job_role`
- `role_family`
- `occupation_group`
- `attrition_probability`
- `risk_band`
- `main_risk_driver`
- `external_pressure_score`
- `retention_priority_index`

## Connect To BI Tools

For `Power BI`:

- Import `data/bi_exports/powerbi_ready_dataset.xlsx` for a single-file semantic dataset
- Or connect directly to `warehouse/workforce_intelligence.duckdb` if you want model-level flexibility

For `Tableau`:

- Import `data/bi_exports/tableau_ready_dataset.csv`
- Or connect to `warehouse/workforce_intelligence.duckdb` for custom joins and extracts

Recommended dashboard pages:

- Executive Overview
- Attrition Risk
- Labor Market Context

## Limitations

- The IBM HR source is a fictional educational dataset, not a production HRIS export
- The workforce model uses a simplified employee-month snapshot rather than true event history
- The external BLS layer is code-ready, but this environment has not yet materialized a live snapshot successfully
- The attrition scoring logic is a governed baseline, not a production-calibrated predictive model

## Documentation

- Business framing: [docs/business_problem.md](docs/business_problem.md)
- Data model: [docs/data_model.md](docs/data_model.md)
- Metric definitions: [docs/metric_definitions.md](docs/metric_definitions.md)
- Model card: [docs/model_card.md](docs/model_card.md)
- Executive summary: [docs/executive_summary.md](docs/executive_summary.md)

## Portfolio Positioning

This project is meant to demonstrate:

- analytics engineering structure
- governed metrics and semantic modeling
- BI-ready dataset delivery
- explainable attrition risk scoring
- workforce analytics storytelling with product framing
