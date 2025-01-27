from database import engine, Base
from models.post import Post
from models.business import Business

print("Tabelle SQLAlchemy:", Base.metadata.tables.keys())

Base.metadata.reflect(bind=engine)


# Ensure models are registered with Base
Base.metadata.create_all(bind=engine)
