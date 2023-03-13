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
referencetemp=28.0

app = FastAPI()

#FastAPI (Uvicorn) runs on 8000 by Default


load_dotenv() #Nile Code, loads things from the coding environment
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_CONNECTION_STRING"))#Attempt at hiding URL - Nile
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
    print("Testing...")
    temperature = await request.json()

    elements = await db["temperatures"].find().to_list(1)

    if len(elements)==0:
         print("Not Doing Else")#Troubleshooting
         new_temp = await db["temperatures"].insert_one(temperature)
         patched_temp = await db["temperatures"].find_one({"_id": new_temp.inserted_id }) #updated_tank.upserted_id
         return patched_temp
    else:
        id=elements[0]["_id"]
        print(id) #Troubleshooting
        updated_temp= await db["temperatures"].update_one({"_id":id},{"$set": temperature})
        patched_temp = await db["temperatures"].find_one({"_id": id}) #updated_tank.upserted_id
        if updated_temp.modified_count>=1: 
            return patched_temp
    raise HTTPException(status_code=400,detail="Issue")

#GET /data
@app.get("/api/state")
async def getstate():
    currenttemp = await db["temperatures"].find_one()
    fanstate = (float(currenttemp["temperature"])>referencetemp) #Watch Formatting here
    lightstate = (sunset()<datetime.now())
    Dictionary ={"fan":fanstate, "light":lightstate}
    jsonString = json.dumps(Dictionary)
    print(jsonString)#troubleshooting
    return Dictionary

def sunset():
    sunsetresponse=requests.get("https://ecse-sunset-api.onrender.com/api/sunset")
    sunsetjson = sunsetresponse.json()
    sunsettimedate = sunsetjson["sunset"]
    sunsettimedate = datetime.strptime(sunsettimedate,'%Y-%m-%dT%H:%M:%S.%f')
    return sunsettimedate

