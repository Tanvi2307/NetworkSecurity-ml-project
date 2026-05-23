import sys
import os
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
import certifi
ca = certifi.where()
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
''' 
mongo_db_url,      →  address of your Atlas cluster
tlsCAFile=ca       →  SSL certificate for security
tls       = Transport Layer Security (secure connection)
CA        = Certificate Authority
File      = the certificate file path

tells MongoDB:
"use these trusted certificates
 to verify the connection is secure" 
'''
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI() #Creates your web server,Like opening your restaurant → now ready to take orders → orders = prediction requests ✅
origins = ["*"] #WHO can talk to your API? "*" = everyone! → any website → any mobile app → any browser → all allowed ✅
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags = ["authentication"]) #When someone visits your website → what do you want to show them? → here we will show a simple message,
async def index():
    return RedirectResponse(url="/docs") #Redirects to API documentation page → where users can test your API endpoints

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful!!")
    except Exception as e:  
        raise NetworkSecurityException(e, sys)
''' 
When someone visits:
http://yourapi.com/train
        ↓
entire ML training pipeline runs!
        ↓
returns "Training is successful" ✅
'''
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    app_run(app, host = "localhost", port = 8000) #Starts the web server on localhost:8000 → now you can visit http://localhost:8000/train to trigger the training pipeline