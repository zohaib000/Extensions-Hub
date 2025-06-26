from openai import OpenAI
import os
import json
from .models import *



def read_openai_key():
    chatgpt_field = ExtraField.objects.get(name="chatgpt_api_key")
    openai_key = chatgpt_field.data.first()
    print(openai_key)
    return openai_key

# custom gpt to detect the tweet type
def get_gpt_response(prompt,data_obj):
    MODEL = "gpt-4o-mini"
    client = OpenAI(api_key=read_openai_key())

    final_prompt=f"""
    {prompt}

    here is data object:
    {data_obj}
    """

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are expert in data processing & completion based on user prompt.",
            },
            {"role": "user", "content": final_prompt},
        ],
        # response_format={"type": "json_object"},
    )

    return completion.choices[0].message.content


