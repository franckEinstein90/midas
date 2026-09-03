"""Seed reference data for local MIDAS development."""

from app.db.seed import seed_reference_data
from app.db.session import SessionLocal


def main() -> None:
    db = SessionLocal()
    try:
        seed_reference_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
