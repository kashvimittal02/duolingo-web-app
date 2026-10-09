from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

def get_utc_now() -> datetime:
    """Returns current naive UTC datetime for cross-platform SQLite compatibility (Python 3.12+ safe)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

# Ensure target directory exists for SQLite database URL
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_raw_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if db_raw_path:
        parent_dir = Path(db_raw_path).parent
        if parent_dir and not parent_dir.exists():
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

# SQLite-specific connect args
connect_args = {"check_same_thread": False, "timeout": 30.0}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

# Enable foreign keys and WAL mode on SQLite connections
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency generator that yields a database session and closes it cleanly."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
