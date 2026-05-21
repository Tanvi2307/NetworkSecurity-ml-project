import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where() #It returns the path of the certificate file.This .pem file contains trusted certificates.

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop = True, inplace = True)
            records = list(json.loads(data.T.to_json()).values()) #json.loads(...) Converts JSON string → Python dictionary.
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL) #Creating a MongoClient object to connect to the MongoDB server using the provided URL. MongoClient is a class from the pymongo library that allows you to interact with MongoDB databases.It is like Bridge between Python and MongoDB
            self.database = self.mongo_client[self.database] #Accessing the specified database from the MongoDB server using the MongoClient object.
            ''' 
            self.mongo_client[self.database] means:
            self.mongo_client["NetworkSecurity"]
            This tells MongoDB: "Open/select the NetworkSecurity database"
            Now it is an actual MongoDB database object.
            '''
            self.collection = self.database[self.collection] #converts: "phishingData" (string) into:Actual MongoDB collection object
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    try:
        FILE_PATH = "NetworkData\phisingData.csv"
        database = "NetworkSecurity"
        collection = "NetworkData"
        network_obj = NetworkDataExtract()
        records = network_obj.csv_to_json_converter(FILE_PATH)
        no_of_records = network_obj.insert_data_mongodb(records, database, collection)
        print(no_of_records)
    except Exception as e:
        raise NetworkSecurityException(e, sys)