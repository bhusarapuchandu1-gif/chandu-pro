from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)

# Secret Key (secure way)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# MongoDB Connection with error handling
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["portfolio_db"]
    contacts_collection = db["contacts"]
    print("MongoDB Connected Successfully!")
except Exception as e:
    print("Database connection error:", e)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Validation
        if not name or not email or not message:
            flash("All fields are required!")
            return redirect(url_for("contact"))

        contact_data = {
            "name": name,
            "email": email,
            "message": message
        }

        try:
            contacts_collection.insert_one(contact_data)
            flash("Message sent successfully!")
        except Exception as e:
            flash("Error saving message!")
            print("Insert error:", e)

        return redirect(url_for("contact"))

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
