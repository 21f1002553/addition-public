from backend.genai.llm_models.base_llm_model import BaseLLMModel
from config import Config
import google.generativeai as genai
from openai import OpenAI

class GeminiModel(BaseLLMModel):
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def get_model(self):
        return self.model
    
    def get_tokenizer(self):
        return None


class ChatGPTModel(BaseLLMModel):

    def __init__(self):
        self.model_name = 'gpt-4o-mini'
        self.client=OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def get_model(self):
        return self.client
    
    def get_tokenizer(self):
        return None

    def generate_content(self, prompt, model_name=None, max_tokens=500):
        if model_name is None:
            model_name = self.model_name
        
        response=self.client.response.create(
            model=model_name,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0
        )
        return response.choices[0].message.content
    


gemini_model = GeminiModel()
chatgpt_model = ChatGPTModel()