from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class riskAssesment():
    label : str 
    score : str
    percentage:int = 0

class information(BaseModel):
    data: bytes

app = FastAPI()

@app.post("/email")
def check_name(item: information):
    #pass the data to ai and ask ai to give data in riskAssesment formet and return
    return riskAssesment(label= "Very likely Scam", score="High")
@app.post("/audio")
async def audio_check(file:UploadFile):

    return {"filename" : file.size}
