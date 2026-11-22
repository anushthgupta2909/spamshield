"""
app.py
------
SpamShield – Spam Message Detector (Flask web application).

Run with:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import logging
import math
import os
import secrets
from datetime import datetime

from flask import (Flask, abort, flash, jsonify, redirect, render_template, request,
                   session, url_for)

import database as db
from detector import MODEL_PATH, SpamDetector

MAX_MESSAGE_LENGTH = 2000          # characters allowed in one message
HISTORY_PER_PAGE = 15

app = Flask(__name__)
# The secret key signs the session cookie (used for flash messages and CSRF).
# Set SPAMSHIELD_SECRET_KEY in production; a random key is used otherwise.
app.config["SECRET_KEY"] = os.environ.get("SPAMSHIELD_SECRET_KEY") or secrets.token_hex(32)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024      # reject request bodies larger than 64 KB
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("spamshield")


# ---------------------------------------------------------------------------
# Start-up: database + model
# ---------------------------------------------------------------------------

def load_detector():
    """
    Load the trained model once when the app starts.
    If the model file does not exist yet, train it automatically.
    """
    if not MODEL_PATH.exists():
        log.warning("Model not found - training a new model (this takes a few seconds)...")
        from train_model import train
        train(verbose=False)
    detector = SpamDetector(MODEL_PATH)
    log.info("Model loaded (accuracy %.2f%%)", detector.metrics.get("accuracy", 0))
    return detector


db.init_db()
detector = load_detector()


# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------

def get_csrf_token():
    """Create (once per session) a random token that every POST form must send back."""
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


app.jinja_env.globals["csrf_token"] = get_csrf_token


@app.before_request
def csrf_protect():
    """Reject POST requests that do not carry the correct CSRF token."""
    if request.method == "POST":
        expected = session.get("_csrf_token")
        sent = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
        if not expected or not sent or not secrets.compare_digest(expected, sent):
            abort(400, description="Your session expired. Please reload the page and try again.")


@app.after_request
def security_headers(response):
    """Add basic HTTP security headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    return response


def validate_message(raw):
    """
    Check the user's message. Returns (clean_message, error_text).
    error_text is None when the message is valid.
    """
    message = (raw or "").strip()
    if not message:
        return message, "Please enter a message to analyze."
    if len(message) > MAX_MESSAGE_LENGTH:
        return message, f"Message is too long ({len(message)} characters). The limit is {MAX_MESSAGE_LENGTH}."
    if not any(ch.isalnum() for ch in message):
        return message, "The message must contain at least some letters or numbers."
    return message, None


def analyze_and_save(message):
    """Run the ML model on a message and store the result in the database."""
    result = detector.predict(message)
    result["id"], result["created_at"] = db.save_analysis(message, result)
    return result


@app.template_filter("serial")
def serial_filter(value):
    """Format a record id like a cheque serial number: 214 -> 000214."""
    return f"{int(value):06d}"


@app.template_filter("pct")
def pct_filter(value, decimals=1):
    """Round a percentage DOWN so 99.99 shows as 99.9 (never a false 100.0)."""
    factor = 10 ** decimals
    return f"{math.floor(float(value) * factor) / factor:.{decimals}f}"


@app.template_filter("stamp_date")
def stamp_date_filter(value, with_time=True):
    """Format '2026-11-22 14:02:10' as '22 Nov 2026 · 14:02'."""
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return value
    return dt.strftime("%d %b %Y · %H:%M") if with_time else dt.strftime("%d %b %Y")


@app.context_processor
def inject_globals():
    """Values available in every template."""
    return {"max_length": MAX_MESSAGE_LENGTH, "model_metrics": detector.metrics}


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@app.route("/")
def dashboard():
    """Home dashboard with overall statistics, charts and recent analyses."""
    stats = db.get_stats()
    chart_data = {
        "spamHam": {"spam": stats["spam"], "ham": stats["ham"]},
        "daily": db.get_daily_stats(7),
    }
    return render_template("dashboard.html", active="dashboard", stats=stats,
                           recent=db.get_recent(6), chart_data=chart_data)


