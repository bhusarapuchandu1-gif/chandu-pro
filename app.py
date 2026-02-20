from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret")

# MongoDB Atlas connection
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["portfolio_db"]
contacts_collection = db["contacts"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required!")
            return redirect(url_for("contact"))

        contacts_collection.insert_one({
            "name": name,
            "email": email,
            "message": message
        })

        flash("Message sent successfully!")
        return redirect(url_for("contact"))

    return render_template("contact.html")

if __name__ == "__main__":
    app.run()
