from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.config import get_project_paths
from src.utils.io import ensure_parent


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _format_decimal(value: float) -> str:
    return f"{value:.2f}"


def _load_metadata(metadata_path: Path) -> dict[str, str]:
    if not metadata_path.exists():
        return {}

    metadata: dict[str, str] = {}
    for line in metadata_path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def write_executive_summary(path: Path) -> None:
    ensure_parent(path)
    project_root = path.resolve().parents[1]
    paths = get_project_paths(project_root)

    executive_kpis_path = paths.data_exports / "executive_kpis.csv"
    attrition_risk_path = paths.data_exports / "fact_attrition_risk.csv"
    employee_fact_path = paths.data_exports / "fact_employee_monthly.csv"
    metadata_path = paths.data_exports / "pipeline_run_metadata.txt"

    if not executive_kpis_path.exists():
        path.write_text(
            "# Executive Summary\n\nPipeline run completed, but KPI exports were not found.\n",
            encoding="utf-8",
        )
        return

    kpis = pd.read_csv(executive_kpis_path).iloc[0]
    risk = pd.read_csv(attrition_risk_path) if attrition_risk_path.exists() else pd.DataFrame()
    employee_fact = pd.read_csv(employee_fact_path) if employee_fact_path.exists() else pd.DataFrame()
    metadata = _load_metadata(metadata_path)

    high_risk_count = int(risk["risk_band"].eq("High Risk").sum()) if not risk.empty else 0
    medium_risk_count = int(risk["risk_band"].eq("Medium Risk").sum()) if not risk.empty else 0
    low_risk_count = int(risk["risk_band"].eq("Low Risk").sum()) if not risk.empty else 0
    top_risk_driver = (
        risk["main_risk_driver"].value_counts().idxmax() if not risk.empty else "Not available"
    )
    estimated_replacement_cost = (
        float(employee_fact["estimated_replacement_cost"].sum()) if not employee_fact.empty else 0.0
    )
    hr_source = metadata.get("hr_source", "unknown")
    labor_market_source = metadata.get("labor_market_source", "unknown")

    path.write_text(
        "\n".join(
            [
                "# Executive Summary",
                "",
                "## Overview",
                "",
                "This repository delivers a BI-ready workforce analytics product that combines internal HR data, labor market context, explainable attrition risk scoring, and reusable semantic outputs for downstream dashboards.",
                "",
                "## Current Pipeline Output",
                "",
                f"- Headcount: `{int(kpis['headcount'])}` employee-month records",
                f"- Attrition rate: `{_format_percent(float(kpis['attrition_rate']))}`",
                f"- Average monthly base pay: `{_format_decimal(float(kpis['average_monthly_base_pay']))}`",
                f"- Average tenure: `{_format_decimal(float(kpis['average_tenure']))}` years",
                f"- Median tenure: `{_format_decimal(float(kpis['median_tenure']))}` years",
                f"- Training participation rate: `{_format_percent(float(kpis['training_participation_rate']))}`",
                f"- Overtime rate: `{_format_percent(float(kpis['overtime_rate']))}`",
                f"- Estimated replacement cost pool: `{_format_decimal(estimated_replacement_cost)}`",
                "",
                "## Risk Layer",
                "",
                f"- High-risk employees: `{high_risk_count}`",
                f"- Medium-risk employees: `{medium_risk_count}`",
                f"- Low-risk employees: `{low_risk_count}`",
                f"- Most common modeled driver: `{top_risk_driver}`",
                "",
                "## Source Status",
                "",
                f"- Internal HR source: `{hr_source}`",
                f"- External labor market source: `{labor_market_source}`",
                "",
                "## Interpretation",
                "",
                "The current build is strong enough to support executive BI questions around workforce composition, attrition concentration, risk segmentation, compensation pressure, and retention prioritization. The internal HR layer is already running on the real IBM attrition source, while the external layer remains ready for live BLS snapshots once the environment-specific fetch issue is resolved.",
                "",
            ]
        ),
        encoding="utf-8",
    )