@app.route("/detect", methods=["GET", "POST"])
def detect():
    """Message analysis page. GET shows the form, POST analyzes the message."""
    result, message = None, ""
    if request.method == "POST":
        message, error = validate_message(request.form.get("message"))
        if error:
            flash(error, "danger")
        else:
            try:
                result = analyze_and_save(message)
            except Exception:
                # Log the full error for the developer, show a friendly one to the user.
                log.exception("Prediction failed")
                flash("Something went wrong while analyzing the message. Please try again.", "danger")
    return render_template("detect.html", active="detect", result=result, message=message,
                           stats=db.get_stats())


@app.route("/history")
def history():
    """List previous analyses with search, filter and pagination."""
    search = request.args.get("q", "").strip()[:200]
    label_filter = request.args.get("filter", "all")
    if label_filter not in ("all", "spam", "ham"):
        label_filter = "all"
    page = request.args.get("page", 1, type=int) or 1
    page = max(page, 1)

    rows, total = db.get_history(search, label_filter, page, HISTORY_PER_PAGE)
    pages = max(math.ceil(total / HISTORY_PER_PAGE), 1)
    if page > pages and total:
        return redirect(url_for("history", q=search, filter=label_filter, page=pages))

    return render_template("history.html", active="history", rows=rows, total=total,
                           search=search, label_filter=label_filter, page=page, pages=pages,
                           stats=db.get_stats())


@app.route("/history/delete/<int:analysis_id>", methods=["POST"])
def delete_history_item(analysis_id):
    """Delete a single history record."""
    if db.delete_analysis(analysis_id):
        flash("Record deleted.", "success")
    else:
        flash("That record no longer exists.", "warning")
    return redirect(url_for("history", q=request.form.get("q", ""),
                            filter=request.form.get("filter", "all"),
                            page=request.form.get("page", 1, type=int)))


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Delete all history records."""
    removed = db.clear_history()
    flash(f"History cleared ({removed} record{'s' if removed != 1 else ''} removed).", "success")
    return redirect(url_for("history"))


@app.route("/analytics")
def analytics():
    """Charts and statistics about all analyses plus model performance."""
    stats = db.get_stats()
    chart_data = {
        "spamHam": {"spam": stats["spam"], "ham": stats["ham"]},
        "daily": db.get_daily_stats(14),
        "confidence": db.get_confidence_distribution(),
        "risk": db.get_risk_breakdown(),
    }
    return render_template("analytics.html", active="analytics", stats=stats,
                           chart_data=chart_data, metrics=detector.metrics)


@app.route("/about")
def about():
    """Project information page."""
    return render_template("about.html", active="about", metrics=detector.metrics)


# ---------------------------------------------------------------------------
# JSON API (used for live charts and handy for demonstrations)
# ---------------------------------------------------------------------------

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """Analyze a message sent as JSON: {"message": "..."} (needs X-CSRFToken header)."""
    payload = request.get_json(silent=True) or {}
    message, error = validate_message(payload.get("message"))
    if error:
        return jsonify({"error": error}), 400
    try:
        return jsonify(analyze_and_save(message))
    except Exception:
        log.exception("API prediction failed")
        return jsonify({"error": "Could not analyze the message."}), 500


@app.route("/api/stats")
def api_stats():
    """Current statistics as JSON."""
    return jsonify({"stats": db.get_stats(), "daily": db.get_daily_stats(14)})


# ---------------------------------------------------------------------------
# Error pages – never show Python tracebacks to the user
# ---------------------------------------------------------------------------

ERROR_TEXT = {
    400: ("Bad request", "The request could not be processed."),
    404: ("Page not found", "The page you are looking for does not exist."),
    405: ("Method not allowed", "This action is not allowed on this page."),
    413: ("Message too large", "The submitted data is too large."),
    500: ("Server error", "Something went wrong on our side. Please try again later."),
}


def render_error(code, description=None):
    title, default_text = ERROR_TEXT.get(code, ERROR_TEXT[500])
    text = description or default_text
    if request.path.startswith("/api/"):
        return jsonify({"error": text}), code
    return render_template("error.html", code=code, title=title, text=text), code


@app.errorhandler(400)
def bad_request(err):
    return render_error(400, getattr(err, "description", None))


@app.errorhandler(404)
def not_found(err):
    return render_error(404)


@app.errorhandler(405)
def method_not_allowed(err):
    return render_error(405)


@app.errorhandler(413)
def too_large(err):
    return render_error(413)


@app.errorhandler(500)
def server_error(err):
    log.exception("Unhandled server error")
    return render_error(500)


if __name__ == "__main__":
    # debug=False so internal errors are never displayed in the browser.
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=debug)
