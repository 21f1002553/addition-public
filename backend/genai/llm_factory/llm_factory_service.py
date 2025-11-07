from ..llm_models.llm_model_implementation import gemini_model,BaseLLMModel,chatgpt_model

class LLMModelFactory:

    _supported_model_providers = {
        "gemini": gemini_model,
        'chatgpt':chatgpt_model
    }

    @staticmethod
    def get_model_provider(model_provider_name: str):
        model=model.lower()

        if model_provider_name in LLMModelFactory._supported_model_providers:
            return LLMModelFactory._supported_model_providers[model_provider_name]
        else:
            raise ValueError(f"Unsupported model provider: {model_provider_name}")