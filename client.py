from upload import *
import time

while True:
    queries = queryDB(10)
    if queries != []:
        uploadFile(queries)
    time.sleep(10)
