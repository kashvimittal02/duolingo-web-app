# Duolingo Web App — Full-Stack SDE Implementation

An original, end-to-end full-stack language learning web application inspired by Duolingo. Built with a server-authoritative architecture where all grading, hearts, progression, daily streaks, XP, crowns, and gamification logic are strictly calculated and persisted on the backend.

---

## 1. Project Overview

This application provides an interactive Spanish A1 curriculum featuring:
- A progressive learning path with locked, available, and completed lessons.
- An interactive lesson player supporting 5 distinct exercise types.
- A deterministic gamification engine with hearts, passive heart regeneration, daily streaks (Asia/Kolkata), mock gem economy, and weekly league rankings.
- Timed "Legendary" Challenge mode with strict 90-second server countdown, no heart loss, and anti-farming XP protection.
- Duolingo-authentic Dark Mode with zero-flash initial paint and persistent local preference.
- Client-side Spanish Audio/TTS via Web Speech API and responsive sound effects via Web Audio API.
- 100% server authority: zero client-side evaluation, zero answers leaked in API payloads, and duplicate-safe, race-condition-resistant SQLite database transactions.

---

## 2. Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons, Canvas-Confetti
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy 2.0, Pydantic v2, Uvicorn
- **Database**: SQLite with Write-Ahead Logging (WAL mode) and enforced Foreign Keys
- **Testing**: Pytest, Playwright (end-to-end browser automation)

---

## 3. Architecture & Separation of Concerns

```
┌─────────────────────────────────────────────────────────────┐
│                   Next.js 14 Frontend                       │
│  - App Router (/ , /lesson/[id] , /leaderboard , /profile)  │
│  - 3D tactile UI design system (Tailwind CSS)               │
│  - Client state renders authoritative backend responses     │
│  - Reverse proxy /api/v1/* -> FastAPI backend              │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / JSON
┌──────────────────────────────▼──────────────────────────────┐
│                    FastAPI Backend                          │
│  - Session Engine: Cryptographic tokens (secrets.token)    │
│  - Sanitizer: Scrubs canonical answers before dispatch      │
│  - Validator Service: NFKD Unicode grading, match sets      │
│  - Concurrency Guard: SQLite WAL + conditional UPDATEs      │
│  - Timezone: Asia/Kolkata streak calculation                │
└──────────────────────────────┬──────────────────────────────┘
                               │ SQLAlchemy ORM (WAL mode)
┌──────────────────────────────▼──────────────────────────────┐
│                  SQLite Database (duolingo.db)              │
│  - 16 Normalized relational tables (incl. challenge tables) │
│  - Unique constraints prevent duplicate submissions/XP      │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions
1. **Server Authority**: The frontend never determines if an answer is correct, never awards XP directly, and never unlocks skills locally.
2. **Answer Scrubbing**: Canonical answers, accepted alternatives, and answer keys are scrubbed before payload transmission. Match-pairs exercises decouple left and right items with randomized IDs (`L_0`, `R_2`).
3. **Passive Heart Regeneration**: Heart recovery is deterministic (1 heart per 30 minutes). Pure read calls (`GET /learner/me`) compute effective hearts without database writes; mutating actions synchronize regenerated hearts atomically.
4. **SQLite Concurrency & Idempotency**:
   - Duplicate answer submissions are caught via `(session_id, exercise_id)` uniqueness within savepoint rollbacks (`db.begin_nested()`).
   - Lesson completions use conditional updates (`WHERE status = 'in_progress'`) and a unique constraint on `user_lesson_completions.session_id` to prevent double XP awards under concurrent requests.
5. **Streak Engine**: Calculated in the specified `Asia/Kolkata` timezone. Consecutive days increment streak; practicing on the same day maintains it; missed days reset streak to 1.

---

## 4. Project Structure

```
duolingo-app/
├── backend/
│   ├── app/
│   │   ├── models/            # SQLAlchemy models (user, course, exercise, session, challenge)
│   │   ├── routers/           # FastAPI endpoints (learner, path, session, leaderboard, challenge)
│   │   ├── schemas/           # Pydantic v2 validation DTOs (session, challenge, learner)
│   │   ├── seeds/             # Curriculum seeder (Spanish A1, default learner, rankings)
│   │   ├── services/          # Authoritative business logic (grading, sessions, streak, challenge)
│   │   ├── config.py          # Application settings & environment variables
│   │   ├── database.py        # SQLite engine with WAL pragma & session factory
│   │   └── main.py            # FastAPI app lifecycle & CORS configuration
│   ├── tests/                 # 57 automated unit, concurrency, and challenge tests
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── app/                   # Next.js App Router pages (/, /lesson/[id], /challenge/[id], /leaderboard, etc.)
│   ├── components/
│   │   ├── layout/            # TopHeader, Sidebar, BottomNav
│   │   ├── lesson/            # LessonHeader, FeedbackBar, Complete/Failed modals
│   │   │   └── exercises/     # Renderers for all 5 exercise types
│   │   ├── path/              # UnitHeader, SkillNode, LessonModal
│   │   ├── theme/             # ThemeProvider & Dark Mode toggle
│   │   └── ui/                # Tactile 3D Buttons, Cards, Modals, ProgressBars, AudioButton
│   ├── lib/                   # API client (lib/api.ts), types (lib/types.ts), audio (lib/audio.ts)
│   ├── public/                # Static brand assets and SVGs
│   ├── next.config.js         # Configurable reverse proxy rewrite rules
│   ├── package.json           # Frontend dependencies
│   └── tailwind.config.js     # Duolingo color palette and design tokens
├── .gitignore                 # Root gitignore excluding dependencies and runtime files
└── README.md                  # Project documentation
```

---

## 5. Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.17.0 or higher
- **npm**: 9.0.0 or higher

---

## 6. Installation & Setup

### A. Backend Setup

1. Open a terminal in the `backend/` directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   - **Windows**:
     ```powershell
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize and seed the SQLite database:
   ```bash
   python -m app.seeds.seeder --reset
   ```
   *(Creates tables and seeds Spanish A1 curriculum, achievements, leaderboard competitors, and default learner `duo_learner`)*.

