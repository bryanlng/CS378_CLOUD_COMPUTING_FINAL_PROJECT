import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode

import Validator
import CustomExceptions

application = Flask(__name__)
app = application


#Creds
db = os.environ.get("DB_NAME", None)
username = os.environ.get("DB_USERNAME", None)
password = os.environ.get("DB_PASSWORD", None)
hostname = os.environ.get("DB_IP", None)

def connect():
    connection = ''
    try:
        connection = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)

    cursor = connection.cursor()
    return connection, cursor



def create_tables():
    # Check if table exists or not. Create and populate it only if it does not exist.
    videos_table = ("CREATE TABLE VIDEOS"
                    "(id INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                    "VIDEO_ID VARCHAR(1000) NOT NULL,"
                    "PRIMARY KEY (id),"
                    "UNIQUE KEY (VIDEO_ID)"
                    ")"
                )

    records_table = ("CREATE TABLE RECORDS"
                            "(id INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                            "YOUTUBE_VIDEO_ID VARCHAR(1000) NOT NULL,"
                            "MEDIA_FORMAT enum('MP3', 'AAC', 'FLAC', 'MP4', 'AVI', 'MOV', 'MKV') NOT NULL,"
                            "PRIMARY KEY (id),"
                            "CONSTRAINT FOREIGN KEY (YOUTUBE_VIDEO_ID)"
                                "REFERENCES ACCOUNT (VIDEO_ID)"
                                "ON UPDATE CASCADE ON DELETE CASCADE"
                            ")"
                        )

    cnx, cur = connect()
    try:
        cur.execute(videos_table)
        cnx.commit()
        cur.execute(records_table)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    create_tables()
    app.run(host='0.0.0.0')
