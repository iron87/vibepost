from ports.driven_port import  AIContentGeneratorPort, DatabasePort
from ports.driver_port import PostCreationPort

class PostService(PostCreationPort):
    """Core component for post creation."""

    def __init__(self, ai_generator: AIContentGeneratorPort, db: DatabasePort):
        self.ai_generator = ai_generator
        self.db = db

    def create_post(self, business_id: int, user_input: str, image_url: str = None):
        business_info = self.db.get_business_info(business_id)
        if not business_info:
            raise ValueError("Business not found")

        post_content = self.ai_generator.generate_post_text(business_info, user_input)
       # post_content = user_input
        self.db.save_post(business_id, post_content, image_url)

        return post_content
