from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib import request

DEFAULT_BLS_SERIES_IDS = [
    "LNS14000000",
]


def build_bls_date_id(year: int, period: str) -> int | None:
    if not period.startswith("M"):
        return None

    month = int(period[1:])
    if month < 1 or month > 12:
        return None
    return year * 100 + month


def parse_bls_series(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for series in payload.get("Results", {}).get("series", []):
        for point in series.get("data", []):
            date_id = build_bls_date_id(int(point["year"]), point["period"])
            if date_id is None:
                continue
            rows.append(
                {
                    "series_id": series["seriesID"],
                    "year": int(point["year"]),
                    "period": point["period"],
                    "date_id": date_id,
                    "value": float(point["value"]),
                }
            )
    return rows


def fetch_bls_series(series_ids: list[str], start_year: int, end_year: int) -> dict[str, Any]:
    payload = json.dumps(
        {"seriesid": series_ids, "startyear": str(start_year), "endyear": str(end_year)}
    ).encode("utf-8")
    http_request = request.Request(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(http_request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def build_bls_snapshot_path(raw_external_dir: Path) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return raw_external_dir / f"bls_snapshot_{timestamp}.json"


def save_bls_snapshot(payload: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def load_latest_bls_snapshot(raw_external_dir: Path) -> Path | None:
    snapshots = sorted(raw_external_dir.glob("bls_snapshot_*.json"))
    return snapshots[-1] if snapshots else None
