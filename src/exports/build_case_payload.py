from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _sorted_unique_values(series: pd.Series) -> list[str]:
    return sorted(str(value) for value in series.dropna().astype(str).unique().tolist())


def _json_ready_records(dataset: pd.DataFrame) -> list[dict]:
    selected = dataset[
        [
            "employee_id",
            "department_name",
            "job_role",
            "risk_band",
            "salary_band",
            "years_at_company",
            "attrition_flag",
            "attrition_probability",
            "estimated_replacement_cost",
            "external_pressure_score",
            "retention_priority_index",
            "occupation_group",
            "overtime_flag",
            "main_risk_driver",
            "recommended_action",
            "unemployment_rate",
            "wage_index",
            "labor_demand_index",
        ]
    ].copy()

    records = selected.to_dict(orient="records")

    # Browser consumers need valid JSON values; pandas NaN would otherwise be dumped as invalid JS tokens.
    normalized_records = []
    for record in records:
        normalized_records.append(
            {
                key: (None if pd.isna(value) else value)
                for key, value in record.items()
            }
        )

    return normalized_records


def build_case_payload(exports_dir: Path, output_path: Path) -> dict:
    dataset = pd.read_csv(exports_dir / "tableau_ready_dataset.csv")
    kpis = pd.read_csv(exports_dir / "executive_kpis.csv").iloc[0].to_dict()

    payload = {
        "summary": {
            "headcount": int(dataset["employee_id"].nunique()),
            "attrition_rate": float(kpis["attrition_rate"]),
            "high_risk_employees": int(dataset["risk_band"].eq("High Risk").sum()),
            "average_tenure": float(kpis["average_tenure"]),
            "estimated_replacement_cost": float(dataset["estimated_replacement_cost"].sum()),
            "external_pressure_score": float(dataset["external_pressure_score"].mean()),
        },
        "filters": {
            "department_name": _sorted_unique_values(dataset["department_name"]),
            "job_role": _sorted_unique_values(dataset["job_role"]),
            "risk_band": _sorted_unique_values(dataset["risk_band"]),
            "salary_band": _sorted_unique_values(dataset["salary_band"]),
        },
        "rows": _json_ready_records(dataset),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
