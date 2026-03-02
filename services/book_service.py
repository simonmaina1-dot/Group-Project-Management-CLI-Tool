"""
Book Service for the Library Management System.

This module handles all book-related operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict
from datetime import datetime, timedelta
from utils.file_handler import load_data, save_data

# File path
BOOK_FILE = "data/books.json"
BORROW_FILE = "data/borrow_records.json"


def add_book(title: str, author: str, isbn: str, copies: int) -> Dict:
    """Add a book to the library system."""
    # Check if title is empty
    if not title or not title.strip():
        return {'success': False, 'message': 'Title cannot be empty'}
    
    # Check if author is empty
    if not author or not author.strip():
        return {'success': False, 'message': 'Author cannot be empty'}
    
    # Check if ISBN is valid (10 or 13 digits)
    isbn_clean = isbn.replace('-', '').replace(' ', '')
    if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
        return {'success': False, 'message': 'ISBN must be 10 or 13 digits'}
    if not isbn_clean.isdigit():
        return {'success': False, 'message': 'ISBN must contain only digits'}
    
    # Check if copies is valid
    if copies < 1:
        return {'success': False, 'message': 'Number of copies must be at least 1'}
    
    # Load existing books
    books = load_data(BOOK_FILE)
    
    # Check if ISBN already exists
    for book in books:
        if book.get('isbn') == isbn:
            return {'success': False, 'message': 'Book with this ISBN already exists'}
    
    # Create book dictionary
    book = {
        'title': title.strip(),
        'author': author.strip(),
        'isbn': isbn,
        'total_copies': copies,
        'available_copies': copies,
        'borrowed_copies': 0,
        'borrowed_by': []
    }
    
    # Add book to list
    books.append(book)
    
    # Save to file
    save_data(BOOK_FILE, books)
    
    return {'success': True, 'message': 'Book added successfully'}


def list_books() -> List[Dict]:
    """Return all books in the library system."""
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    return books


def get_book_by_isbn(isbn: str) -> Dict:
    """Get a book by ISBN."""
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            return book
    
    return None


def delete_book(isbn: str) -> Dict:
    """Delete a book from the library system."""
    books = load_data(BOOK_FILE)
    initial_count = len(books)
    
    # Remove book with matching ISBN
    books = [book for book in books if book.get('isbn') != isbn]
    
    if len(books) < initial_count:
        save_data(BOOK_FILE, books)
        return {'success': True, 'message': f'Book {isbn} deleted successfully'}
    
    return {'success': False, 'message': 'Book not found'}


def search_book(query: str) -> List[Dict]:
    """Search for books by title (case-insensitive partial match)."""
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    
    query_lower = query.lower()
    return [book for book in books if query_lower in book.get('title', '').lower()]


def update_book(isbn: str, updates: Dict) -> Dict:
    """Update book information."""
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            # Update allowed fields
            if 'title' in updates and updates['title']:
                book['title'] = updates['title']
            if 'author' in updates and updates['author']:
                book['author'] = updates['author']
            if 'total_copies' in updates:
                book['total_copies'] = updates['total_copies']
                # Adjust available_copies if needed
                if 'available_copies' not in updates:
                    borrowed = book.get('borrowed_copies', 0)
                    book['available_copies'] = max(0, updates['total_copies'] - borrowed)
            if 'available_copies' in updates:
                book['available_copies'] = updates['available_copies']
            
            save_data(BOOK_FILE, books)
            return {'success': True, 'message': 'Book updated successfully'}
    
    return {'success': False, 'message': 'Book not found'}


def borrow_book(username: str, isbn: str) -> Dict:
    """
    Borrow a book from the library system.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        
    Returns:
        Dictionary with success status and message
    """
    books = load_data(BOOK_FILE)
    
    # Handle case when file doesn't exist or is empty
    if not isinstance(books, list):
        books = []

    for book in books:
        if book.get("isbn") == isbn:
            available = book.get("available_copies", 0)
            
            if available > 0:
                # Get book title for the record
                book_title = book.get("title", "Unknown")
                
                # Reduce available copies
                book["available_copies"] = available - 1
                book["borrowed_copies"] = book.get("borrowed_copies", 0) + 1
                
                # Add user to borrowed_by list
                if "borrowed_by" not in book:
                    book["borrowed_by"] = []
                
                borrow_record = {
                    "user": username,
                    "borrow_date": datetime.now().isoformat(),
                    "due_date": (datetime.now() + timedelta(days=14)).isoformat()
                }
                book["borrowed_by"].append(borrow_record)
                
                save_data(BOOK_FILE, books)

                # Record borrowing in borrow records file
                borrow_date = datetime.now()
                return_date = borrow_date + timedelta(days=14)
                records = load_data(BORROW_FILE)
                
                if not isinstance(records, list):
                    records = []
                
                record = {
                    'book_title': book_title,
                    'user_name': username,
                    'isbn': isbn,
                    'borrow_date': borrow_date.isoformat(),
                    'return_date': return_date.isoformat()
                }
                records.append(record)
                save_data(BORROW_FILE, records)

                return {'success': True, 'message': 'Book borrowed successfully'}
            else:
                return {'success': False, 'message': 'Book not available'}
    
    return {'success': False, 'message': 'Book not found'}


def return_book(username: str, isbn: str) -> Dict:
    """
    Return a borrowed book.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        
    Returns:
        Dictionary with success status and message
    """
    books = load_data(BOOK_FILE)
    
    # Handle case when file doesn't exist or is empty
    if not isinstance(books, list):
        books = []

    for book in books:
        if book.get("isbn") == isbn:
            borrowed_by = book.get("borrowed_by", [])
            
            # Find and remove user from borrowed_by
            found = False
            for record in borrowed_by:
                if record.get('user') == username:
                    borrowed_by.remove(record)
                    found = True
                    break
            
            if found:
                book['borrowed_by'] = borrowed_by
                book['available_copies'] = book.get('available_copies', 0) + 1
                book['borrowed_copies'] = max(0, book.get('borrowed_copies', 1) - 1)
                save_data(BOOK_FILE, books)
                return {'success': True, 'message': 'Book returned successfully'}
            else:
                return {'success': False, 'message': 'User did not borrow this book'}
    
    return {'success': False, 'message': 'Book not found'}


def get_borrowed_books(username: str) -> List[Dict]:
    """Get all books borrowed by a user."""
    books = load_data(BOOK_FILE)
    borrowed = []
    
    for book in books:
        borrowed_by = book.get('borrowed_by', [])
        for record in borrowed_by:
            if record.get('user') == username:
                borrowed.append(book)
                break
    
    return borrowed


def get_overdue_books() -> List[Dict]:
    """Get all overdue books."""
    books = load_data(BOOK_FILE)
    overdue = []
    now = datetime.now()
    
    for book in books:
        borrowed_by = book.get('borrowed_by', [])
        for record in borrowed_by:
            due_date_str = record.get('due_date')
            if due_date_str:
                due_date = datetime.fromisoformat(due_date_str)
                if now > due_date:
                    overdue.append(book)
                    break
    
    return overdue

