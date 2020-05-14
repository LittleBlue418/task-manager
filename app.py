import os

from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)

password = os.environ.get("MONGODB_PASSWORD")

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:{}@myfirstcluster-8zy3m.mongodb.net/task_manager?retryWrites=true&w=majority'.format(password)

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    new_task = request.form.to_dict()

    new_task['is_urgent'] = 'is_urgent' in new_task

    tasks.insert_one(new_task)

    return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    task_to_edit = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=task_to_edit, categories=all_categories)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0" if "DYNO" in os.environ else None,
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )