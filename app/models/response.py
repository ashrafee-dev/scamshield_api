from pydantic import BaseModel
from typing import Literal

class riskAssessment(BaseModel):
    label : Literal["Scam" , "Scam Likely" , "Safe"]
    score : Literal["High" , "Low" , "Medium"]
    certainty:int 
    reason: str
