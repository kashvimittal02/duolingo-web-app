from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal, ensure_schema_compatibility
from app.seeds.seeder import seed_database
from app.models.course import Course
from app.routers import learner, path, leaderboard, session, challenge, practice

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hook to ensure database initialization and auto-seeding on boot."""
    Base.metadata.create_all(bind=engine)
    ensure_schema_compatibility(engine)
    db = SessionLocal()
    try:
        # Check if database has curriculum seeded; if not, seed automatically
        course_count = db.query(Course).count()
        if course_count == 0:
            seed_database(db, reset=False)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for Duolingo-inspired full-stack web application.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health checks
@app.get("/health", tags=["Health"])
@app.get(f"{settings.API_V1_PREFIX}/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

# Register API v1 Routers
app.include_router(learner.router, prefix=settings.API_V1_PREFIX)
app.include_router(path.router, prefix=settings.API_V1_PREFIX)
app.include_router(leaderboard.router, prefix=settings.API_V1_PREFIX)
app.include_router(session.router, prefix=settings.API_V1_PREFIX)
app.include_router(challenge.router, prefix=settings.API_V1_PREFIX)
app.include_router(practice.router, prefix=settings.API_V1_PREFIX)
