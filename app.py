from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expenses.db"
app = Flask(__name__)
app.secret_key = "demo-secret-key-change-before-deployment"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL
            )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_raw = request.form.get("amount", "").strip()
        category = request.form.get("category", "Other")
        expense_date = request.form.get("expense_date", date.today().isoformat())
        try:
            amount = float(amount_raw)
            if not title or amount <= 0:
                raise ValueError
        except ValueError:
            flash("Enter a description and a valid amount greater than zero.")
            return redirect(url_for("index"))
        allowed = {"Food", "Travel", "Shopping", "Education", "Bills", "Other"}
        if category not in allowed:
            category = "Other"
        with get_db() as conn:
            conn.execute(
                "INSERT INTO expenses (title, amount, category, expense_date) VALUES (?, ?, ?, ?)",
                (title, amount, category, expense_date)
            )
        flash("Expense added successfully!")
        return redirect(url_for("index"))

    with get_db() as conn:
        expenses = conn.execute("SELECT * FROM expenses ORDER BY expense_date DESC, id DESC").fetchall()
        total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        category_rows = conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC"
        ).fetchall()
    return render_template("index.html", expenses=expenses, total=total, category_rows=category_rows, today=date.today().isoformat())

@app.post("/delete/<int:expense_id>")
def delete_expense(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    flash("Expense deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
