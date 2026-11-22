from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(150), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "description": self.description
        }