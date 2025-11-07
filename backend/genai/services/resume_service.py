from ..prompt import PromptManager
from ...models import User, Role, Resume, JobPost, Application, PerformanceReview
from ..schema import Schema
from ...database.vector_db import chroma_db_service
from ..llm_factory import LLMModelFactory
from ...utils import TextUtility

class ResumeService:
    def __init__(self, file_path, user_id, resume_id):
        self.file_path = file_path
        self.user_id = user_id
        self.resume_id = resume_id
    
    def preprocess_resume(self,model_name:str):
        
        if self.file_path.endswith('.pdf'):
            parsed_resume = TextUtility.extract_text_from_pdf(self.file_path)
        elif self.file_path.endswith('.docx'):
            parsed_resume = TextUtility.extract_text_from_docx(self.file_path)
        
        # remove pii from resume
        parsed_resume = TextUtility.remove_pii(parsed_resume)

        #prompt gemini to structure resume into json format
        prompt=PromptManager.get_structure_json_resume(parsed_resume)

        if model_name is not None and model_name == "gemini":
            model=LLMModelFactory.get_model_provider('gemini').get_model()
            response=model.generate_content(prompt)
            result=response.text

        elif model_name is not None and model_name == "chatgpt":
            model=LLMModelFactory.get_model_provider('chatgpt').get_model()
            result=model.generate_content(prompt)

        # remove json marker from resume
        parsed_resume = TextUtility.remove_json_marker(result)

        #structure the resume 
        parsed_resume=TextUtility.format_resume_text(parsed_resume)

        # embed resume and store it in chroma
        chroma_db_service.load_data(
            collection_name="resume"+self.resume_id,
            doc_id=self.resume_id,
            meta_data={
                "user_id": self.user_id,
                "resume_id": self.resume_id
            },
            text=parsed_resume
        )

        # search top-n job based on resume
        jobs = chroma_db_service.search_jobs_for_resume(parsed_resume, k=5)
        


# store all the jobs in vector db

class JobService:

    def __init__(self, collection_name: str = 'Job_Post'):
        self.collection_name = collection_name
    
    
    


    


