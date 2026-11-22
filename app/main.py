from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.database import engine, Base
from app.routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Service API",
    description="Микросервис для управления книгами",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]
        errors[field] = error["msg"]
    
    return JSONResponse(
        status_code=400,
        content={
            "timestamp": datetime.now().isoformat(),
            "status": 400,
            "error": "Bad Request",
            "message": "Ошибки валидации",
            "details": errors,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.now().isoformat(),
            "status": 500,
            "error": "Internal Server Error",
            "message": "Произошла внутренняя ошибка сервера",
            "path": str(request.url)
        }
    )

@app.get("/", tags=["info"])
def root():
    return {
        "message": "Book Service API работает!",
        "docs": "/docs"
    }