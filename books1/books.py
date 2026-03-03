from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/titles/{book_title}")
async def read_book(book_title: str):
    for b in BOOKS:
        if b['title'].casefold() == book_title.casefold():
            return b
    return {}

@app.get("/books/")
async def read_category_by_query(category: str):
    return [b for b in BOOKS if b['category'].casefold() == category.casefold()]

@app.get("/books/authors/{author_name}/")
async def read_author_category_by_query(author_name:str, category: str):
    return [
        b for b in BOOKS if 
        b['category'].casefold() == category.casefold() and 
        b['author'].casefold() == author_name.casefold()
    ]

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i, b in enumerate(BOOKS):
        if b['title'].casefold() == updated_book['title'].casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i, b in enumerate(BOOKS):
        if b['title'].casefold() == book_title.casefold():
            BOOKS.pop(i)

@app.get("/authors")
async def get_author_books(author_name: str):
    return [b for b in BOOKS if b['author'].casefold() == author_name.casefold()]
        


