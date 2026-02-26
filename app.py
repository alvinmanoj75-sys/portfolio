from flask import Flask, render_template, request, jsonify, session, redirect
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# ── Demo Admin Credentials ────────────────────────────────────────
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin123"

# ── Routes ───────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session['authenticated'] = True
            return jsonify({"success": True, "message": "Login successful"})
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    return render_template("login.html")

@app.route("/report")
def report():
    if not session.get('authenticated'):
        return redirect("/login")
    
    return render_template("report-supabase.html")

@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)