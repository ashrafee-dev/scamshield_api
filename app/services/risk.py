
from pydantic import ValidationError

from models.response import riskAssessment
from services.ai import ask_deepseek


def get_assessment(transcription: str) -> riskAssessment | None:
    for _ in range(5):
        response = ask_deepseek(transcription)
        if response is None:
            continue
        assessment = None
        try:
            assessment = riskAssessment(**response)

        except ValidationError as e:
            print(e.errors())

        return assessment
