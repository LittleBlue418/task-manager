import os

from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)

password = os.environ.get("MONGODB_PASSWORD")

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:{}@myfirstcluster-8zy3m.mongodb.net/task_manager?retryWrites=true&w=majority'.format(
    password)

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    show_completed = bool(request.args.get('show_completed'))
    completed = []
    not_completed = []

    if show_completed:
        tasks = mongo.db.tasks.find()

        for task in tasks:
            if task['complete']:
                completed.append(task)
            else:
                not_completed.append(task)

    else:
        not_completed = mongo.db.tasks.find({ "complete": False })

    return render_template("tasks.html", completed=completed, not_completed=not_completed, show_completed=show_completed)


@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    new_task = request.form.to_dict()

    new_task['is_urgent'] = 'is_urgent' in new_task
    new_task['complete'] = False

    tasks.insert_one(new_task)

    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    task_to_edit = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=task_to_edit, categories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
        {
            'task_name': request.form.get('task_name'),
            'category_name': request.form.get('category_name'),
            'task_description': request.form.get('task_description'),
            'due_date': request.form.get('due_date'),
            'is_urgent': request.form.get('is_urgent'),
            'complete': False
        })
    return redirect(url_for('get_tasks'))

@app.route('/toggle_complete/<task_id>')
def toggle_complete(task_id):
    tasks = mongo.db.tasks
    is_completed = bool(request.args.get('done'))
    print(is_completed)

    tasks.update_one({'_id': ObjectId(task_id)},
            {'$set':{'complete': is_completed}})

    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
        category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=["POST"])
def update_category(category_id):
    mongo.db.categories.update({'_id': ObjectId(category_id)},
        {
            'category_name': request.form.get('category_name'),
        })
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def new_category():
    return render_template('addcategory.html')

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0" if "DYNO" in os.environ else None,
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
