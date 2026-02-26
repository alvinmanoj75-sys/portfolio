from flask import Flask, render_template, request, jsonify, session, redirect
import traceback
from email.mime.text import MIMEText
import smtplib
from email.utils import formataddr
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# ── Demo Credentials ────────────────────────────────────────────
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin123"

# ── File Storage Config ────────────────────────────────────────
DATA_FILE = "inquiries.json"  # Store inquiries in JSON file

# In-memory storage for Vercel (serverless)
IN_MEMORY_INQUIRIES = []

def load_inquiries_from_file():
    """Load inquiries from file into memory on startup"""
    global IN_MEMORY_INQUIRIES
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                IN_MEMORY_INQUIRIES = json.load(f)
        else:
            IN_MEMORY_INQUIRIES = []
    except Exception as e:
        print(f"Could not load inquiries: {e}")
        IN_MEMORY_INQUIRIES = []

def save_inquiry_to_storage(name: str, email: str, message: str) -> bool:
    """Save inquiry to both file and in-memory storage"""
    global IN_MEMORY_INQUIRIES
    try:
        inquiry_data = {
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to in-memory storage
        IN_MEMORY_INQUIRIES.append(inquiry_data)
        
        # Try to save to file if possible (for local development)
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(IN_MEMORY_INQUIRIES, f, indent=2)
        except Exception as file_err:
            print(f"File storage not available (serverless environment): {file_err}")
        
        print(f"Saved inquiry from {name}")
        return True
    except Exception as e:
        print(f"Storage error: {e}")
        return False

def get_all_inquiries():
    """Get all inquiries from in-memory storage"""
    return IN_MEMORY_INQUIRIES

def delete_inquiry(index: int) -> bool:
    """Delete an inquiry by index"""
    global IN_MEMORY_INQUIRIES
    try:
        if 0 <= index < len(IN_MEMORY_INQUIRIES):
            IN_MEMORY_INQUIRIES.pop(index)
            
            # Save to file
            try:
                with open(DATA_FILE, 'w') as f:
                    json.dump(IN_MEMORY_INQUIRIES, f, indent=2)
            except Exception as file_err:
                print(f"File update failed: {file_err}")
            
            return True
        return False
    except Exception as e:
        print(f"Delete error: {e}")
        return False

def clear_all_inquiries() -> bool:
    """Clear all inquiries"""
    global IN_MEMORY_INQUIRIES
    try:
        IN_MEMORY_INQUIRIES = []
        
        # Save empty list to file
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump([], f, indent=2)
        except Exception as file_err:
            print(f"File update failed: {file_err}")
        
        return True
    except Exception as e:
        print(f"Clear error: {e}")
        return False

# Load inquiries on startup
load_inquiries_from_file()

# ── Email config (keep if you want email + DB) ──────────────────
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT   = int(os.getenv("SMTP_PORT", 587))
SMTP_USER   = os.getenv("SMTP_USER")
SMTP_PASS   = os.getenv("SMTP_PASS")
YOUR_EMAIL  = os.getenv("YOUR_EMAIL", SMTP_USER)

def send_email(name: str, email: str, message: str) -> bool:
    if not all([SMTP_USER, SMTP_PASS]):
        print("Email config missing — skipping send")
        return False

    subject = f"New Portfolio Inquiry from {name}"
    body = f"""Name: {name}
Email: {email}
Message: {message}

Reply to: {email}"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((name, SMTP_USER))
    msg["Reply-To"] = email
    msg["To"] = YOUR_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

# ── Routes ───────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        name    = data.get("name", "").strip()
        email   = data.get("email", "").strip()
        message = data.get("message", "").strip()

        if not all([name, email, message]):
            return jsonify({"success": False, "message": "All fields required"}), 400

        # Save to storage
        file_saved = save_inquiry_to_storage(name, email, message)
        
        if not file_saved:
            return jsonify({"success": False, "message": "Failed to save inquiry"}), 500
        
        # Optional: send email too
        email_sent = send_email(name, email, message)

        msg = f"Thank you, {name}! Your inquiry has been received."
        if not email_sent:
            msg += " (Email notification could not be sent, but your inquiry is saved.)"

        return jsonify({"success": True, "message": msg})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

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
    
    try:
        inquiries = get_all_inquiries()
        return render_template("report.html", inquiries=inquiries, total=len(inquiries))
    except Exception as e:
        return f"Error loading inquiries: {str(e)}", 500

@app.route("/delete-inquiry", methods=["POST"])
def delete_inquiry_route():
    if not session.get('authenticated'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        index = data.get("index", -1)
        
        if delete_inquiry(index):
            return jsonify({"success": True, "message": "Inquiry deleted successfully"})
        else:
            return jsonify({"success": False, "message": "Inquiry not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/clear-all-inquiries", methods=["POST"])
def clear_all_inquiries_route():
    if not session.get('authenticated'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        if clear_all_inquiries():
            return jsonify({"success": True, "message": "All inquiries cleared"})
        else:
            return jsonify({"success": False, "message": "Failed to clear inquiries"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)