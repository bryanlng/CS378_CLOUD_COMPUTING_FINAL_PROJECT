import os
import mysql.connector
from mysql.connector import errorcode

#Creds
db = os.environ.get("RDS_DB_NAME", None)
username = os.environ.get("RDS_USERNAME", None)
password = os.environ.get("RDS_PASSWORD", None)
hostname = os.environ.get("RDS_HOSTNAME", None)

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
                                "REFERENCES VIDEOS (VIDEO_ID)"
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
