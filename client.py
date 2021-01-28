from upload import *
import time

while True:
    t = 10
    queries = queryDB(t)
    if queries != []:
        uploadFile(queries)
    else:
        print("No queries in the last %s seconds" % (t))
    time.sleep(10)
