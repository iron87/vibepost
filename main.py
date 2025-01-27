from adapters.sql_alchemy_adapter import SQLAlchemyDatabase
from database import get_db
from core.post_service import PostService

def main():
    db = next(get_db())  
    database_port = SQLAlchemyDatabase(db)
    post_service = PostService(db=database_port, ai_generator=None)

    post = post_service.create_post(1, "Welcome to our restaurant!", "https://example.com/image.jpg")
    print(post)

if __name__ == "__main__":
    main()
