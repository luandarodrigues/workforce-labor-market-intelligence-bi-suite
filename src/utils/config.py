from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data_raw: Path
    data_raw_internal: Path
    data_raw_external: Path
    data_staging: Path
    data_mart: Path
    data_exports: Path
    warehouse_file: Path


def get_project_paths(root: Path | None = None) -> ProjectPaths:
    resolved_root = (root or Path(__file__).resolve().parents[2]).resolve()
    return ProjectPaths(
        root=resolved_root,
        data_raw=resolved_root / "data" / "raw",
        data_raw_internal=resolved_root / "data" / "raw" / "internal",
        data_raw_external=resolved_root / "data" / "raw" / "external",
        data_staging=resolved_root / "data" / "staging",
        data_mart=resolved_root / "data" / "mart",
        data_exports=resolved_root / "data" / "bi_exports",
        warehouse_file=resolved_root / "warehouse" / "workforce_intelligence.duckdb",
    )
