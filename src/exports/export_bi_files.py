from __future__ import annotations

from pathlib import Path

import pandas as pd


def build_attrition_rate(attrition_count: int, headcount: int) -> float:
    return 0.0 if headcount == 0 else attrition_count / headcount


def build_consolidated_bi_dataset(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    fact_employee = frames["fact_employee_monthly"].copy()
    dim_employee = frames["dim_employee"].copy()
    dim_department = frames["dim_department"].copy()
    dim_role = frames["dim_role"].copy()
    dim_region = frames["dim_region"].copy()
    dim_date = frames["dim_date"].copy()
    fact_attrition_risk = frames["fact_attrition_risk"].copy()
    fact_labor_market = frames["fact_labor_market_monthly"].copy()

    region_labor_fallback = (
        fact_labor_market.groupby(["date_id", "region_id"], as_index=False)[
            ["unemployment_rate", "wage_index", "labor_demand_index", "external_pressure_score"]
        ]
        .mean()
        .rename(
            columns={
                "unemployment_rate": "region_unemployment_rate",
                "wage_index": "region_wage_index",
                "labor_demand_index": "region_labor_demand_index",
                "external_pressure_score": "region_external_pressure_score",
            }
        )
    )

    consolidated = (
        fact_employee.merge(dim_employee, on="employee_id", how="left")
        .merge(dim_department, on="department_id", how="left")
        .merge(dim_role, on="role_id", how="left")
        .merge(dim_region, on="region_id", how="left")
        .merge(dim_date, on="date_id", how="left")
        .merge(fact_attrition_risk, on=["employee_id", "date_id"], how="left")
        .merge(
            fact_labor_market,
            on=["date_id", "region_id", "occupation_group"],
            how="left",
            suffixes=("", "_occupation"),
        )
        .merge(region_labor_fallback, on=["date_id", "region_id"], how="left")
    )

    for metric_name in [
        "unemployment_rate",
        "wage_index",
        "labor_demand_index",
        "external_pressure_score",
    ]:
        consolidated[metric_name] = consolidated[metric_name].fillna(
            consolidated[f"region_{metric_name}"]
        )

    consolidated["role_criticality_score"] = (
        consolidated["role_criticality"]
        .map({"high": 1.0, "medium": 0.6, "low": 0.3})
        .fillna(0.6)
    )
    consolidated["attrition_risk_rate_flag"] = (
        consolidated["risk_band"].fillna("Low Risk").eq("High Risk").astype(int)
    )
    consolidated["retention_priority_index"] = (
        consolidated["attrition_probability"].fillna(0.0) * 0.5
        + consolidated["external_pressure_score"].fillna(0.0) * 0.3
        + consolidated["role_criticality_score"] * 0.2
    ).round(3)

    consolidated["record_type"] = "employee_month"

    ordered_columns = [
        "record_type",
        "employee_id",
        "date_id",
        "year",
        "quarter",
        "month",
        "region_id",
        "region_name",
        "region_type",
        "labor_market_code",
        "department_id",
        "department_name",
        "role_id",
        "job_role",
        "job_level",
        "role_family",
        "occupation_group",
        "role_criticality",
        "age_band",
        "gender",
        "education_level",
        "marital_status",
        "distance_from_home_band",
        "monthly_income",
        "annualized_income",
        "salary_band",
        "years_at_company",
        "years_in_current_role",
        "years_since_last_promotion",
        "overtime_flag",
        "training_times_last_year",
        "job_satisfaction",
        "environment_satisfaction",
        "work_life_balance",
        "performance_rating",
        "attrition_flag",
        "estimated_replacement_cost",
        "attrition_probability",
        "risk_band",
        "main_risk_driver",
        "recommended_action",
        "model_version",
        "attrition_risk_rate_flag",
        "unemployment_rate",
        "wage_index",
        "labor_demand_index",
        "external_pressure_score",
        "role_criticality_score",
        "retention_priority_index",
    ]
    return consolidated[ordered_columns].sort_values(["date_id", "employee_id"]).reset_index(drop=True)


def export_csv(df, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def export_excel(df, path: Path, sheet_name: str = "Sheet1") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False, sheet_name=sheet_name)
