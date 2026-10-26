from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Book Management API")


class Book(BaseModel):
    title: str
    author: str
    publication_year: int
    genre: str


books = {}
next_id = 1


@app.post("/books", status_code=201)
def create_book(book: Book):
    global next_id
    new_book = {"id": next_id, **book.model_dump()}
    books[next_id] = new_book
    next_id = next_id + 1
    return new_book


@app.get("/books")
def get_books(genre: Optional[str] = None):
    result = list(books.values())
    if genre:
        result = [book for book in result if book["genre"].lower() == genre.lower()]
    return result


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=404, 
            detail="Book not found"
        )
    return books[book_id]


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(
            status_code=404, 
            detail="Book not found")
    books[book_id] = {"id": book_id, **book.model_dump()}
    return books[book_id]


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=404, 
            detail="Book not found")
    del books[book_id]
    return {"message": "Book has been deleted"}