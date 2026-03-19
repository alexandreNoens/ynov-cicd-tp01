import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "students.db"
SCHEMA_PATH = ROOT_DIR / "sql" / "provisioning.sql"
DEV_DATA_PATH = ROOT_DIR / "sql" / "dev-data.sql"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)


def reset_db() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        dev_data = DEV_DATA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.executescript(dev_data)