5. Start the backend development server:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   - API Base: `http://127.0.0.1:8000`
   - Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

---

### B. Frontend Setup

1. Open a separate terminal in the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install npm dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   - Application URL: `http://localhost:3000`

4. *(Optional)* Build and run the production server:
   ```bash
   npm run build
   npm run start
   ```

---

## 7. API Specification Overview

All endpoints are prefixed with `/api/v1`:

| Method | Endpoint | Description | Auth / Access |
|---|---|---|---|
| `GET` | `/health` | Server health check and version | Public |
| `GET` | `/learner/me` | Fetch learner profile, hearts, gems, streak, daily XP, achievements | Authoritative user |
| `POST` | `/learner/refill-hearts` | Restore hearts to 5 for 350 gems | Authoritative user |
| `POST` | `/learner/practice-heart` | Free practice session (+1 heart, 0 XP) | Authoritative user |
| `GET` | `/courses/active/tree` | Learning path with units, skills, and locked/available/completed states | Authoritative user |
| `GET` | `/lessons/{id}/status` | Validate lesson availability and prerequisite locks | Authoritative user |
| `POST` | `/lessons/{id}/start` | Initialize lesson session; returns sanitized exercise payloads | Authoritative user |
| `POST` | `/lessons/sessions/{token}/answer` | Authoritatively grades answer; deducts hearts on error | Session owner |
| `POST` | `/lessons/sessions/{token}/complete` | Finalizes lesson; awards XP (15 first / 5 replay), crowns, streak | Session owner |
| `POST` | `/challenges/{lesson_id}/start` | Initialize Legendary timed challenge (90s server clock); returns sanitized exercises | Authoritative user |
| `GET` | `/challenges/sessions/{challenge_token}` | Authoritative challenge status, remaining countdown seconds, and expiry state | Session owner |
| `POST` | `/challenges/sessions/{challenge_token}/answer` | Evaluates challenge answer; strictly rejects late submissions past 90s server deadline | Session owner |
| `POST` | `/challenges/sessions/{challenge_token}/complete` | Finalizes challenge; awards +20 XP on first completion / 0 XP on replay; idempotent | Session owner |
| `GET` | `/leaderboard` | Weekly leaderboard standings (Sunday-to-Saturday XP) | Authoritative user |

Interactive API documentation with request schemas and live testing is available at `http://127.0.0.1:8000/docs`.

---

## 8. Exercise Types Supported

The application implements all 5 required exercise types with dedicated UI components and server validators:

1. **Multiple Choice** (`multiple_choice`): Single-choice selection with keyboard badges (`1`, `2`, `3`).
2. **Translate / Word Bank** (`word_bank`): Interactive token bank where tiles dynamically snap into the sentence assembly slot and can be returned by clicking.
3. **Match Pairs** (`match_pairs`): Two-column card matching with decoupled left/right item IDs (`L_x`, `R_y`), animated selection outlines, and bidirectional set validation.
4. **Fill in the Blank** (`fill_blank`): Sentence template with an inline blank slot filled by selectable options.
5. **Type the Answer** (`type_answer`): Freeform Spanish text input with a virtual Spanish accent bar (`á`, `é`, `í`, `ó`, `ú`, `ñ`, `¿`, `¡`) and NFKD Unicode normalization on the server.

### Timed "Legendary" Challenge Mode
In addition to standard lessons, learners can launch a Timed Legendary Challenge for any unlocked lesson (`/challenge/[id]`):
- **90-Second Server-Authoritative Timer**: Challenge deadline is tracked and strictly enforced on the server (`expires_at = started_at + 90s`). Answers submitted after time expires are rejected with HTTP 400.
- **No Strikes & No Heart Loss**: Challenges test speed; incorrect answers display corrections without deducting learner hearts and without a strikes limit.
- **Anti-Farming XP Rewards**: Completing the challenge awards **+20 XP** on first successful completion and **0 XP** on replay.
- **Completion Idempotency**: Subsequent completion calls return the completed state without granting duplicate XP.
- **Session Isolation**: Challenge sessions (`challenge_sessions` and `challenge_answers`) are tracked in dedicated tables completely isolated from standard lesson progress.

