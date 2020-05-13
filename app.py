import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0" if "DYNO" in os.environ else None,
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )