import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "campuspulse-development-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "campuspulse.db"

CATEGORIES = [
    "Wi-Fi / Internet",
    "Laboratory Equipment",
    "Electrical Issue",
    "Maintenance",
    "Other",
]

PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["Open", "In Progress", "Resolved"]


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open'
            )
        """)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "")
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "")

        if not title or not location or not description:
            flash("Please complete all required fields.", "error")
            return redirect(url_for("index"))

        if category not in CATEGORIES or priority not in PRIORITIES:
            flash("Please select a valid category and priority.", "error")
            return redirect(url_for("index"))

        with get_db() as connection:
            connection.execute(
                """INSERT INTO incidents
                   (title, category, location, description, priority)
                   VALUES (?, ?, ?, ?, ?)""",
                (title, category, location, description, priority),
            )

        flash("Incident reported successfully!", "success")
        return redirect(url_for("index"))

    with get_db() as connection:
        incidents = connection.execute(
            "SELECT * FROM incidents ORDER BY id DESC"
        ).fetchall()

    stats = {
        "total": len(incidents),
        "open": sum(i["status"] == "Open" for i in incidents),
        "progress": sum(i["status"] == "In Progress" for i in incidents),
        "resolved": sum(i["status"] == "Resolved" for i in incidents),
    }

    return render_template(
        "index.html",
        incidents=incidents,
        stats=stats,
        categories=CATEGORIES,
        priorities=PRIORITIES,
    )


@app.route("/update/<int:incident_id>", methods=["POST"])
def update_status(incident_id):
    status = request.form.get("status", "")

    if status not in STATUSES:
        flash("Invalid incident status.", "error")
        return redirect(url_for("index"))

    with get_db() as connection:
        connection.execute(
            "UPDATE incidents SET status = ? WHERE id = ?",
            (status, incident_id),
        )

    flash("Incident status updated.", "success")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
