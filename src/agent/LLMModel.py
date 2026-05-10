import os
from openai import OpenAI
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

# 创建一个model
class LLMModel:
    def __init__(self):
        self.model = os.getenv("MODEL")
        api_key = os.getenv("DASHSCOPE_API_KEY")
        base_url = os.getenv("BASE_URL")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def think(self, messages:List[Dict[str, str]],tools:List[Dict[str, Any]], temperature:float = 0)->Any:
        print(type(tools))
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                temperature=temperature,
            )
            return response
        except Exception as e:
            print(f"Error occurred: {e}")
            raise
def test():
    from pydantic import BaseModel 