from adapters.sql_alchemy_adapter import SQLAlchemyDatabase
from adapters.llm_content_generator_adapter import LLMContentGeneratorAdapter
from adapters.telegram_sender_adapter import TelegramSenderAdapter
from database import get_db
from core.post_service import PostService
import settings
from telegram_adapter import TelegramBotAdapter


def main():
    db = next(get_db())
    llm_port =  LLMContentGeneratorAdapter(settings.settings.LLM_MODEL, settings.settings.LLM_PROVIDER, settings.settings.LLM_API_URL)  
    database_port = SQLAlchemyDatabase(db)
    post_service = PostService(db=database_port, ai_generator=llm_port)
    #post = post_service.create_post(1, "Oggi abbiamo preparato dei nuovi primi: cacio e pepe e carbonara!", "https://example.com/image.jpg")
    #print(post)
    bot_adapter = TelegramBotAdapter(database_port,post_service)
    bot_adapter.run()
    
if __name__ == "__main__":
    main()
