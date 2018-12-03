from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO"] = "mongodb://localhost:27017"
mongo = PyMongo(app)

@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html", listings=data)

@app.route("/scrape")
def scraper():
    data = mongo.db.data
    marss_data = scrape_mars.scrape()
    data.update({}, marss_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
