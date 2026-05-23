import json
from pathlib import Path

from src.ingest.bls_api import parse_bls_series
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
    assert records[0]["value"] == 4.1


def test_save_and_load_latest_bls_snapshot(tmp_path: Path):
    first = tmp_path / "bls_snapshot_20260523T100000Z.json"
    second = tmp_path / "bls_snapshot_20260523T110000Z.json"
    save_bls_snapshot({"status": "REQUEST_SUCCEEDED"}, first)
    save_bls_snapshot({"status": "REQUEST_SUCCEEDED", "Results": {}}, second)
    latest = load_latest_bls_snapshot(tmp_path)
    assert latest == second
    assert json.loads(latest.read_text(encoding="utf-8"))["status"] == "REQUEST_SUCCEEDED"
