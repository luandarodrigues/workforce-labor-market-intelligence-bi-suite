from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


def build_metrics_dictionary(metric_rules_path: Path, output_path: Path) -> None:
    rules = yaml.safe_load(metric_rules_path.read_text(encoding="utf-8"))
    rows = [{"metric_name": key, **value} for key, value in rules.items()]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_excel(output_path, index=False)
