# Event Trigger Platform

[![tests](https://github.com/SAMARTHJAISWAL/backend-assignment-segwise/actions/workflows/tests.yml/badge.svg)](https://github.com/SAMARTHJAISWAL/backend-assignment-segwise/actions/workflows/tests.yml)

A FastAPI backend (plus a small static frontend) for managing event triggers, built as a backend assignment for Segwise. Triggers are either **scheduled** (fire once at a given time) or **api** (stored definitions), and every firing is written to an event log that is archived after 2 hours and deleted after 48 hours.

## Features

- Create, list and delete triggers (`api` or `scheduled`), protected by an `X-API-KEY` header.
- Scheduled triggers are registered with APScheduler when created, fire once at `schedule_time`, log an event and are then marked inactive. Pending ones are re-registered when the server restarts.
- `POST /test/` fires an ad-hoc test trigger with any JSON payload without saving a trigger (logged with `trigger_id` 0).
- Event logs with pagination, an active/archived view, and per-trigger counts.
- Retention job every 10 minutes: events older than 2 hours are archived, events older than 48 hours are deleted.
- Optional Redis cache for event listings, invalidated on every write. If Redis is not reachable the API falls back to the database.
- Static HTML/JS frontend in `frontend/` for creating triggers and browsing logs.

Not implemented: recurring/interval triggers, editing triggers, and an endpoint that fires a saved `api` trigger.

## Tech stack

Python 3.12, FastAPI, SQLAlchemy 2, SQLite, APScheduler 3, Redis (optional), Pydantic v2 / pydantic-settings, pytest. Frontend is plain HTML/CSS/JS served by nginx in Docker.

## Run locally

```bash
git clone https://github.com/SAMARTHJAISWAL/backend-assignment-segwise.git
cd backend-assignment-segwise
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # set SECRET_API_KEY
uvicorn app.main:app --reload
```

The API is at <http://127.0.0.1:8000> and Swagger UI at <http://127.0.0.1:8000/docs>. Tables are created automatically on startup.

To use the frontend, set `apiKey` in `frontend/config.js` to the same value as `SECRET_API_KEY`, then serve the folder:

```bash
cd frontend && python -m http.server 5500
# open http://127.0.0.1:5500
```

### With Docker Compose

```bash
SECRET_API_KEY=change-me docker compose up --build
```

Backend on port 8000, frontend on 5500, Redis on 6379.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./event_triggers.db` | SQLAlchemy database URL |
| `SECRET_API_KEY` | `change-me` | Value required in the `X-API-KEY` header for `/triggers` |
| `REDIS_HOST` | `localhost` | Redis host for the event cache |
| `REDIS_PORT` | `6379` | Redis port |
| `CACHE_ENABLED` | `true` | Set `false` to skip Redis entirely |
| `CACHE_EXPIRATION` | `3600` | Cache TTL in seconds |
| `ACTIVE_RETENTION_HOURS` | `2` | Age at which events are archived |
| `TOTAL_RETENTION_HOURS` | `48` | Age at which events are deleted |

## API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/` | no | Health/welcome message |
| `POST` | `/triggers/` | `X-API-KEY` | Create a trigger |
| `GET` | `/triggers/` | `X-API-KEY` | List triggers |
| `DELETE` | `/triggers/{trigger_id}` | `X-API-KEY` | Delete a trigger and its logs (404 if missing) |
| `GET` | `/events/?archived=false&page=1&limit=10` | no | Paginated event logs, newest first |
| `GET` | `/events/aggregate` | no | Event count per `trigger_id` |
| `POST` | `/test/` | no | Fire a test trigger with any JSON body |

Create a scheduled trigger:

```bash
curl -X POST http://127.0.0.1:8000/triggers/ \
  -H "X-API-KEY: change-me" -H "Content-Type: application/json" \
  -d '{"name": "Reminder", "type": "scheduled", "payload": "hello", "schedule_time": "2030-01-26T15:00:00"}'
```

`schedule_time` is interpreted in the server's local time zone; event `timestamp` values are stored and returned in UTC.

Fire a test trigger:

```bash
curl -X POST http://127.0.0.1:8000/test/ -H "Content-Type: application/json" -d '{"key": "value"}'
```

## Helper scripts

Run from the repo root with `python -m`:

| Command | What it does |
|---------|--------------|
| `python -m scripts.init_db` | Create tables |
| `python -m scripts.populate_events` | Insert sample events, including some older than 48 hours |
| `python -m scripts.run_cleanup` | Run the archive and delete jobs once |
| `python -m scripts.verify_db` | Print all event logs |
| `python -m scripts.check_cache` | Round-trip a value through Redis |
| `python -m scripts.demo_scheduler` | Schedule three jobs 10/20/30 s out and watch them fire |

## Tests

Tests use a throwaway SQLite file and disable Redis, so no services are needed.

```bash
pip install -r requirements-dev.txt
pytest
```

## Project structure

```
app/
  main.py            # FastAPI app, lifespan (create tables, start scheduler)
  config.py          # settings from env / .env
  models.py          # Trigger, EventLog
  schemas.py         # Pydantic request/response models
  crud/              # DB helpers
  routes/            # /triggers, /events, /test
  services/scheduler.py  # APScheduler jobs: scheduled triggers + retention
  utils/             # auth, db session, Redis cache, time helper
frontend/            # static UI (index.html, script.js, config.js, styles.css)
scripts/             # maintenance / demo scripts
tests/               # pytest suite
```

## Deployment

The original submission was deployed with the frontend on Vercel (<https://backend-assignment-segwise.vercel.app/>) and the backend on Render free tier (<https://backend-assignment-segwise.onrender.com/>). On Render, set `SECRET_API_KEY` in the service environment and keep `frontend/config.js` in sync. Free-tier Render services sleep when idle, so the first request can take a while.

## Assumptions

- Triggers can be deleted but not edited or paused.
- Scheduled triggers are one-time.
- Event logs live for 48 hours in total: 2 hours active, then 46 hours archived.
- The frontend's API key is visible to anyone who loads the page; it is a demo gate, not real authentication.
