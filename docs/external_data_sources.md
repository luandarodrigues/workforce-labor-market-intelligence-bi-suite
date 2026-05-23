# External Data Sources

## Intended Production Sources

The version 1 external layer is designed around United States labor market data from:

- `BLS Public Data API` for monthly series
- `BLS OEWS` tables for occupation and wage context

## Current Pipeline Behavior

Expected raw location:

- `data/raw/external/bls_snapshot_*.json`

Current behavior:

- `python -m src.app fetch-external` attempts to fetch and persist a BLS snapshot
- `python -m src.app run-all` reuses the latest saved snapshot automatically
- If no snapshot exists, the pipeline falls back to a demo BLS-shaped structure so the project remains executable

## Current State

In the current environment, the code path is ready for live BLS ingestion, but a real snapshot has not yet been persisted successfully because of environment-specific fetch issues. This means the warehouse and BI exports already support the external schema, but the current run still uses demo market values.

## Why The External Layer Exists

The purpose of the labor market layer is to move the project beyond descriptive HR reporting. It supports questions such as:

- which functions are exposed to stronger market pull
- where compensation pressure may be rising
- which roles combine internal risk with external competition

This is also the basis for composite product metrics such as:

- `external_pressure_score`
- `retention_priority_index`
