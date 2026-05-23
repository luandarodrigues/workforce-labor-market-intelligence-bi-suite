from pathlib import Path

import pandas as pd

from src.exports.build_executive_summary import write_executive_summary


def test_write_executive_summary_uses_exported_metrics(tmp_path: Path):
    exports_dir = tmp_path / "data" / "bi_exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(
        [
            {
                "headcount": 100,
                "attrition_rate": 0.12,
                "average_monthly_base_pay": 6200,
                "average_tenure": 6.5,
                "median_tenure": 5.0,
                "training_participation_rate": 0.91,
                "overtime_rate": 0.22,
            }
        ]
    ).to_csv(exports_dir / "executive_kpis.csv", index=False)
    pd.DataFrame(
        [
            {"employee_id": 1, "risk_band": "High Risk", "main_risk_driver": "Career progression"},
            {"employee_id": 2, "risk_band": "Low Risk", "main_risk_driver": "Mixed workforce factors"},
        ]
    ).to_csv(exports_dir / "fact_attrition_risk.csv", index=False)
    pd.DataFrame([{"estimated_replacement_cost": 50000}, {"estimated_replacement_cost": 60000}]).to_csv(
        exports_dir / "fact_employee_monthly.csv",
        index=False,
    )
    (exports_dir / "pipeline_run_metadata.txt").write_text(
        "hr_source=real_csv\nlabor_market_source=demo_bls_structure\n",
        encoding="utf-8",
    )

    output_path = docs_dir / "executive_summary.md"
    write_executive_summary(output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "12.00%" in content
    assert "High-risk employees: `1`" in content
    assert "real_csv" in content
