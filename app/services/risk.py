
from pydantic import ValidationError

from models.response import riskAssesment
from services.ai import ask_deepseek


def get_assesment(transcription: str) -> riskAssesment | None:
    for i in range(5):
        response = ask_deepseek(transcription)
        if response is None:
            continue
        assesment = None
        try:
            assesment = riskAssesment(**response)

        except ValidationError as e:
            print(e.errors())

        return assesment
