# Contact CRUD App

FastAPI + SQLite contact management web app.

## Stack
- FastAPI (Python 3.12)
- SQLAlchemy + SQLite (`contacts.db` auto-created)
- HTML + JS frontend served from `app/index.html`

## Layout
- `app/main.py` — FastAPI routes
- `app/models.py` — SQLAlchemy models
- `app/database.py` — DB engine/session
- `app/index.html` — frontend UI
- `tests/test_api.py` — pytest API tests

## Run (Replit)
Workflow `Start application` runs:
```
uvicorn app.main:app --host 0.0.0.0 --port 5000
```
Serves on port 5000 (webview).

## Deployment
Configured for autoscale target via `deployConfig`.
