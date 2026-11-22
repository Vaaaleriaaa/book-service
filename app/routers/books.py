from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookPatch, BookResponse

router = APIRouter(
    prefix="/api/books",
    tags=["books"]
)

@router.get(
    "/", 
    response_model=List[BookResponse], 
    summary="Получить все книги",
    description="Возвращает список всех книг из базы данных. \
    Если книг нет, возвращает пустой массив."
)
def get_all_books(db: Session = Depends(get_db)):
    """
    Получить список всех книг.   
    - **Возвращает**: массив объектов Book
    - **Статус**: 200 OK
    """
    books = db.query(Book).all()
    return books

@router.get(
    "/{book_id}", 
    response_model=BookResponse,
    summary="Получить книгу по ID",
    description="Возвращает информацию о конкретной книге по её уникальному идентификатору."
)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
    Получить книгу по её ID.
    - **book_id**: уникальный идентификатор книги
    - **Возвращает**: объект Book
    - **Статус**: 200 OK
    - **Ошибки**: 404 Not Found - если книга не найдена
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга не найдена с ID: {book_id}"
        )
    
    return book

@router.post(
    "/", 
    response_model=BookResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую книгу",
    description="Создает новую запись о книге в базе данных. ID генерируется автоматически."
)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Создать новую книгу.
    - **Тело запроса**: объект BookCreate (title, author, year, description)
    - **Возвращает**: созданный объект Book с присвоенным ID
    - **Статус**: 201 Created
    - **Ошибки**: 400 Bad Request - если данные не прошли валидацию
    """
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        description=book_data.description
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book

@router.put(
    "/{book_id}", 
    response_model=BookResponse,
    summary="Полностью обновить книгу",
    description="Заменяет все поля книги новыми значениями. Все поля обязательны."
)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    """
    Полностью обновить книгу (PUT).
    - **book_id**: ID книги для обновления
    - **Тело запроса**: объект BookUpdate (все поля обязательны)
    - **Возвращает**: обновленный объект Book
    - **Статус**: 200 OK
    - **Ошибки**: 404 Not Found - если книга не найдена
    """
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга не найдена с ID: {book_id}"
        )
    
    existing_book.title = book_data.title
    existing_book.author = book_data.author
    existing_book.year = book_data.year
    existing_book.description = book_data.description
    
    db.commit()
    db.refresh(existing_book)
    
    return existing_book

@router.patch(
    "/{book_id}", 
    response_model=BookResponse,
    summary="Частично обновить книгу",
    description="Обновляет только указанные поля книги. Можно передать одно или несколько полей."
)
def patch_book(book_id: int, book_data: BookPatch, db: Session = Depends(get_db)):
    """
    Частично обновить книгу (PATCH).
    - **book_id**: ID книги для обновления
    - **Тело запроса**: объект BookPatch (все поля опциональны)
    - **Возвращает**: обновленный объект Book
    - **Статус**: 200 OK
    - **Ошибки**: 404 Not Found - если книга не найдена
    """
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга не найдена с ID: {book_id}"
        )
    
    update_data = book_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_book, field, value)
    
    db.commit()
    db.refresh(existing_book)
    
    return existing_book

@router.delete(
    "/{book_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить книгу",
    description="Удаляет книгу из базы данных по её ID."
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Удалить книгу.
    - **book_id**: ID книги для удаления
    - **Возвращает**: пустое тело ответа
    - **Статус**: 204 No Content
    - **Ошибки**: 404 Not Found - если книга не найдена
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга не найдена с ID: {book_id}"
        )
    
    db.delete(book)
    db.commit()
    
    return None

@router.get(
    "/search/author/{author}", 
    response_model=List[BookResponse],
    summary="Поиск книг по автору",
    description="Возвращает список всех книг указанного автора."
)
def search_books_by_author(author: str, db: Session = Depends(get_db)):
    """
    Поиск книг по автору.
    - **author**: имя автора для поиска (точное совпадение)
    - **Возвращает**: массив объектов Book
    - **Статус**: 200 OK
    """
    books = db.query(Book).filter(Book.author == author).all()
    return books