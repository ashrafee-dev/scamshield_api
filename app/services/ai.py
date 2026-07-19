import json
from typing import Any
from services.filter import filter_sensitive
from config import client


def ask_deepseek(promt) ->dict[str,Any] | None:
    promt =  filter_sensitive(promt)
    print(promt)
    response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": f"""Analyze the following (Sensitive informations were filtered.)  - {promt}

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

