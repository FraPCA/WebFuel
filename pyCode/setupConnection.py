from pymongo import MongoClient
from time import sleep

conn = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019') #Imposta connessione col replica set
sleep(0.1) #Senza, indica erroneamente di non avere alcun nodo connesso
print(conn.nodes) #DEBUG
