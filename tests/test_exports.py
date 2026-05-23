from pathlib import Path

import pandas as pd

from src.app import run_all
from src.exports.export_bi_files import build_consolidated_bi_dataset, export_csv


def test_export_csv_writes_file(tmp_path: Path):
    output = tmp_path / "bi_exports" / "sample.csv"
    export_csv(pd.DataFrame([{"x": 1}]), output)
    assert output.exists()


def test_build_consolidated_bi_dataset_enriches_employee_fact():
    frames = {
        "fact_employee_monthly": pd.DataFrame(
            [
                {
                    "employee_id": 1,
                    "department_id": 10,
                    "role_id": 20,
                    "region_id": "us_national",
                    "date_id": 202401,
                    "monthly_income": 5000,
                    "annualized_income": 60000,
                    "salary_band": "Mid",
                    "years_at_company": 4,
                    "years_in_current_role": 2,
                    "years_since_last_promotion": 3,
                    "overtime_flag": 1,
                    "training_times_last_year": 2,
                    "job_satisfaction": 2,
                    "environment_satisfaction": 3,
                    "work_life_balance": 2,
                    "performance_rating": 3,
                    "attrition_flag": 1,
                    "estimated_replacement_cost": 48000,
                }
            ]
        ),
        "dim_employee": pd.DataFrame(
            [
                {
                    "employee_id": 1,
                    "age_band": "30-39",
                    "gender": "Female",
                    "education_level": 3,
                    "marital_status": "Single",
                    "distance_from_home_band": "6-10",
                }
            ]
        ),
        "dim_department": pd.DataFrame([{"department_id": 10, "department_name": "Research & Development"}]),
        "dim_role": pd.DataFrame(
            [
                {
                    "role_id": 20,
                    "job_role": "Research Scientist",
                    "job_level": 1,
                    "role_family": "Science",
                    "occupation_group": "Computer and Mathematical",
                    "role_criticality": "high",
                }
            ]
        ),
        "dim_region": pd.DataFrame(
            [
                {
                    "region_id": "us_national",
                    "region_name": "United States",
                    "region_type": "country",
                    "labor_market_code": "US",
                }
            ]
        ),
        "dim_date": pd.DataFrame([{"date_id": 202401, "month": 1, "quarter": 1, "year": 2024}]),
        "fact_attrition_risk": pd.DataFrame(
            [
                {
                    "employee_id": 1,
                    "date_id": 202401,
                    "attrition_probability": 0.72,
                    "risk_band": "High Risk",
                    "main_risk_driver": "Career progression",
                    "recommended_action": "Prioritize career progression review",
                    "model_version": "baseline_v1",
                }
            ]
        ),
        "fact_labor_market_monthly": pd.DataFrame(
            [
                {
                    "date_id": 202401,
                    "region_id": "us_national",
                    "occupation_group": "Computer and Mathematical",
                    "unemployment_rate": 2.7,
                    "wage_index": 1.1,
                    "labor_demand_index": 1.08,
                    "external_pressure_score": 0.44,
                }
            ]
        ),
    }

    consolidated = build_consolidated_bi_dataset(frames)

    assert "department_name" in consolidated.columns
    assert "retention_priority_index" in consolidated.columns
    assert consolidated.loc[0, "job_role"] == "Research Scientist"
    assert consolidated.loc[0, "risk_band"] == "High Risk"
    assert consolidated.loc[0, "external_pressure_score"] == 0.44
    assert consolidated.loc[0, "attrition_risk_rate_flag"] == 1


def test_run_all_creates_core_export_files(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for folder in ["src/metrics", "docs"]:
        (tmp_path / folder).mkdir(parents=True, exist_ok=True)
    (tmp_path / "src/metrics/metric_rules.yml").write_text(
        "headcount:\n  category: standard\n  formula: active employees in reference month\n",
        encoding="utf-8",
    )

    run_all()

    expected = [
        tmp_path / "data" / "bi_exports" / "fact_employee_monthly.csv",
        tmp_path / "data" / "bi_exports" / "fact_attrition_risk.csv",
        tmp_path / "data" / "bi_exports" / "fact_labor_market_monthly.csv",
        tmp_path / "data" / "bi_exports" / "dim_employee.csv",
        tmp_path / "data" / "bi_exports" / "executive_kpis.csv",
        tmp_path / "data" / "bi_exports" / "tableau_ready_dataset.csv",
        tmp_path / "data" / "bi_exports" / "powerbi_ready_dataset.xlsx",
        tmp_path / "warehouse" / "workforce_intelligence.duckdb",
    ]
    for path in expected:
        assert path.exists()

    tableau_ready = pd.read_csv(tmp_path / "data" / "bi_exports" / "tableau_ready_dataset.csv")
    assert {"department_name", "job_role", "risk_band", "retention_priority_index"}.issubset(
        tableau_ready.columns
    )
