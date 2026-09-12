#!/usr/bin/env python3
"""
TinyCorp Employee Portal — a deliberately vulnerable Flask app for a
beginner-friendly web-exploitation CTF challenge.

The vulnerability: the login query is built by string-formatting user
input directly into SQL (see the `# VULNERABLE LINE` comment below),
so a crafted username can alter the query's logic and bypass the
password check entirely (classic SQL injection / auth bypass).

Do not deploy this outside an isolated CTF environment — it is
intentionally insecure.
"""
import os
import sqlite3

from flask import Flask, request, render_template, redirect, url_for, session

from init_db import init_db, DB_PATH

FLAG = os.environ.get("CTF_FLAG", "FLAG{s1ngl3_qu0t3_5t0ps_th3_qu3ry}")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-not-for-prod")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def ensure_db():
    if not os.path.exists(DB_PATH):
        init_db()


@app.route("/", methods=["GET"])
def index():
    if session.get("role") == "admin":
        return redirect(url_for("dashboard"))
    return render_template("login.html", error=None)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db()
    cur = conn.cursor()

    # VULNERABLE LINE: user input is formatted directly into the SQL
    # string instead of using a parameterized query. A username like
    #   admin' --
    # turns this into:
    #   SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
    # which comments out the password check entirely.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cur.execute(query)
        user = cur.fetchone()
    except sqlite3.OperationalError:
        user = None
    conn.close()

    if user is None:
        return render_template("login.html", error="Invalid username or password.")

    session["username"] = user["username"]
    session["role"] = user["role"]

    if user["role"] == "admin":
        return redirect(url_for("dashboard"))
    return render_template("employee.html", username=user["username"])


@app.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    return render_template("dashboard.html", flag=FLAG)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
