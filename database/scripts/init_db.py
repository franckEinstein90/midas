"""Apply Alembic migrations and seed reference data via the backend."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"


def init_db() -> None:
    from midas_db.migrate import upgrade_head

    upgrade_head()

    result = subprocess.run(
        [sys.executable, str(BACKEND_DIR / "scripts" / "seed_db.py")],
        cwd=BACKEND_DIR,
        env=os.environ.copy(),
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    print("MIDAS PostgreSQL schema migrated and seeded.")


if __name__ == "__main__":
    init_db()
