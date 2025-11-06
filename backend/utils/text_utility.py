from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader 
from langchain_community.document_loaders import PyPDFLoader
import re
import json

class TextUtility:

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        loader = PyPDFLoader(pdf_path)
        text = loader.load()
        for i in range(len(text)):
            content += text[i].page_content
        return content
    
    @staticmethod
    def extract_text_from_docx(file_path):
        docx_loader=Docx2txtLoader(file_path)
        docs=docx_loader.load()
        return docs
    
    @staticmethod
    def remove_pii(text: str):
        s = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+','[EMAIL]', s)
        s = re.sub(r'\+?\d[\d\s\()]{7,}\d', '[PHONE]', s)
        s = re.sub(r'https?://\S+|www\.\S+', '[URL]', s)
        return s.strip()
    
    @staticmethod
    def remove_json_marker(text: str):
        cleaned_json=text.strip('`json \n')
        return json.loads(cleaned_json)


    @staticmethod
    def format_resume_text(resume: Dict[str, Any]) -> str:
        lines = []

        lines.append(f"Location: {resume.get('location', '')}")
        lines.append(f"Total Experience: {resume.get('total_experience', '')}")
        lines.append("Skills: " + ", ".join(resume.get("skills", [])))

        lines.append("\nWork Experience:")
        for exp in resume.get("work_experience", []):
            lines.append(f"- {exp['title']} at {exp['company']} ({exp['start_date']} to {exp['end_date']}): {exp['description']}")

        lines.append("\nEducation:")
        for edu in resume.get("education", []):
            lines.append(f"- {edu['degree']} in {edu['field_of_study']} from {edu['institute']} ({edu['start_date']}–{edu['end_date']})")

        lines.append("\nCertifications:")
        for cert in resume.get("certifications", []):
            lines.append(f"- {cert}")

        lines.append("\nProjects:")
        for proj in resume.get("projects", []):
            lines.append(f"- {proj['title']}: {proj['description']}")

        return "\n".join(lines)