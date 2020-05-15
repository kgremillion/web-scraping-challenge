from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape
# Create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_scrape = mongo.db.mars_scrape.find_one()

    # Return template and data
    return render_template("index.html", mars_scrape=mars_scrape)

# Route that will trigger the scrape function
@app.route("/scrape") 
def scraper():

    # Run the scrape function
    mars_scrape = mongo.db.mars_scrape

    mars_mission = scrape()
    print(mars_mission)
    # Update the Mongo database using update and upsert=True
    mars_scrape.update({}, mars_mission, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

