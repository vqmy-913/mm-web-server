from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, redirect
from bson.objectid import ObjectId

# change to another port (8000) with: flask run --port 8000
app = Flask(__name__)

# set up client in MongoDB
client = MongoClient("localhost", 27017)
db = client.flask_db
ratings = db.ratings


# create index page from template
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        restaurant = request.form["restaurant"]
        rating = request.form["rating"]
        ratings.insert_one({"restaurant": restaurant, "rating": rating})
        return redirect(url_for("index"))

    all_ratings = ratings.find()
    return render_template("index.html", ratings=all_ratings)


# accepts POST requests
# since web browsers default to GET requests, user clicks button > POST request to delete a rating
# delete button
@app.post("/<id>/delete/")
def delete(id):
    ratings.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))


# edit button
@app.post("/<id>/update/")
def update(id):
    if request.method == "POST":
        new_content = request.form["restaurant"]
        new_rating = request.form["rating"]
        ratings.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"restaurant": new_content, "rating": new_rating}},
        )
        return redirect(url_for("index"))
    return render_template("index.html", ratings=ratings.find())


# done button
