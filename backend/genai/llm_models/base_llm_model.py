import os 
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class BaseLLMModel:
    local_models_dir='./saved_models/'

    def get_model(self):
        raise NotImplementedError("Error: Model not defined")

    def get_tokenizer(self):
        raise NotImplementedError("Error: Tokenizer not defined")
    
    def save_to_local(self,model_name,model,tokenizer):
        if self.local_models_dir:
            path: str = f'{self.local_models_dir}{model_name}'\
            
            os.makedirs(path, exist_ok=True)
            if model:
                model.save_pretrained(path)
            if tokenizer:
                tokenizer.save_pretrained(path)

    def load_from_local(self,model_name):
        
        model, tokenizer = None, None
        if self.local_models_dir:
            path: str = f'{self.local_models_dir}{model_name}'
           
            if os.path.exists(path) and os.path.isdir(path):
                try:
                    tokenizer=AutoTokenizer.from_pretrained(path)
                    model=AutoModelForCausalLM.from_pretrained(path,torch_dtype=torch.float16,device_map="auto",low_cpu_mem_usage=True)    
                except Exception as e:
                    model, tokenizer = None, None
            return model,tokenizer