import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode

import Util
import Validator
import CustomExceptions

application = Flask(__name__)
app = application





@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    Util.create_tables()
    app.run(host='0.0.0.0')
