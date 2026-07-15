from fastapi import FastAPI, UploadFile
from pydantic import BaseModel,ValidationError
from openai import OpenAI
from typing import Literal
import os
import json
from pydantic.networks import import_email_validator
from starlette.types import Message

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


class riskAssesment(BaseModel):
    label : Literal["Scam" , "Scam Likely" , "Safe"]
    score : Literal["High" , "Low" , "Medium"]
    certainty:int 
    reason: str

class information(BaseModel):
    sender : str
    body: str

app = FastAPI()

@app.post("/email")
def check_name(item: information):
    #check if item.sender in redis
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": f"""Analyze the following email.{item.body}

                                            Return ONLY valid JSON in exactly this format:
        {{
                                            "label": "Scam" | "Scam Likely" | "Safe",
                                            "score": "High" | "Medium" | "Low",
                                            "certainty": integer
                                            "reason" : str
                                            }}

                                            Return ONLY a JSON object.
                                            Do NOT wrap the JSON in quotes.
                                            Do NOT escape quotation marks."""}
        ]
        #stream=True
        #reasoning_effort="high",
        #extra_body={"thinking": {"type": "disabled"}}
    ) 
    for i in range(5):
        if response.choices[0].message.content is None:
                continue
        response = json.loads(response.choices[0].message.content)
        print(response)
        assesment = None
        try:
            assesment = riskAssesment(**response)
            print(assesment)
        except ValidationError as e:
            print(e.errors())

        return assesment

@app.post("/audio")
async def audio_check(file:UploadFile):
    byte = await file.read()
    response = "Nothing Yet"
    # will use ffmpeg and whisper
    # whisper will transcribe and filter out clients data, so AI doesnt get their data
    return {"response" : response}
