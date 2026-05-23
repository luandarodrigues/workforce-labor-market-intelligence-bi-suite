import json
from pathlib import Path

from src.exports.build_case_payload import build_case_payload


def test_build_case_payload_returns_summary_filters_and_rows(tmp_path: Path):
    payload = build_case_payload(
        exports_dir=Path("data/bi_exports"),
        output_path=tmp_path / "workforce_case_payload.json",
    )

    assert "summary" in payload
    assert "filters" in payload
    assert "rows" in payload
    assert "headcount" in payload["summary"]
    assert "department_name" in payload["filters"]
    assert payload["rows"]
    assert "main_risk_driver" in payload["rows"][0]
    assert "recommended_action" in payload["rows"][0]
    assert "unemployment_rate" in payload["rows"][0]
    assert (tmp_path / "workforce_case_payload.json").exists()


def test_build_case_payload_writes_valid_json_without_nan_literals(tmp_path: Path):
    output_path = tmp_path / "workforce_case_payload.json"
    build_case_payload(
        exports_dir=Path("data/bi_exports"),
        output_path=output_path,
    )

    raw = output_path.read_text(encoding="utf-8")
    parsed = json.loads(raw)

    assert "NaN" not in raw
    assert any(row["occupation_group"] is None for row in parsed["rows"])
