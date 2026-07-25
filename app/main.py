from fastapi import FastAPI
from app.api import analyze

    # if item.sender in r.get("numbers"):
    #     return 
    #

app = FastAPI()
app.include_router(analyze.router)

