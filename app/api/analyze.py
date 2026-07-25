import os
import filetype
from fastapi import APIRouter, HTTPException, WebSocketException, UploadFile, WebSocket, WebSocketDisconnect, Request
from app.services import rate_limit
from app.models.response import riskAssessment
from app.models.request import information
from app.services.risk import get_assessment
from app.services.transcription import audio_transcript

router = APIRouter()

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

@router.post("/email")
def email_check(item: information, request: Request)-> riskAssessment | dict | None:
    assert request.client is not None
    if not rate_limit.check_rate_limit(request.client.host):
        raise HTTPException (status_code= 429, detail= {"error":"Reached your limit, wait 60 seconds before requesting again"})
    return get_assessment(item.body)

@router.post("/audio")
async def audio_check(file:UploadFile, request: Request)-> riskAssessment | dict | None:


    assert request.client is not None
    if not rate_limit.check_rate_limit(request.client.host):
        raise HTTPException (status_code= 429, detail= {"error":"Reached your limit, wait 60 seconds before requesting again"})
    byte = await file.read()
    kind = filetype.guess(byte)

    if kind is None or kind.mime not in Allowed:
        raise HTTPException (status_code= 415, detail= {"error":"Content type not allowed"})
    tmp_dir = "/dev/shm/" if os.path.exists("/dev/shm") else ""
    filename = f"{tmp_dir}audio.{kind.extension}"
    with open(filename, "wb") as f:
        f.write(byte)
    transcript = audio_transcript(filename)
    os.remove(filename)
    return get_assessment(transcript)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket)-> riskAssessment | str | None:
    await websocket.accept()

    file_count = 0
    try:
        while True:

            byte = await websocket.receive_bytes()

            assert websocket.client is not None
            if not rate_limit.check_rate_limit(websocket.client.host):
                raise WebSocketException(code = 1008, reason="Reached your limit, wait 60 seconds before requesting again")
            kind = filetype.guess(byte) 

            if kind is None or kind.mime not in Allowed:
                await websocket.send_json({"error": "Content type not allowed"})
                continue
            tmp_dir = "/dev/shm/" if os.path.exists("/dev/shm") else ""
            filename = f"{tmp_dir}audio{file_count}.{kind.extension}"
            with open(filename, "wb") as f:
                f.write(byte)
            transcript = audio_transcript(filename)
            os.remove(filename)
            file_count += 1
            assessment =  get_assessment(transcript)
            if assessment is None: 
                await websocket.send_json({"error": "Failed to analyze the audio. Try again"})
            else:
                await websocket.send_json(assessment.model_dump())
    except WebSocketDisconnect:
        print("Client disconnected")

