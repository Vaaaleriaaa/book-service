from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название книги")
    author: str = Field(..., min_length=1, max_length=150, description="Автор книги")
    year: int = Field(..., ge=0, description="Год издания")
    description: Optional[str] = Field(None, max_length=1000, description="Описание книги")

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=150)
    year: Optional[int] = Field(None, ge=1800)
    description: Optional[str] = Field(None, max_length=1000)

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True 

class ErrorResponse(BaseModel):
    timestamp: datetime
    status: int
    error: str
    message: str
    path: str

class ValidationErrorResponse(BaseModel):
    timestamp: datetime
    status: int
    error: str
    message: str
    details: dict
    path: str