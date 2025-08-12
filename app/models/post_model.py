from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
