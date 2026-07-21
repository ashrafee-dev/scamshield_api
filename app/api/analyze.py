import io
from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect, Request
from services import rate_limit
from models.response import riskAssesment
from models.request import information
from services.risk import get_assesment
from services.transcription import audio_transcript

router = APIRouter()

@router.post("/email")
def email_check(item: information, request: Request)-> riskAssesment | dict | None:
    assert request.client is not None
    if not rate_limit.check_rate_limit(request.client.host):
        return {"error": "Reached you limit, wait 60 seconds before requesting again"}
    return get_assesment(item.body)

@router.post("/audio")
async def audio_check(file:UploadFile, request: Request)-> riskAssesment | dict | None:

    assert request.client is not None
    if not rate_limit.check_rate_limit(request.client.host):
        return {"error": "Reached you limit, wait 60 seconds before requesting again"}
    byte = await file.read()

    file_stream =  io.BytesIO(byte)
    transcript = audio_transcript(file_stream)
    return get_assesment(transcript)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket)-> riskAssesment | str | None:
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

            assert websocket.client is not None
            if not rate_limit.check_rate_limit(websocket.client.host):
                await websocket.send_json({"error": "Reached you limit, wait 60 seconds before requesting again"})
                continue

            file_stream =  io.BytesIO(byte)
            transcript = audio_transcript(file_stream)
            file_count += 1
            assesment =  get_assesment(transcript)
            if assesment is None: 
                await websocket.send_json({"error": "Assessment failed"})
            else:
                await websocket.send_json(assesment.model_dump())
    except WebSocketDisconnect:
        print("Client disconnected")

