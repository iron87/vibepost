from sqlalchemy.orm import Session
from models.post import Post
from models.business import Business
from ports.driven_port import DatabasePort

class SQLAlchemyDatabase(DatabasePort):
    """SQLAlchemy Database Adapter."""

    def __init__(self, db: Session):
        self.db = db

    def save_post(self, business_id: int, content: str, image_url: str = None) -> Post:
        post = Post(business_id=business_id, content=content, image_url=image_url)
        self.db.add(post)
        self.db.commit()
        return post;

    def get_business_info(self, business_id: int) -> Business:
        business = self.db.query(Business).filter(Business.id == business_id).first()
        return business
    
    def get_business_by_telegram_id(self, telegram_id: str) -> Business:
        business = self.db.query(Business).filter(Business.telegramid == telegram_id).first()
        return business
