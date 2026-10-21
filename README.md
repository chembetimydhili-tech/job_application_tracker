# Job Application Tracker — Full Stack

A portfolio starter using React + Vite for the frontend, FastAPI for the backend, SQLAlchemy for database access, SQLite by default, and optional PostgreSQL.

## Features
- Account registration and login with hashed passwords and JWT bearer tokens
- User-specific application records
- Create, list, edit, and delete job applications
- Status tracking: Applied, Interview, Assessment, Offer, Rejected
- Search and status filtering
- Dashboard totals and status counts
- Responsive dark gradient interface

## Requirements
Python 3.10+, Node.js and npm.

## Start backend (Windows)
```bat
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

SQLite database file is created automatically. To use PostgreSQL, set `DATABASE_URL` before starting the backend, for example:
`postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/job_tracker`

## Start frontend (second terminal)
```bat
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite (normally http://localhost:5173).

Optional frontend API URL: create `frontend/.env` with `VITE_API_URL=http://127.0.0.1:8000`.

## Important
This is a learning project starter, not production-hardened software. Test it locally before publishing it as complete. For deployment, set a unique long `SECRET_KEY`, configure `FRONTEND_ORIGIN`, and review auth/security settings. Do not put real credentials or secrets in GitHub.