---

## 9. Seeded Content & Default Learner

The database seeder automatically configures:
- **Default Learner**:
  - Username: `duo_learner` (Alex Developer)
  - Initial State: 5 hearts, 500 gems, 5-day streak, 300+ lifetime XP
  - Progress: Skill 1 ("Greetings") completed (5 crowns); Skill 2 ("Food & Drinks") partially completed with Lesson 2 ("Daily Meals") available to play.
- **Curriculum**:
  - Course: Spanish A1 (`es-en`)
  - 2 Units: "Unit 1: Rookie Basics", "Unit 2: Daily Life"
  - 4 Skills: Greetings, Food & Drinks, Basic Phrases, Travel
  - 8 Lessons with 40 exercises covering all 5 exercise formats.
- **Leaderboard**: 9 seeded competitive learners with realistic weekly XP distribution.
- **Achievements**: 4 achievements ("First Steps", "Wildfire", "Centurion", "Flawless Victory").

---

## 10. Automated Tests

The backend test suite contains 57 comprehensive automated tests:

```bash
cd backend
venv\Scripts\python -m pytest -v
```

### Test Coverage Highlights:
- `test_phase1_database.py` (12 tests): Relational schema integrity, foreign key cascades, unique constraints, seeder idempotency.
- `test_phase2_apis.py` (15 tests): Passive heart regeneration without database mutation, gem deduction, free practice, course tree status transitions, weekly leaderboard XP aggregation, Asia/Kolkata streak continuation.
- `test_phase3_lesson_engine.py` (24 tests):
  - Lock enforcement: 403 on locked lessons or 0 hearts.
  - Payload sanitization: verified absence of `canonical_answer`, `accepted_answers`, `answer_key`.
  - Server grading for all 5 exercise types.
  - Multi-threaded concurrency tests under SQLite WAL mode: concurrent duplicate wrong answers (single heart loss), concurrent duplicate correct answers, concurrent completion race conditions.
- `test_phase4_legendary_mode.py` (6 tests):
  - 90-second server countdown deadline enforcement.
  - Late answer rejection past server expiry.
  - First-time Legendary bonus (+20 XP) and anti-farming replay protection (0 XP).
  - Idempotent completion and session isolation from normal lessons.

---

## 11. Environment Configuration

### Backend Variables (`backend/.env` or system environment):
```bash
DATABASE_URL=sqlite:///./duolingo.db    # SQLite database connection URL
DEFAULT_TIMEZONE=Asia/Kolkata           # Timezone for streaks and daily boundaries
MAX_HEARTS=5                            # Maximum learner hearts capacity
HEART_REGEN_SECONDS=1800                # Passive heart regeneration interval (30 min)
GEM_REFILL_COST=350                     # Cost to refill hearts with gems
BASE_LESSON_XP=15                       # XP awarded for first-time completion
REPLAY_LESSON_XP=5                      # XP awarded for replay completion
ALLOW_DEV_USER_OVERRIDE=false           # Dev security flag for X-User-Id header override
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000   # Comma-separated allowed origins
```

### Frontend Variables (`frontend/.env.local` or deployment settings):
```bash
# Internal backend URL used by the Next.js server reverse proxy:
BACKEND_INTERNAL_URL=http://127.0.0.1:8000

# Optional public override for client-side fetches (defaults to /api/v1 in browser):
NEXT_PUBLIC_API_URL=
```

---

## 12. Deployment Instructions

1. **Backend Deployment (e.g. Render, Railway, Fly.io, Docker)**:
   - Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Set `CORS_ORIGINS` to the deployed frontend domain.
2. **Frontend Deployment (e.g. Vercel, Netlify)**:
   - Root directory: `frontend`
   - Set `BACKEND_INTERNAL_URL` to the public or private URL of your deployed backend (e.g. `https://my-backend.onrender.com`).
   - The Next.js reverse proxy (`/api/v1/:path*`) automatically forwards requests to the configured backend.

---

## 13. Known Assumptions & Scope Decisions

- **Authentication**: As permitted by the assignment specification, authentication defaults to the seeded learner `duo_learner` without requiring user registration or passwords.
- **Audio / TTS & Sound Effects**: Fully implemented client-side using native browser Web Speech API (`window.speechSynthesis` prioritizing `es-ES` Spanish pronunciation) and the Web Audio API (harmonic synthesizer for correct/incorrect responses and completion celebrations). Includes interactive audio replay buttons and global sound muting toggle.
- **Currency**: Gems are mock currency seeded with the learner; no real payments or external billing APIs are integrated.
