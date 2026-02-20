from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "chandu_secret_key"

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
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

        contact_data = {
            "name": name,
            "email": email,
            "message": message
        }

        contacts_collection.insert_one(contact_data)
        flash("Message sent successfully!")
        return redirect(url_for("contact"))

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
