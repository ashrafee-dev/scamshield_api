import json
from typing import Any
from app.services.filter import filter_sensitive
from app.config import client


def ask_deepseek(prompt: str) -> dict[str, Any] | None:
    prompt = filter_sensitive(prompt)
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": f"""Analyze the following message. Sensitive information has been filtered.

                Message:
                {prompt}

                Return ONLY a JSON object in exactly this format:

                {{
                "label": "Scam",
                "score": "High",
                "certainty": 95,
                "reason": "Brief explanation."
                }}

                Rules:
                - label must be one of: "Scam", "Scam Likely", or "Safe"
                - score must be one of: "High", "Medium", or "Low"
                - certainty must be an integer between 0 and 100
                - reason must be a string
                - Do not include any additional fields.
                """
            }
        ],
        response_format={"type": "json_object"},
        # stream=True
        # reasoning_effort="high",
        # extra_body={"thinking": {"type": "disabled"}}
    )
    if response.choices[0].message.content is None:
        return

    response = json.loads(response.choices[0].message.content)
    return response
