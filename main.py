from adapters.sql_alchemy_adapter import SQLAlchemyDatabase
from adapters.llm_content_generator_adapter import LLMContentGeneratorAdapter
from database import get_db
from core.post_service import PostService
import settings

def main():
    db = next(get_db())
    llm_port =  LLMContentGeneratorAdapter(settings.settings.LLM_MODEL, settings.settings.LLM_PROVIDER, settings.settings.LLM_API_URL)  
    database_port = SQLAlchemyDatabase(db)
    post_service = PostService(db=database_port, ai_generator=llm_port)

    post = post_service.create_post(1, "Oggi abbiamo preparato dei nuovi primi: cacio e pepe e carbonara!", "https://example.com/image.jpg")
    print(post)

if __name__ == "__main__":
    main()
