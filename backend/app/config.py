import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "Duolingo App API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # SQLite Database file location
    DB_PATH: Path = BASE_DIR / "duolingo.db"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    
    # Timezone & Gamification Constants
    DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
    MAX_HEARTS: int = int(os.getenv("MAX_HEARTS", "5"))
    HEART_REGEN_SECONDS: int = int(os.getenv("HEART_REGEN_SECONDS", "1800"))  # 30 minutes
    GEM_REFILL_COST: int = int(os.getenv("GEM_REFILL_COST", "350"))
    BASE_LESSON_XP: int = int(os.getenv("BASE_LESSON_XP", "15"))
    REPLAY_LESSON_XP: int = int(os.getenv("REPLAY_LESSON_XP", "5"))
    PRACTICE_HEART_XP: int = 0  # 0 XP to prevent practice heart farming
    
    # Dev / Test Security Flags
    ALLOW_DEV_USER_OVERRIDE: bool = os.getenv("ALLOW_DEV_USER_OVERRIDE", "false").lower() in ("true", "1", "yes")
    
    # CORS
    CORS_ORIGINS: list[str] = (
        [origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()]
        if os.getenv("CORS_ORIGINS")
        else [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
        ]
    )

settings = Settings()
