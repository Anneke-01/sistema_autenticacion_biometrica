from dotenv import load_dotenv 
import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions

app = Flask(__name__)
app.debug = True
load_dotenv()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    session.clear()
    return render_template("dashboard.html")

@app.route("/estudiantes", methods=["GET", "POST"])
def estudiantes():
    session.clear()
    return render_template("estudiantes.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

if __name__ == '__main__':
    app.run()