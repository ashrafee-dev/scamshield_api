from fastapi import FastAPI
from api import analyze



app = FastAPI()
app.include_router(analyze.router)

