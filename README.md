# StudySpark

A minimal Class 10 study space: syllabus checklist, practice quizzes, study planner and map-work tracker, with login. Flask + Supabase, ready for Render.

## Structure

```
app.py            Flask app: routes, auth, JSON API
data.py           Syllabus, quiz questions, map lists
schema.sql        Supabase tables + row-level security
requirements.txt  Dependencies
Procfile          Process command (gunicorn)
render.yaml       Optional Render blueprint
templates/        base, login, register, dashboard, syllabus, practice, planner, maps, 404
static/css|js     Styles and scripts
```

## 1. Supabase

1. Create a project at supabase.com.
2. SQL Editor → paste `schema.sql` → Run.
3. Project Settings → API: copy the **Project URL**, **anon** key and **service_role** key.
4. Authentication → Providers → Email. For quick testing, turn off "Confirm email"; otherwise new users must confirm by email before logging in.

## 2. Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then fill in the values
python app.py               # http://localhost:5000
```

## 3. Deploy on Render

1. Push this folder to GitHub.
2. Render → New → Web Service → pick the repo (or New → Blueprint to use `render.yaml`).
3. Build command: `pip install -r requirements.txt`. Start command: `gunicorn app:app` (Render reads this from the dashboard or `render.yaml`; the `Procfile` is there for Heroku-style platforms).
4. Add environment variables: `SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`.
5. Deploy. Health check path: `/healthz`.

## Notes

- The service-role key stays on the server only; never put it in templates or JS.
- Every query is filtered by the logged-in user's id, and RLS is enabled as a safety net.
- Syllabus lists follow the details you supplied; confirm with the official CBSE syllabus.
