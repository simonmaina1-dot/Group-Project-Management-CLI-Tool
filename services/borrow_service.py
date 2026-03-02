from datetime import datetime, timedelta
from utils.file_handler import load_data, save_data
from models.borrow_record import BorrowRecord

BOOK_FILE = "data/books.json"
BORROW_FILE = "data/borrow_records.json"


def borrow_book(username, isbn):
    """
    Allows a member to borrow a book.
    Automatically reduces available copies.
    """
    books = load_data(BOOK_FILE)
    
    # Handle case when file doesn't exist or is empty
    if not isinstance(books, list):
        books = []

    for book in books:
        if book.get("isbn") == isbn and book.get("available_copies", 0) > 0:
            # Get book title for the record
            book_title = book.get("title", "Unknown")
            
            # Reduce available copies
            book["available_copies"] -= 1
            save_data(BOOK_FILE, books)

            # Record borrowing
            borrow_date = datetime.now()
            return_date = borrow_date + timedelta(days=14)
            records = load_data(BORROW_FILE)
            
            if not isinstance(records, list):
                records = []
            
            record = BorrowRecord(book_title, username, borrow_date.isoformat(), return_date.isoformat(), isbn)
            records.append(record.to_dict())
            save_data(BORROW_FILE, records)

            return "Book borrowed successfully."

    return "Book not available."


def return_book(username, isbn):
    """
    Allows member to return book.
    Automatically increases available copies.
    """
    books = load_data(BOOK_FILE)
    
    # Handle case when file doesn't exist or is empty
    if not isinstance(books, list):
        books = []

    for book in books:
        if book.get("isbn") == isbn:
            book["available_copies"] = book.get("available_copies", 0) + 1
            save_data(BOOK_FILE, books)
            return "Book returned successfully."

    return "Book not found."

