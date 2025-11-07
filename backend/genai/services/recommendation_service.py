from ..prompt import PromptManager
from ..llm_factory import LLMModelFactory
from ...utils import TextUtility


class RecommendationService:
    def __init__(self, resume_text, job_description, job_title, courses, model_name=None):
        self.resume_text = resume_text
        self.job_description = job_description
        self.job_title = job_title
        self.courses = courses
        self.model_name = model_name

    


    