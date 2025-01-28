from models.business import Business
from ports.driven_port import AIContentGeneratorPort
from llama_index.llms.ollama import Ollama



class LLMContentGeneratorAdapter(AIContentGeneratorPort):
    def __init__(self, model: str, llm_provider: str, llm_api_url: str):
        #TODO: implement using the factory pattern 
        if llm_provider == "ollama":
            self.llm = Ollama(base_url=llm_api_url, model=model)

    def generate_post_text(self, business_info: Business, user_input: str) -> str:
        #TODO: improve the prompt
        llm_input = f"You are a social media manager assistant. Please write a social post (in Italian) for the following business: {business_info.name} is a {business_info.category} business with this specialties {business_info.specialties}. It's located in {business_info.city}. Consider also this: {user_input}. Add some emoticons and tags to make the post more engaging. Write only the post in the response"
        response = self.llm.complete(llm_input);
        return response.text;
