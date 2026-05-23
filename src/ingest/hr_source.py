from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


def _to_snake(name: str) -> str:
    normalized = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return normalized.replace(" ", "_")


def normalize_hr_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.rename(columns={column: _to_snake(column) for column in df.columns}).copy()
    if "attrition" in renamed.columns:
        renamed["attrition_flag"] = renamed["attrition"].map({"Yes": 1, "No": 0})
    return renamed


def load_hr_source(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    normalized = normalize_hr_columns(df)
    if "monthly_income" in normalized.columns:
        normalized["annualized_income"] = normalized["monthly_income"] * 12
    if "over_time" in normalized.columns:
        normalized["overtime_flag"] = normalized["over_time"].map({"Yes": 1, "No": 0})
    normalized["region_id"] = "us_national"
    return normalized


def find_hr_source_csv(raw_internal_dir: Path) -> Path | None:
    preferred_names = [
        "WA_Fn-UseC_-HR-Employee-Attrition.csv",
        "ibm_hr_attrition.csv",
        "hr_attrition.csv",
    ]
    for name in preferred_names:
        candidate = raw_internal_dir / name
        if candidate.exists():
            return candidate
    csv_files = sorted(raw_internal_dir.glob("*.csv"))
    return csv_files[0] if csv_files else None


def load_preferred_hr_source(raw_internal_dir: Path) -> tuple[pd.DataFrame, str]:
    csv_path = find_hr_source_csv(raw_internal_dir)
    if csv_path is None:
        return build_demo_hr_source(), "demo"
    return load_hr_source(csv_path), str(csv_path)


def build_demo_hr_source() -> pd.DataFrame:
    raw = pd.DataFrame(
        [
            {
                "EmployeeNumber": 1,
                "Age": 34,
                "Department": "Sales",
                "JobRole": "Sales Executive",
                "MonthlyIncome": 5000,
                "YearsAtCompany": 5,
                "YearsInCurrentRole": 2,
                "YearsSinceLastPromotion": 1,
                "OverTime": "Yes",
                "TrainingTimesLastYear": 3,
                "JobSatisfaction": 3,
                "EnvironmentSatisfaction": 3,
                "WorkLifeBalance": 2,
                "PerformanceRating": 3,
                "Attrition": "Yes",
                "Gender": "Female",
                "Education": 3,
                "MaritalStatus": "Single",
                "DistanceFromHome": 8,
            },
            {
                "EmployeeNumber": 2,
                "Age": 41,
                "Department": "Research & Development",
                "JobRole": "Research Scientist",
                "MonthlyIncome": 7200,
                "YearsAtCompany": 8,
                "YearsInCurrentRole": 4,
                "YearsSinceLastPromotion": 3,
                "OverTime": "No",
                "TrainingTimesLastYear": 2,
                "JobSatisfaction": 4,
                "EnvironmentSatisfaction": 4,
                "WorkLifeBalance": 3,
                "PerformanceRating": 4,
                "Attrition": "No",
                "Gender": "Male",
                "Education": 4,
                "MaritalStatus": "Married",
                "DistanceFromHome": 12,
            },
            {
                "EmployeeNumber": 3,
                "Age": 29,
                "Department": "Human Resources",
                "JobRole": "Laboratory Technician",
                "MonthlyIncome": 4300,
                "YearsAtCompany": 2,
                "YearsInCurrentRole": 1,
                "YearsSinceLastPromotion": 0,
                "OverTime": "Yes",
                "TrainingTimesLastYear": 1,
                "JobSatisfaction": 2,
                "EnvironmentSatisfaction": 2,
                "WorkLifeBalance": 1,
                "PerformanceRating": 3,
                "Attrition": "Yes",
                "Gender": "Female",
                "Education": 2,
                "MaritalStatus": "Single",
                "DistanceFromHome": 5,
            },
        ]
    )
    normalized = normalize_hr_columns(raw)
    normalized["annualized_income"] = normalized["monthly_income"] * 12
    normalized["region_id"] = "us_national"
    normalized["overtime_flag"] = normalized["over_time"].map({"Yes": 1, "No": 0})
    return normalized
