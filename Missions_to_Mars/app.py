from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

# setup mongo connection
mongo_conn = PyMongo(app,"mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars_data_dict = mongo_conn.db.mars_data.find_one()
    print(mars_data_dict)
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", data=mars_data_dict)


@app.route("/scrape")
def scrape():
  
    mars_data_scrape = mission_to_mars.scrape()
    print("scrapped data ------ " , type(mars_data_scrape))
    print(mars_data_scrape)
    mars_dict = mongo_conn.db.mars_data
    # Update the Mongo database using update and upsert=True
    #mongo_conn.db.mars_db.update({}, mars_data_scrape, upsert=True)
    mars_dict.replace_one({}, mars_data_scrape, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
