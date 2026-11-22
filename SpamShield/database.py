"""
database.py
-----------
All SQLite database code for SpamShield.

Every query uses PARAMETERISED placeholders (the "?" symbol) instead of
building SQL with string formatting. SQLite then treats user input strictly
as data, which prevents SQL-injection attacks.
"""

import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "spamshield.db"


@contextmanager
def get_db():
    """
    Open a database connection, commit if everything succeeded,
    roll back if an error occurred, and always close the connection.
    """
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dictionaries
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create the analyses table (and an index on the date) if missing."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                message          TEXT    NOT NULL,
                label            TEXT    NOT NULL CHECK (label IN ('spam', 'ham')),
                risk_level       TEXT    NOT NULL,
                confidence       REAL    NOT NULL,
                spam_probability REAL    NOT NULL,
                created_at       TEXT    NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_analyses_created ON analyses (created_at)")


def save_analysis(message, result):
    """Store one prediction result. Returns (new row id, timestamp string)."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO analyses (message, label, risk_level, confidence, spam_probability, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (message, result["label"], result["risk_level"], result["confidence"],
             result["spam_probability"], created_at),
        )
        return cursor.lastrowid, created_at


def _escape_like(text):
    """Escape the LIKE wildcards % and _ so they are searched literally."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def get_history(search="", label_filter="all", page=1, per_page=15):
    """
    Return (rows, total_count) for the history page.

    search       -> text to look for inside the message
    label_filter -> 'all', 'spam' or 'ham'
    page         -> page number starting from 1
    """
    conditions, params = [], []
    if search:
        conditions.append("message LIKE ? ESCAPE '\\'")
        params.append(f"%{_escape_like(search)}%")
    if label_filter in ("spam", "ham"):
        conditions.append("label = ?")
        params.append(label_filter)

    # Only fixed SQL fragments are joined here; user values stay in params.
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    offset = (page - 1) * per_page

    with get_db() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM analyses {where}", params).fetchone()[0]
        rows = conn.execute(
            f"SELECT * FROM analyses {where} ORDER BY id DESC LIMIT ? OFFSET ?",
            params + [per_page, offset],
        ).fetchall()
    return [dict(row) for row in rows], total


def get_recent(limit=6):
    """Return the most recent analyses (for the dashboard)."""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) for row in rows]


def delete_analysis(analysis_id):
    """Delete one record. Returns True if a row was deleted."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
        return cursor.rowcount > 0


def clear_history():
    """Delete every record. Returns how many rows were removed."""
    with get_db() as conn:
        return conn.execute("DELETE FROM analyses").rowcount


def get_stats():
    """Overall totals used by the dashboard and analytics pages."""
    today = date.today().isoformat()
    with get_db() as conn:
        row = conn.execute(
            """SELECT COUNT(*)                                          AS total,
                      COALESCE(SUM(label = 'spam'), 0)                  AS spam,
                      COALESCE(SUM(label = 'ham'), 0)                   AS ham,
                      COALESCE(SUM(risk_level = 'suspicious'), 0)       AS suspicious,
                      COALESCE(AVG(confidence), 0)                      AS avg_confidence,
                      COALESCE(SUM(substr(created_at, 1, 10) = ?), 0)   AS today
               FROM analyses""",
            (today,),
        ).fetchone()
    stats = dict(row)
    stats["spam_rate"] = round(stats["spam"] / stats["total"] * 100, 1) if stats["total"] else 0.0
    stats["avg_confidence"] = round(stats["avg_confidence"], 1)
    return stats


def get_daily_stats(days=14):
    """
    Spam / ham counts for each of the last `days` days.
    Days with no activity are included with zero counts so charts
    always show a continuous timeline.
    """
    start = date.today() - timedelta(days=days - 1)
    with get_db() as conn:
        rows = conn.execute(
            """SELECT substr(created_at, 1, 10) AS day,
                      SUM(label = 'spam') AS spam,
                      SUM(label = 'ham')  AS ham
               FROM analyses
               WHERE substr(created_at, 1, 10) >= ?
               GROUP BY day""",
            (start.isoformat(),),
        ).fetchall()
    counts = {row["day"]: (row["spam"], row["ham"]) for row in rows}

    result = []
    for i in range(days):
        day = start + timedelta(days=i)
        spam, ham = counts.get(day.isoformat(), (0, 0))
        total = spam + ham
        result.append({
            "date": day.isoformat(),
            "label": day.strftime("%d %b"),
            "spam": spam,
            "ham": ham,
            "total": total,
            "spam_rate": round(spam / total * 100, 1) if total else 0,
        })
    return result


def get_confidence_distribution():
    """Count predictions in confidence buckets: 50-60%, 60-70% ... 90-100%."""
    buckets = [(50, 60), (60, 70), (70, 80), (80, 90), (90, 101)]
    with get_db() as conn:
        rows = conn.execute("SELECT label, confidence FROM analyses").fetchall()
    dist = {"labels": [f"{lo}-{min(hi, 100)}%" for lo, hi in buckets],
            "spam": [0] * len(buckets), "ham": [0] * len(buckets)}
    for row in rows:
        for i, (lo, hi) in enumerate(buckets):
            if lo <= row["confidence"] < hi:
                dist[row["label"]][i] += 1
                break
    return dist


def get_risk_breakdown():
    """Counts of safe / suspicious / spam risk levels."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT risk_level, COUNT(*) AS n FROM analyses GROUP BY risk_level").fetchall()
    counts = {row["risk_level"]: row["n"] for row in rows}
    return {level: counts.get(level, 0) for level in ("safe", "suspicious", "spam")}
