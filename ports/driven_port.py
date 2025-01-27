from abc import ABC, abstractmethod

class AIContentGeneratorPort(ABC):
    """AI Content Generator Port Interface."""
    
    @abstractmethod
    def generate_post_text(self, business_info: dict, user_input: str) -> str:
        pass


class DatabasePort(ABC):
    """Database Port Interface."""

    @abstractmethod
    def save_post(self, business_id: int, content: str, image_url: str = None):
        pass
    
    @abstractmethod
    def get_business_info(self, business_id: int) -> dict:
        pass
