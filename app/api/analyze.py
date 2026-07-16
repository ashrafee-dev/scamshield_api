import os

from fastapi import APIRouter, UploadFile

from models.request import information
from services.risk import get_assesment
from services.transcription import audio_transcript

router = APIRouter()

@router.post("/email")
def check_name(item: information):
    #check if item.sender in redis
    return get_assesment(item.body)

@router.post("/audio")
async def audio_check(file:UploadFile):
    byte = await file.read()
    filename = f"temp_audio/{file.filename}"
    with open(filename, "wb") as f:
        f.write(byte)
    transcript = audio_transcript(filename)
    os.remove(filename)
    #filter out sesitive info - later I'll use regex to do it properly
    transcript = "".join (char for char in transcript if char.isalpha() or char.isspace())
    return get_assesment(transcript)
    # will use ffmpeg and whisper
    # whisper will transcribe and filter out clients data, so AI doesnt get their data


