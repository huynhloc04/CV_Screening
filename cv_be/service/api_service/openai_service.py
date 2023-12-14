import openai
import env
from config import OPENAI_MODEL
import time
import json
from typing import Any

openai.api_key = env.OPENAI_API_KEY


class OpenAIService:
    @staticmethod
    def gpt_api(text: str = None, cv_name: str = None):
        model: str = OPENAI_MODEL
        temp: float = 0
        """request gpt api with a prompt"""
        start = time.time()

        response = openai.ChatCompletion.create(
            model = model,
            messages = [
                            {"role": "user", 
                             "content": text}
                    ],
            temperature=temp
            )
        
        elaps_time = time.time() - start
        print(f" >>> Request gpt api in {elaps_time}")
        return cv_name, json.loads(response.choices[0].message.content)
