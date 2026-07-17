import os
import filetype
from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect

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

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    Allowed = {
        "audio/mpeg",
        "audio/m4a",
        "audio/mp4",
        "audio/wav",
        "audio/x-wav",
        "audio/webm",
        "audio/ogg",
        "audio/flac",
    }
    file_count = 0
    try:
        while True:

            byte = await websocket.receive_bytes()
            kind = filetype.guess(byte) 
            if kind:
                print(kind.mime)
            if kind is None or kind.mime not in Allowed:
                raise ValueError("Not allowed type")
            filename = f"temp_audio/audio{file_count}.{kind.extension}"
            with open(filename, "wb") as f:
                f.write(byte)
            transcript = audio_transcript(filename)
            os.remove(filename)
            #filter out sesitive info - later I'll use regex to do it properly
            transcript = "".join (char for char in transcript if char.isalpha() or char.isspace())
            file_count += 1
            assesment =  get_assesment(transcript)
            if assesment is None: 
                await websocket.send_json({"error": "Assessment failed"})
            else:
                await websocket.send_json(assesment.model_dump())
    except WebSocketDisconnect:
        print("Client disconnected")

