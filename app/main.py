from fastapi import FastAPI, UploadFile
import os
from api import analyze
from services.transcription import audio_transcript
from services.risk import get_assesment
from models.request import information



app = FastAPI()
app.include_router(analyze.router)

