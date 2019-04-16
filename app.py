
# Import Dependencies
import mars_scrapper
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mission2mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    # Find data
    mars_info = mongo.db.mars_info.find_one()
    if not mars_info:
        scrape()
    # Return template and data
    return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scrape():

    # Run scrapped functions
    mars_info = mongo.db.mars_info
    mars_data = mars_scrapper.get_mars_news()
    print(mars_data)

    mars_data = mars_scrapper.get_mars_images()
    mars_data = mars_scrapper.get_mars_weather()
    mars_data = mars_scrapper.get_mars_facts()
    mars_data = mars_scrapper.get_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug= True)