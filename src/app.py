"""CLI entrypoint for the workforce analytics project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb
import pandas as pd

from src.exports.build_executive_summary import write_executive_summary
from src.exports.build_metrics_dictionary import build_metrics_dictionary
from src.exports.export_bi_files import build_consolidated_bi_dataset, export_csv, export_excel
from src.ingest.bls_api import (
    DEFAULT_BLS_SERIES_IDS,
    build_bls_snapshot_path,
    fetch_bls_series,
    load_latest_bls_snapshot,
    parse_bls_series,
    save_bls_snapshot,
)
from src.ingest.hr_source import load_preferred_hr_source
from src.utils.config import get_project_paths
from src.utils.io import ensure_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run-all")
    subparsers.add_parser("fetch-external")
    return parser


def _build_labor_market_raw() -> pd.DataFrame:
    rows = [
        {
            "date_id": 202401,
            "region_id": "us_national",
            "occupation_group": "Sales Occupations",
            "series_id": "BLS_SALES",
            "year": 2024,
            "period": "M01",
            "unemployment_rate": 4.2,
            "wage_index": 1.03,
            "labor_demand_index": 1.01,
            "external_pressure_score": 0.62,
        },
        {
            "date_id": 202401,
            "region_id": "us_national",
            "occupation_group": "Computer and Mathematical",
            "series_id": "BLS_COMP",
            "year": 2024,
            "period": "M01",
            "unemployment_rate": 2.7,
            "wage_index": 1.10,
            "labor_demand_index": 1.08,
            "external_pressure_score": 0.44,
        },
        {
            "date_id": 202401,
            "region_id": "us_national",
            "occupation_group": "Healthcare Practitioners",
            "series_id": "BLS_HEALTH",
            "year": 2024,
            "period": "M01",
            "unemployment_rate": 3.1,
            "wage_index": 1.06,
            "labor_demand_index": 1.05,
            "external_pressure_score": 0.57,
        },
    ]
    return pd.DataFrame(rows)


def _load_labor_market_source(raw_external_dir: Path) -> tuple[pd.DataFrame, str]:
    snapshot_path = load_latest_bls_snapshot(raw_external_dir)
    if snapshot_path is None:
        return _build_labor_market_raw(), "demo_bls_structure"

    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    parsed = parse_bls_series(payload)
    if not parsed:
        return _build_labor_market_raw(), f"empty_snapshot:{snapshot_path.name}"

    rows = []
    for record in parsed:
        rows.append(
            {
                "date_id": int(f"{record['year']}01"),
                "region_id": "us_national",
                "occupation_group": "All Occupations",
                "series_id": record["series_id"],
                "year": record["year"],
                "period": record["period"],
                "unemployment_rate": record["value"],
                "wage_index": 1.0,
                "labor_demand_index": 1.0,
                "external_pressure_score": min(1.0, max(0.0, record["value"] / 10)),
            }
        )
    return pd.DataFrame(rows), str(snapshot_path)


def _execute_sql_file(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    con.execute(path.read_text(encoding="utf-8"))


def _fetch_table(con: duckdb.DuckDBPyConnection, table_name: str) -> pd.DataFrame:
    return con.execute(f"select * from {table_name}").fetchdf()


def run_all() -> None:
    paths = get_project_paths(Path.cwd())
    ensure_directory(paths.data_raw_internal)
    ensure_directory(paths.data_raw_external)
    ensure_directory(paths.data_exports)
    ensure_directory(paths.warehouse_file.parent)

    hr_df, hr_source_name = load_preferred_hr_source(paths.data_raw_internal)
    labor_market_raw, labor_market_source_name = _load_labor_market_source(paths.data_raw_external)
    role_mapping = pd.read_csv(Path(__file__).resolve().parent / "staging" / "role_market_mapping.csv")

    con = duckdb.connect(str(paths.warehouse_file))
    con.register("hr_raw_df", hr_df)
    con.register("labor_market_raw_df", labor_market_raw)
    con.register("role_market_mapping_df", role_mapping)
    con.execute("create or replace table hr_raw as select * from hr_raw_df")
    con.execute("create or replace table labor_market_raw as select * from labor_market_raw_df")
    con.execute("create or replace table role_market_mapping as select * from role_market_mapping_df")

    sql_root = Path(__file__).resolve().parent
    for relative_path in [
        "staging/stage_hr.sql",
        "staging/stage_labor_market.sql",
        "marts/dim_department.sql",
        "marts/dim_role.sql",
        "marts/dim_region.sql",
        "marts/dim_date.sql",
        "marts/dim_employee.sql",
        "marts/fact_employee_monthly.sql",
        "marts/fact_labor_market_monthly.sql",
        "marts/fact_attrition_risk.sql",
        "metrics/build_kpis.sql",
    ]:
        _execute_sql_file(con, sql_root / relative_path)

    export_table_names = [
        "dim_employee",
        "dim_department",
        "dim_role",
        "dim_region",
        "dim_date",
        "fact_employee_monthly",
        "fact_attrition_risk",
        "fact_labor_market_monthly",
        "executive_kpis",
    ]
    exported_frames = {name: _fetch_table(con, name) for name in export_table_names}
    con.close()

    for name, frame in exported_frames.items():
        export_csv(frame, paths.data_exports / f"{name}.csv")

    consolidated_bi_dataset = build_consolidated_bi_dataset(exported_frames)
    export_csv(consolidated_bi_dataset, paths.data_exports / "tableau_ready_dataset.csv")
    export_excel(
        consolidated_bi_dataset,
        paths.data_exports / "powerbi_ready_dataset.xlsx",
        sheet_name="workforce_bi",
    )

    build_metrics_dictionary(
        Path("src/metrics/metric_rules.yml"),
        paths.data_exports / "metrics_dictionary.xlsx",
    )
    write_executive_summary(Path("docs/executive_summary.md"))
    (paths.data_exports / "pipeline_run_metadata.txt").write_text(
        f"hr_source={hr_source_name}\n"
        f"labor_market_source={labor_market_source_name}\n",
        encoding="utf-8",
    )
    print("Running end-to-end workforce analytics pipeline")


def fetch_external() -> None:
    paths = get_project_paths(Path.cwd())
    ensure_directory(paths.data_raw_external)
    payload = fetch_bls_series(DEFAULT_BLS_SERIES_IDS, start_year=2024, end_year=2024)
    snapshot_path = save_bls_snapshot(payload, build_bls_snapshot_path(paths.data_raw_external))
    print(f"Saved external snapshot to {snapshot_path}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "run-all":
        run_all()
        return
    if args.command == "fetch-external":
        fetch_external()
        return
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
