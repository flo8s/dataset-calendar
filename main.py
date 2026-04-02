"""祝日 CSV 取得 + dbt ビルド + メタデータ生成パイプライン。"""

import urllib.request
from pathlib import Path

from dbt.cli.main import dbtRunner

CSV_URL = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
FDL_DIR = Path(".fdl")
CSV_PATH = FDL_DIR / "holidays.csv"


def main():
    _download_holidays()

    dbt = dbtRunner()

    result = dbt.invoke(["deps"])
    if not result.success:
        raise SystemExit("dbt deps failed")

    result = dbt.invoke(["run"])
    if not result.success:
        raise SystemExit("dbt run failed")

    result = dbt.invoke(["docs", "generate"])
    if not result.success:
        raise SystemExit("dbt docs generate failed")


def _download_holidays() -> None:
    """内閣府の祝日 CSV をダウンロードし UTF-8 に変換して保存する。"""
    FDL_DIR.mkdir(exist_ok=True)
    with urllib.request.urlopen(CSV_URL) as resp:
        data = resp.read()
    text = data.decode("cp932")
    CSV_PATH.write_text(text, encoding="utf-8")
    lines = text.strip().splitlines()
    print(f"  holidays.csv: {len(lines) - 1} holidays downloaded")


if __name__ == "__main__":
    main()
