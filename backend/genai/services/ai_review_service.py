from ..prompt import PromptManager
from ..llm_factory import LLMModelFactory
from ...utils import TextUtility


class AIPerformanceReview:
    def __init__(self, model_name: str = 'gemini'):
        self.model_name = model_name

    def generate_performance_review(self, employee_review, manager_view):

        # load the prompt
        prompt=PromptManager.performance_review_prompt(employee_review, manager_view)

        # Load Model
        if self.model_name is not None and self.model_name == "gemini":
            model=LLMModelFactory.get_model_provider('gemini').get_model()
            response=model.generate_content(prompt)
            return response.text

        elif self.model_name is not None and self.model_name == "chatgpt":
            model=LLMModelFactory.get_model_provider('chatgpt').get_model()
            response=model.generate_content(prompt)
            return response
        
        else:
            raise ValueError(f"Unsupported model provider: {self.model_name}")