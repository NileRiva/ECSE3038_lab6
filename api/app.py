from fastapi import FastAPI,HTTPException,Request
from bson import ObjectId
import motor.motor_asyncio
from fastapi.middleware.cors import CORSMiddleware
import pydantic
import os
from dotenv import load_dotenv
from datetime import datetime
import uvicorn
import json
import requests
import pytz

referencetemp=28.0

app = FastAPI()

#FastAPI (Uvicorn) runs on 8000 by Default


load_dotenv() #Nile Code, loads things from the coding environment
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_CONNECTION_STRING'))#Attempt at hiding URL - Nile
db = client.temperaturedb


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

origins = ["https://nilelab6.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#PUT 
@app.put("/api/temperature",status_code=204)
async def set_temp(request:Request):
    
    temperature = await request.json()
    elements = await db["temperatures"].find().to_list(1)

    if len(elements)==0:
         new_temp = await db["temperatures"].insert_one(temperature)
         patched_temp = await db["temperatures"].find_one({"_id": new_temp.inserted_id }) #updated_tank.upserted_id
         return patched_temp
    else:
        id=elements[0]["_id"]
        updated_temp= await db["temperatures"].update_one({"_id":id},{"$set": temperature})
        patched_temp = await db["temperatures"].find_one({"_id": id}) #updated_tank.upserted_id
        if updated_temp.modified_count>=1: 
            return patched_temp
    raise HTTPException(status_code=400,detail="Issue")

#GET /data
@app.get("/api/state")
async def getstate():
    currenttemp = await db["temperatures"].find().to_list(1)
    fanstate = (float(currenttemp[0]["temperature"])>referencetemp) #Watch Formatting here
    lightstate = (datetime.now(tz=pytz.timezone('America/New_York')).time()>sunset().time())
    Dictionary ={"fan":fanstate, "light":lightstate}
    return Dictionary

def sunset():
    sunsetresponse=requests.get(f'https://api.sunrise-sunset.org/json?lat=18.1096&lng=-77.2975&date=today')
    sunsetjson = sunsetresponse.json()
    sunsettimedate = sunsetjson["results"]["sunset"]
    sunsettimedate = datetime.strptime(sunsettimedate,'%I:%M:%S %p')
    return sunsettimedate



