from flask import Flask
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

# change to another port (8000) with: flask run --port 8000
app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
todos = db.todos

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))
    
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

# accepts POST requests
# since web browsers default to GET requests, user clicks button > POST request to delete a todo
@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


# edit button
@app.post("/<id>/update/")
def update(id):
    if request.method == "POST":
        new_content = request.form["content"]
        new_degree = request.form["degree"]
        todos.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"content": new_content, "degree": new_degree}},
        )
        return redirect(url_for("index"))
    return render_template("index.html", todos=todos.find())

