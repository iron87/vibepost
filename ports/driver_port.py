from abc import ABC, abstractmethod

from models.post import Post

class PostCreationPort(ABC):
    """Driver Port Interface for port creation."""

    @abstractmethod
    def create_post(self, business_id: int, user_input: str, image_url: str = None) -> Post: 
        pass
