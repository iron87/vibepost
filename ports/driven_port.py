from abc import ABC, abstractmethod

from models.business import Business
from models.post import Post

class AIContentGeneratorPort(ABC):
    """AI Content Generator Port Interface."""
    
    @abstractmethod
    def generate_post_text(self, business_info: Business, user_input: str) -> str:
        pass


class DatabasePort(ABC):
    """Database Port Interface."""

    @abstractmethod
    def save_post(self, business_id: int, content: str, image_url: str = None) -> Post:
        pass
    
    @abstractmethod
    def get_business_info(self, business_id: int) -> Business:
        pass
        
    @abstractmethod
    def get_business_by_telegram_id(self, telegram_id: str) -> Business:
        pass

class NotificationSenderPort(ABC):
    """Post Preview Sender Port Interface."""
    
    @abstractmethod
    def send_post_preview(self, post_content: str, business_contact: str):
        pass