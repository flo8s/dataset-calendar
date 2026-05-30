"""祝日 CSV 取得 + dbt build + snapshot パイプライン。

Snapshot must run in the SAME Python process as dbt build — see
dataset-shared/README.md for the constraint detail.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import urllib.request
from pathlib import Path

from dbt.cli.main import dbtRunner

CSV_URL = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
CACHE_DIR = Path(".cache")
CSV_PATH = CACHE_DIR / "holidays.csv"

SHARED_SCRIPTS = Path(__file__).resolve().parent / "shared" / "scripts"
_spec = importlib.util.spec_from_file_location(
    "snapshot_to_r2", SHARED_SCRIPTS / "snapshot-to-r2.py"
)
assert _spec and _spec.loader
snapshot_to_r2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_to_r2)


def main() -> None:
    target = os.environ.get("DBT_TARGET", sys.argv[1] if len(sys.argv) > 1 else "default")

    _download_holidays()

    dbt = dbtRunner()
    for cmd in (
        ["deps"],
        ["build", "--target", target],
        ["docs", "generate", "--target", target],
    ):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {' '.join(cmd)} failed")

    snapshot_to_r2.run(target)


def _download_holidays() -> None:
    """内閣府の祝日 CSV をダウンロードし UTF-8 に変換して保存する。"""
    CACHE_DIR.mkdir(exist_ok=True)
    with urllib.request.urlopen(CSV_URL) as resp:
        data = resp.read()
    text = data.decode("cp932")
    CSV_PATH.write_text(text, encoding="utf-8")
    lines = text.strip().splitlines()
    print(f"  holidays.csv: {len(lines) - 1} holidays downloaded")


if __name__ == "__main__":
    main()
