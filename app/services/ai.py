from openai import OpenAI
import json
from config import client


def ask_deepseek(promt):
    response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": f"""Analyze the following- {promt}

                                        Return ONLY valid JSON in exactly this format:
    {{

                                        "label" "Scam" | "Scam Likely" | "Safe",
                                        "score": "High" | "Medium" | "Low",
                                        "certainty": integer
                                        "reason" : str
                                        }}

                                        Return ONLY a JSON object.
                                        Do NOT wrap the JSON in quotes.
                                        Do NOT escape quotation marks."""}
    ]
    #stream=True
    #reasoning_effort="high",
    #extra_body={"thinking": {"type": "disabled"}}
    ) 
    if response.choices[0].message.content is None:
        return

    response = json.loads(response.choices[0].message.content)
    return response

