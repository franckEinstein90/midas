"""Install IANA timezone data for pgembed's bundled PostgreSQL."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def pgembed_share_dir() -> Path:
    import pgembed

    return Path(pgembed.__file__).resolve().parent / "pginstall" / "share" / "postgresql"


def pgembed_timezone_dir() -> Path:
    return pgembed_share_dir() / "timezone"


def _timezone_source_candidates() -> list[Path]:
    candidates: list[Path] = []

    try:
        import pgserver

        candidates.append(
            Path(pgserver.__file__).resolve().parent
            / "pginstall"
            / "share"
            / "postgresql"
            / "timezone"
        )
    except ImportError:
        pass

    repo_root = Path(__file__).resolve().parents[2]
    projects_root = repo_root.parent

    candidates.extend(
        [
            projects_root
            / "cyrus"
            / "cyrus_data"
            / ".venv"
            / "Lib"
            / "site-packages"
            / "pgserver"
            / "pginstall"
            / "share"
            / "postgresql"
            / "timezone",
            projects_root
            / "careerAgent"
            / "careerAgent_data"
            / "node_modules"
            / "@embedded-postgres"
            / "windows-x64"
            / "native"
            / "share"
            / "timezone",
        ]
    )

    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.exists() and any(resolved.iterdir()):
            unique.append(resolved)
    return unique


def timezones_installed() -> bool:
    tz_dir = pgembed_timezone_dir()
    return tz_dir.exists() and (tz_dir / "America" / "Toronto").exists()


def ensure_pgembed_timezones() -> bool:
    """Copy timezone data into pgembed if missing. Returns True when installed."""
    if timezones_installed():
        return False

    dest = pgembed_timezone_dir()
    for source in _timezone_source_candidates():
        if not (source / "America" / "Toronto").exists():
            continue

        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, dest)
        logger.info("Installed PostgreSQL timezone data from %s", source)
        return True

    raise RuntimeError(
        "pgembed is missing IANA timezone data (DBeaver sends America/Toronto on connect). "
        "Run midas-db start again after installing timezone data, or copy a timezone "
        "directory from another embedded-Postgres install."
    )
