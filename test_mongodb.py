from pymongo import MongoClient
from pymongo.server_api import ServerApi
import sys
from networksecurity.exception.exception import NetworkSecurityException

uri = "mongodb+srv://tanviagarwal785_db_user:<@password>@cluster0.i0p4ggh.mongodb.net/?appName=Cluster0" #this uri is the connection string for the MongoDB Atlas cluster. It includes the username, password, and cluster information needed to connect to the database. 

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    raise NetworkSecurityException(e, sys)