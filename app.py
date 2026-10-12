"""StudySpark – a minimal Class 10 study space (Flask + Supabase)."""
import logging
import os
import re
import secrets
from datetime import date, timedelta
from functools import wraps

from dotenv import load_dotenv
from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from supabase import create_client
from werkzeug.exceptions import HTTPException

from data import ALL_KEYS, MAP_GROUPS, QUIZZES, SUBJECTS

load_dotenv()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=bool(os.environ.get("RENDER")),  # HTTPS only on Render
    PERMANENT_SESSION_LIFETIME=timedelta(days=14),
    MAX_CONTENT_LENGTH=64 * 1024,
)
logging.basicConfig(level=logging.INFO)

SUBJECT_NAMES = [s["name"] for s in SUBJECTS]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# --------------------------------------------------------------------------
# Supabase
# --------------------------------------------------------------------------
def _env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


_db = None


def db():
    """Server-side client (service role). Never expose this key to the browser.
    Every query below is filtered by the logged-in user's id."""
    global _db
    if _db is None:
        _db = create_client(_env("SUPABASE_URL"), _env("SUPABASE_SERVICE_KEY"))
    return _db


def auth_client():
    """Fresh anon client per auth call so sessions never leak between users."""
    return create_client(_env("SUPABASE_URL"), _env("SUPABASE_ANON_KEY"))


# --------------------------------------------------------------------------
# Security helpers
# --------------------------------------------------------------------------
def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def verify_csrf():
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        sent = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token") or ""
        expected = session.get("csrf", "")
        if not expected or not secrets.compare_digest(sent.encode(), expected.encode()):
            abort(400)


@app.after_request
def security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            if request.path.startswith("/api/"):
                return jsonify(error="Please log in again."), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def uid():
    return session["user"]["id"]


def bad(message, code=400):
    return jsonify(error=message), code


# --------------------------------------------------------------------------
# Data helpers
# --------------------------------------------------------------------------
def get_done(user_id):
    rows = (db().table("progress").select("item_key")
            .eq("user_id", user_id).eq("done", True).execute().data)
    return {r["item_key"] for r in rows}


def get_plans(user_id):
    return (db().table("plans")
            .select("id,task,subject,due_date,done")
            .eq("user_id", user_id).order("created_at").execute().data)


def summarise(done):
    stats, done_total, total = [], 0, 0
    for s in SUBJECTS:
        n = sum(1 for g in s["groups"] for t in g["topics"] if t["key"] in done)
        stats.append({
            "name": s["name"], "icon": s["icon"], "accent": s["accent"],
            "done": n, "total": s["total"],
            "pct": round(n / s["total"] * 100) if s["total"] else 0,
        })
        done_total += n
        total += s["total"]
    percent = round(done_total / total * 100) if total else 0
    return stats, done_total, total, percent


# --------------------------------------------------------------------------
# Auth pages
# --------------------------------------------------------------------------
def _auth_error(exc, action="log in"):
    """Turn a Supabase auth exception into a message a student can act on."""
    text = str(exc).lower()
    if "email not confirmed" in text:
        return "Your email isn't confirmed yet. Open the confirmation email from Supabase, then log in."
    if "invalid login credentials" in text:
        return "Wrong email or password. If you haven't signed up yet, create an account first."
    if "already registered" in text or "already been registered" in text:
        return "That email is already registered. Try logging in instead."
    if "rate limit" in text or "too many" in text:
        return "Too many attempts. Please wait a minute and try again."
    if "invalid api key" in text or "apikey" in text or "jwt" in text:
        return "The server's Supabase keys look wrong. Check SUPABASE_URL and SUPABASE_ANON_KEY in your .env file."
    if "password" in text and ("weak" in text or "least" in text):
        return "That password is too weak. Try a longer one."
    if any(w in text for w in ("connect", "name or service", "getaddrinfo", "timed out", "resolve")):
        return "Couldn't reach Supabase. Check SUPABASE_URL in your .env file and your internet connection."
    return f"Couldn't {action}. Please try again."


def _start_session(user):
    meta = getattr(user, "user_metadata", None) or {}
    session.clear()
    session.permanent = True
    session["user"] = {
        "id": user.id,
        "email": user.email,
        "name": meta.get("name") or (user.email or "student").split("@")[0],
    }
    csrf_token()


