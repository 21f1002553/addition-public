from dotenv import dotenv_values


_properties = dotenv_values('.env')

class Config:
    GEMINI_API_KEY=_properties['GEMINI_API_KEY']
    LANGCHAIN_API_KEY=_properties['LANGCHAIN_API_KEY']
    OPENAI_API_KEY=_properties['OPENAI_API_KEY']