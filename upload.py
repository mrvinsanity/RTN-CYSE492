import boto3
from botocore.client import Config
import sqlite3
from datetime import datetime, timedelta
import json

def queryDB(t):
    timeBuffer = timedelta(seconds=t)
    now = datetime.utcnow()
    lowerBound = now - timeBuffer
    upperBound = now + timeBuffer
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    fileNames = []
    queries = c.execute("SELECT id,content FROM content_blocks WHERE date_created between '%s' and '%s'" % (lowerBound, upperBound)) # list of queries between lower and upper bounds
    for query in queries:
        id = query[0]
        message = query[1].decode("utf-8")
        fName = str(id) + ".json"
        with open(fName, 'w') as outfile:
            json.dump(message, outfile)
            fileNames.append(fName)
    conn.close()
    return fileNames

def uploadFile(queries):
    ACCESS_KEY_ID = ''
    ACCESS_SECRET_KEY = ''
    BUCKET_NAME = 'stixobjectbucket'
    for f in queries:
        data = open(f, 'rb')
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        s3.Bucket(BUCKET_NAME).put_object(Key=f, Body=data)