@app.route("/")
def index():
    return render_template("landing.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not EMAIL_RE.match(email) or not password:
            flash("Enter your email and password.", "error")
        else:
            try:
                res = auth_client().auth.sign_in_with_password(
                    {"email": email, "password": password})
                _start_session(res.user)
                return redirect(url_for("dashboard"))
            except Exception as exc:  # wrong password, unconfirmed email, etc.
                app.logger.warning("login failed: %r", exc)
                flash(_auth_error(exc, "log you in"), "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()[:60]
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name:
            flash("Please tell us your name.", "error")
        elif not EMAIL_RE.match(email):
            flash("Enter a valid email address.", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        else:
            try:
                res = auth_client().auth.sign_up({
                    "email": email, "password": password,
                    "options": {"data": {"name": name}},
                })
                if res.session is None:  # email confirmation is switched on
                    flash("Account created! Check your email to confirm, then log in.", "ok")
                    return redirect(url_for("login"))
                _start_session(res.user)
                return redirect(url_for("dashboard"))
            except Exception as exc:
                app.logger.warning("register failed: %r", exc)
                flash(_auth_error(exc, "create the account"), "error")
    return render_template("register.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# --------------------------------------------------------------------------
# App pages
# --------------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    done = get_done(uid())
    stats, done_total, total, percent = summarise(done)
    upcoming = [p for p in get_plans(uid()) if not p["done"]][:4]
    return render_template("dashboard.html", stats=stats, done_count=done_total,
                           total=total, percent=percent, upcoming=upcoming)


@app.route("/syllabus")
@login_required
def syllabus():
    done = get_done(uid())
    _, done_total, total, percent = summarise(done)
    return render_template("syllabus.html", subjects=SUBJECTS, done=done,
                           done_count=done_total, total=total, percent=percent)


@app.route("/practice")
@login_required
def practice():
    return render_template("practice.html", quizzes=QUIZZES, subjects=SUBJECT_NAMES)


@app.route("/planner")
@login_required
def planner():
    return render_template("planner.html", plans=get_plans(uid()), subjects=SUBJECT_NAMES)


@app.route("/maps")
@login_required
def maps():
    done = get_done(uid())
    return render_template("maps.html", groups=MAP_GROUPS, done=done)


@app.route("/healthz")
def healthz():
    return "ok"


# --------------------------------------------------------------------------
# JSON API
# --------------------------------------------------------------------------
@app.post("/api/progress")
@login_required
def api_progress():
    data = request.get_json(silent=True) or {}
    key, done = data.get("key"), data.get("done")
    if key not in ALL_KEYS or not isinstance(done, bool):
        return bad("Unknown topic.")
    db().table("progress").upsert(
        {"user_id": uid(), "item_key": key, "done": done},
        on_conflict="user_id,item_key",
    ).execute()
    return jsonify(ok=True)


@app.post("/api/plans")
@login_required
def api_add_plan():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()
    subject = data.get("subject")
    due = data.get("due_date") or None
    if not task or len(task) > 200:
        return bad("Enter a task (up to 200 characters).")
    if subject not in SUBJECT_NAMES:
        return bad("Pick a subject.")
    if due:
        try:
            date.fromisoformat(due)
        except ValueError:
            return bad("That date doesn't look right.")
    row = db().table("plans").insert({
        "user_id": uid(), "task": task, "subject": subject, "due_date": due,
    }).execute().data[0]
    return jsonify({k: row[k] for k in ("id", "task", "subject", "due_date", "done")}), 201


@app.patch("/api/plans/<plan_id>")
@login_required
def api_update_plan(plan_id):
    data = request.get_json(silent=True) or {}
    if not isinstance(data.get("done"), bool):
        return bad("Nothing to update.")
    db().table("plans").update({"done": data["done"]}) \
        .eq("id", plan_id).eq("user_id", uid()).execute()
    return jsonify(ok=True)


@app.delete("/api/plans/<plan_id>")
@login_required
def api_delete_plan(plan_id):
    db().table("plans").delete().eq("id", plan_id).eq("user_id", uid()).execute()
    return jsonify(ok=True)


@app.post("/api/quiz")
@login_required
def api_quiz():
    data = request.get_json(silent=True) or {}
    subject, score, total = data.get("subject"), data.get("score"), data.get("total")
    if subject != "all" and subject not in SUBJECT_NAMES:
        return bad("Unknown subject.")
    if not (isinstance(score, int) and isinstance(total, int) and 0 <= score <= total <= 100 and total > 0):
        return bad("Invalid score.")
    db().table("quiz_attempts").insert({
        "user_id": uid(), "subject": subject, "score": score, "total": total,
    }).execute()
    return jsonify(ok=True), 201


# --------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------
@app.errorhandler(400)
def handle_400(_):
    if request.path.startswith("/api/"):
        return jsonify(error="Session expired. Please refresh the page."), 400
    flash("Your session expired. Please try again.", "error")
    return redirect(url_for("login"))


@app.errorhandler(404)
def handle_404(_):
    if request.path.startswith("/api/"):
        return jsonify(error="Not found."), 404
    return render_template("404.html"), 404


@app.errorhandler(Exception)
def handle_error(exc):
    if isinstance(exc, HTTPException):
        return exc
    app.logger.exception("Unhandled error")
    if request.path.startswith("/api/"):
        return jsonify(error="Something went wrong. Please try again."), 500
    return render_template("404.html", message="Something went wrong on our side."), 500


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))