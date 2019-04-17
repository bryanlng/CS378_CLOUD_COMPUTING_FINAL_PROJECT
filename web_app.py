import os
import time

from flask import request
from flask import Flask, render_template


application = Flask(__name__)
app = application


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    initialize_table()
    app.run(host='0.0.0.0')
