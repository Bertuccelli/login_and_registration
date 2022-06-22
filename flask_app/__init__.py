from flask import Flask
app = Flask(__name__)
app.secret_key = "stealth"

DATABASE = "login_db"
# YOU NEED TO ADD THIS ONCE YOU HAVE THE DB NAME