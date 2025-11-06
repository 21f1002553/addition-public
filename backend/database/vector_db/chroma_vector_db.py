import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer


class ChromaVectorDBService:
    def __init__(self, persist_dir: str = './chroma-db' , model_name: str = 'all-MiniLM-L6-v2',):
        self.client = chromadb.PersistentClient(path="chroma_db")
        # self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer(model_name)

    ## Get Embeddings
    def get_embedding(self,text:str) -> List[float]:
        return self.model.encode(text).tolist()

    ## get_collections
    def get_collection(self,collection_name: str):
        return self.client.get_or_create_collection(name=collection_name)

    ## Load Data into vector store
    def load_data(self, doc_id, meta_data, collection_name: str, text: str):
        collection = self.get_collection(collection_name)
        embeddings = self.get_embedding(text)
        collection.add(documents=[text], embeddings=[embeddings], metadatas=[meta_data], ids=[doc_id])

        return {
            "id": doc_id,
            "text": text,
            "meta_data": meta_data,
            "embeddings": embeddings,
            "collection_name": collection_name,
            "status":"success"
        }

    ## clear collection
    def clear_collection(self,collection_name: str):
        collection = self.get_collection(collection_name)
        existing_ids=collection.get()["ids"]
        if existing_ids:
            collection.delete(ids=existing_ids)

    ## add resume
    def add_resume(self, resume_id: str, text: str, metadata):
        return self.load_data(collection_name="resume", doc_id=resume_id, meta_data=metadata, text=text)

    ## add JobPost
    def add_job_post(self, job_post_id: str, text: str, metadata):
        return self.load_data(collection_name="job_post", doc_id=job_post_id, meta_data=metadata, text=text)

    ## search jobs using resume embeddings
    def search_jobs_for_resume(self,resume_text: str, k=5):
        embeddings=self.get_embedding(resume_text)
        jobs = self.get_collection("job_post").query(
            query_embeddings=[embeddings],
            n_results=k
        )

        output=[]

        for doc, meta, dist, id_  in zip(jobs['documents'], jobs['metadatas'], jobs['distances'], jobs['ids']):
            output.append({
                "id": id_,
                "text": doc,
                "meta_data": meta,
                "distance": dist,
                "collection_name": "job_post",
            })
        return output

    ## search resumes for jobs
    def search_resumes_for_job(self,job_text: str, k=5):
        embeddings=self.get_embedding(job_text)
        resumes = self.get_collection("resume").query(
            query_embeddings=[embeddings],
            n_results=k
        )

        output=[]

        for doc,meta,dist, id_ in zip(resumes.get('documents'), resumes.get('metadatas'), resumes.get('distances'), resumes.get('ids')):

            output.append({
                "id": id_,
                "text": doc,
                "meta_data": meta,
                "distance": dist,
                "collection_name": "resume"
            })
        return output


    ### update the docs
    def update_docs(self,collection_name: str, doc_id: str, text: str, metadata):
        collection = self.get_collection(collection_name)
        collection.delete(ids=[doc_id])
        embeddings = self.get_embedding(text)
        collection.add(documents=[text], embeddings=[embeddings], metadatas=[metadata], ids=[doc_id])

        return {
            "id": doc_id,
            "text": text,
            "meta_data": metadata,
            "embeddings": embeddings,
            "collection_name": collection_name,
            "status":"success"
        }


chroma_db_service = ChromaVectorDBService()