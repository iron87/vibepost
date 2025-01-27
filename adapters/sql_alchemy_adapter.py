from sqlalchemy.orm import Session
from models.post import Post
from models.business import Business
from ports.driven_port import DatabasePort

class SQLAlchemyDatabase(DatabasePort):
    """SQLAlchemy Database Adapter."""

    def __init__(self, db: Session):
        self.db = db

    def save_post(self, business_id: int, content: str, image_url: str = None):
        post = Post(business_id=business_id, content=content, image_url=image_url)
        self.db.add(post)
        self.db.commit()

    def get_business_info(self, business_id: int) -> dict:
        business = self.db.query(Business).filter(Business.id == business_id).first()
        return {
            "name": business.name,
            "specialties": business.specialties,
            "keywords": business.keywords
        } if business else None
