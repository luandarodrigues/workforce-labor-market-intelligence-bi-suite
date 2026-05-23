import json
from pathlib import Path

from src.app import _load_labor_market_source
from src.ingest.bls_api import build_bls_date_id, parse_bls_series
from src.ingest.bls_api import load_latest_bls_snapshot, save_bls_snapshot


def test_parse_bls_series_flattens_monthly_points():
    payload = {
        "Results": {
            "series": [
                {
                    "seriesID": "TEST",
                    "data": [{"year": "2024", "period": "M01", "value": "4.1"}],
                }
            ]
        }
    }
    records = parse_bls_series(payload)
    assert records[0]["series_id"] == "TEST"
    assert records[0]["year"] == 2024
    assert records[0]["period"] == "M01"
    assert records[0]["date_id"] == 202401
    assert records[0]["value"] == 4.1


def test_build_bls_date_id_ignores_non_monthly_periods():
    assert build_bls_date_id(2024, "M01") == 202401
    assert build_bls_date_id(2024, "M12") == 202412
    assert build_bls_date_id(2024, "M13") is None


def test_load_labor_market_source_expands_snapshot_to_configured_occupation_groups(tmp_path: Path):
    save_bls_snapshot(
        {
            "Results": {
                "series": [
                    {
                        "seriesID": "LNS14000000",
                        "data": [{"year": "2024", "period": "M02", "value": "4.0"}],
                    }
                ]
            }
        },
        tmp_path / "bls_snapshot_20260523T110000Z.json",
    )

    frame, source_name = _load_labor_market_source(
        tmp_path,
        ["Computer and Mathematical", "Sales Occupations"],
    )

    assert source_name.endswith(".json")
    assert set(frame["occupation_group"]) == {"Computer and Mathematical", "Sales Occupations"}
    assert set(frame["date_id"]) == {202402}


def test_save_and_load_latest_bls_snapshot(tmp_path: Path):
    first = tmp_path / "bls_snapshot_20260523T100000Z.json"
    second = tmp_path / "bls_snapshot_20260523T110000Z.json"
    save_bls_snapshot({"status": "REQUEST_SUCCEEDED"}, first)
    save_bls_snapshot({"status": "REQUEST_SUCCEEDED", "Results": {}}, second)
    latest = load_latest_bls_snapshot(tmp_path)
    assert latest == second
    assert json.loads(latest.read_text(encoding="utf-8"))["status"] == "REQUEST_SUCCEEDED"
