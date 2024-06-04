from pymongo import MongoClient
from time import sleep


conn = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019')
sleep(0.1)
print(conn.nodes)
