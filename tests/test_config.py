from pathlib import Path

from src.app import build_parser
from src.utils.config import ProjectPaths, get_project_paths


def test_get_project_paths_uses_repo_root(tmp_path: Path):
    paths = get_project_paths(tmp_path)
    assert isinstance(paths, ProjectPaths)
    assert paths.data_raw == tmp_path / "data" / "raw"
    assert paths.data_raw_internal == tmp_path / "data" / "raw" / "internal"
    assert paths.data_raw_external == tmp_path / "data" / "raw" / "external"
    assert paths.warehouse_file == tmp_path / "warehouse" / "workforce_intelligence.duckdb"


def test_build_parser_includes_run_all_command():
    parser = build_parser()
    args = parser.parse_args(["run-all"])
    assert args.command == "run-all"


def test_build_parser_includes_fetch_external_command():
    parser = build_parser()
    args = parser.parse_args(["fetch-external"])
    assert args.command == "fetch-external"
