import os

from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)

password = os.environ.get("MONGODB_PASSWORD")

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:{}@myfirstcluster-8zy3m.mongodb.net/task_manager?retryWrites=true&w=majority'.format(password)

mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0" if "DYNO" in os.environ else None,
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )