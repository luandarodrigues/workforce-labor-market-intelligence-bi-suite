from pathlib import Path

import pandas as pd

from src.ingest.hr_source import find_hr_source_csv, normalize_hr_columns


def test_normalize_hr_columns_snake_cases_expected_fields():
    raw = pd.DataFrame(
        [{"EmployeeNumber": 1, "MonthlyIncome": 5000, "JobSatisfaction": 4, "Attrition": "Yes"}]
    )
    normalized = normalize_hr_columns(raw)
    assert {"employee_number", "monthly_income", "job_satisfaction", "attrition"} <= set(normalized.columns)
    assert normalized.loc[0, "attrition_flag"] == 1


def test_find_hr_source_csv_prefers_ibm_filename(tmp_path: Path):
    fallback = tmp_path / "other.csv"
    preferred = tmp_path / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    fallback.write_text("x\n1\n", encoding="utf-8")
    preferred.write_text("x\n1\n", encoding="utf-8")
    assert find_hr_source_csv(tmp_path) == preferred
