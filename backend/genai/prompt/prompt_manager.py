


class PromptManager:

    @staticmethod
    def get_structure_json_resume(resume_text):
        prompt = f"""
        You are an expert HR data extraction assistant.
        You will be provided with a resume and a job description.
        Your task is to extract the relevant information from the resume that is most relevant to the job description.
        The output should be a JSON object with the following structure:
        {{
            "location": "",
            "skills": [],
            "total_experience": "",
            "work_experience": [
                {{
                    "title": "",
                    "company": "",
                    "position": "",
                    "start_date": "",
                    "end_date": "",
                    "description": ""        
                }}
            ],
            "education": [
                {{
                    "degree": "",
                    "institute": "",
                    "field_of_study": "",
                    "start_date": "",
                    "end_date": "",
                }}
            ],
            "certifications": [],
            "projects": [],
            "interests": [],
        }}
        Rules:
        - The output should be a valid JSON object.
        - Calculate total_experience from start_date to end_date in work_experience.
        - If any fields are missing, leave it as empty.
        - Do not include extra text or summary.
        - Do not include any other information.

        Resume text: 
        ---
        {resume_text}
        ---
    """
        return prompt
    

    @staticmethod
    def performance_review_prompt(self_review, manager_review):
        prompt = f"""
        You are an expert performance review summarizer assistant.
        You will be provided with an employee self-assessment and a manager review.
        Your task is to summarize the employee's performance based on the self-assessment and manager review.
        Respond only in valid JSON and nothing else.
        If you cannot answer, return the JSON with empty fields or null.
        Return a JSON object exactly matching the schema below:

        Schema: 
        {{
            "Strengths": "",
            "Weaknesses": "",
            "Improvements": "",
            "Actionable_step: "",
            "Comments": ""
        }}

        Inputs:
        - Employee Self Review type: {self_review}
        - Manager Review: {manager_review}

        Rules:
        = Provide a summary of the employee's performance based on the self-assessment and manager review.
        - Provide a concise summary of strengths, weaknesses, and areas for improvement each in less than 20 words.
        - Actionable Steps should be specific and prioritized (e.g. "Take X Courses").
        - Comments should be a single sentence summary.
        - Output only in valid JSON
        
    """
        return prompt
    

    @staticmethod
    def mock_interview_prompt(job_title,job_description,resume_text,n_easy_questions,n_medium_questions,n_hard_questions):
        prompt = f"""
        You are an expert AI assistant for interview tasks.
        Your Job is to provide tailored mock interviews for candidates based on the job description and title.
        Respond only in Valid JSON and nothing else.
        Generate a structured mock interview for the role. The output should be in JSON with keys: easy, medium and hard.
        Each key maps to a list of questions with the following structure:

        {{
            "question": "",
            "answer": "",
            "difficulty": ""
        }}

        Inputs:
        - Job Title: {job_title}
        - Job Description: {job_description}
        - Resume text: {resume_text}
        - Number of easy questions: {n_easy_questions}
        - Number of medium questions: {n_medium_questions}
        - Number of hard questions: {n_hard_questions}
        - Tone: Professional and Concise

        Rules:
        - Provide exactly the requested number of questions for each category.
        - Each question should be action-result formatted and containes keywords relevant to the job.
        - Keep each question and answer concise (questions <= 30 words).
        - Answer should be a 1-3 sentence summary.
        - Output only in valid JSON.
        
        """
        return prompt


    @staticmethod
    def course_recommendation_prompt(resume_text, job_description, job_title, courses):
        prompt = f"""
        You are an expert AI assistant for course recommendation tasks.
        Your Job is to provide course recommendations for candidates based on the job description and title from course list provided in input by taking into account the candidate's resume.
        Return a JSON Object of course recommendations with the following structure:
        {{
            "Course_id":"",
            "Course_title":"",
            "Course_description":"",
            "reason":""
        }}

        Inputs:
        - Resume text: {resume_text}
        - Job Description: {job_description}
        - Job Title: {job_title}
        - Courses: {courses}
        - Tone: Professional and Concise

        Rules:
        - Provide course recommendations based on the resume and job description.
        - Provide up to 3-4 course recommendations.
        - Each course recommendation should be action-result formatted and containes keywords relevant to the job.
        - Return only in valid JSON
        
        """
        return prompt
    

    @staticmethod
    def skill_gap_suggest_upskill_prompt(resume_text, job_description, job_title, courses):
        prompt = f"""
        You are an expert carrer coach.
        Your Job is to compare the candidate and target Job and suggest ways to upskill the candidate to match the job.
        Respond only in Valid Json and Structure should match with the Schema provided below.
        If you cannot answer, return the JSON with empty fields or null.

        Schema: 
        {{
            "missing_skill":[],
            "upskilling_path": [
                {{
                    "step": "",
                    "estimated_time": "",
                    "reason:""
                }}            
            ]
        }}
        
        Inputs:
        - Resume: {resume_text}
        - Job Title: {job_title}
        = Job Description: {job_description}
        - Courses: {courses}
        

        Rules:
        - missing_skills: list the key skills absent for the role.
        - upskilling_path: provide up to 3-4 steps to upskill, each with estimated hours and one line reason.
        - Output only in valid JSON.
        - Keep the entries concise.
        """
        return prompt


    @staticmethod
    def tailor_resume_prompt(resume_text, target_jobs):
        prompt = f"""
        You are an expert AI assistant for HR Tasks.
        Respond only in Valid JSON and nothing else.
        If you cannot answer, return the JSON with empty fields or null.

        Rewrite and optimize the candidate's resume bullets to better match the job description.
        The output should be a JSON object with the following structure:

        {{
            "rewritten_summary": "",
            "rewritten_bullets": [],
            "explained_changes": [] # short reasons for the changes
        }}

        Inputs:
        - Resume text: {resume_text}
        - Target Jobs: {target_jobs}
        - Tone: professional and concise

        Rules:
        - Provide a rewritten summary optimized for the target jobs.
        - Provide up to 5-6 rewritten_bullets; each bullet should be action-result formatted and containes keywords relevant to the target job.
        - explained_changes: provide up to 3-4 short explanation for the changes.
        - Output only in valid JSON.

        """
        return prompt