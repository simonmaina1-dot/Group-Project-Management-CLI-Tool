"""
Book Service for the Library Management System.

This module handles all book-related operations with role-based access control.
- Admin: Can add, delete, update books
- Librarian: Can view all books
- Student: Can view available books
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from utils.file_handler import load_data, save_data

# File paths
BOOK_FILE = "data/books.json"
BORROW_FILE = "data/borrow_records.json"


# ==================== Access Control Helpers ====================

def check_book_access(current_user: Optional[Dict], action: str) -> tuple:
    """
    Check if current user has permission to perform the action.
    
    Args:
        current_user: The logged in user dictionary or None
        action: The action being performed ('add', 'delete', 'update', 'view')
        
    Returns:
        Tuple of (has_access: bool, message: str)
    """
    if current_user is None:
        return False, "Please login to access books."
    
    role = current_user.get('role', '')
    
    if action in ['add', 'delete']:
        # Only admin can add or delete books
        if role != 'admin':
            return False, f"Access denied. Only admins can {action} books."
    
    # All logged in users can view books
    return True, ""


# ==================== Book Operations ====================

def add_book(title: str, author: str, isbn: str, copies: int, current_user: Optional[Dict] = None) -> Dict:
    """
    Add a book to the library system. Only admins can add books.
    
    Args:
        title: Book title
        author: Book author
        isbn: Book ISBN
        copies: Number of copies
        current_user: The logged in user (must be admin)
        
    Returns:
        Dictionary with success status and message
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'add')
    if not has_access:
        return {'success': False, 'message': msg}
    
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
        'borrowed_by': [],
        'added_by': current_user.get('username') if current_user else 'system',
        'added_at': datetime.now().isoformat()
    }
    
    # Add book to list
    books.append(book)
    
    # Save to file
    save_data(BOOK_FILE, books)
    
    return {'success': True, 'message': 'Book added successfully'}


def list_books(current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Return all books in the library system. All logged in users can view.
    
    Args:
        current_user: The logged in user or None
        
    Returns:
        List of book dictionaries
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'view')
    if not has_access:
        return []
    
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    return books


def list_available_books(current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Return only available books in the library system.
    
    Args:
        current_user: The logged in user or None
        
    Returns:
        List of available book dictionaries
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'view')
    if not has_access:
        return []
    
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    
    return [book for book in books if book.get('available_copies', 0) > 0]


def get_book_by_isbn(isbn: str, current_user: Optional[Dict] = None) -> Optional[Dict]:
    """
    Get a book by ISBN.
    
    Args:
        isbn: Book ISBN
        current_user: The logged in user or None
        
    Returns:
        Book dictionary if found, None otherwise
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'view')
    if not has_access:
        return None
    
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            return book
    
    return None


def delete_book(isbn: str, current_user: Optional[Dict] = None) -> Dict:
    """
    Delete a book from the library system. Only admins can delete.
    
    Args:
        isbn: Book ISBN to delete
        current_user: The logged in user (must be admin)
        
    Returns:
        Dictionary with success status and message
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'delete')
    if not has_access:
        return {'success': False, 'message': msg}
    
    books = load_data(BOOK_FILE)
    initial_count = len(books)
    
    # Remove book with matching ISBN
    books = [book for book in books if book.get('isbn') != isbn]
    
    if len(books) < initial_count:
        save_data(BOOK_FILE, books)
        return {'success': True, 'message': f'Book {isbn} deleted successfully'}
    
    return {'success': False, 'message': 'Book not found'}


def search_book(query: str, current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Search for books by title or author (case-insensitive partial match).
    
    Args:
        query: Search query
        current_user: The logged in user or None
        
    Returns:
        List of matching book dictionaries
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'view')
    if not has_access:
        return []
    
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    
    query_lower = query.lower()
    return [book for book in books 
            if query_lower in book.get('title', '').lower() 
            or query_lower in book.get('author', '').lower()]


def update_book(isbn: str, updates: Dict, current_user: Optional[Dict] = None) -> Dict:
    """
    Update book information. Only admins can update.
    
    Args:
        isbn: Book ISBN to update
        updates: Dictionary with fields to update
        current_user: The logged in user (must be admin)
        
    Returns:
        Dictionary with success status and message
    """
    # Check access
    has_access, msg = check_book_access(current_user, 'add')  # Same as add
    if not has_access:
        return {'success': False, 'message': msg}
    
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
            
            book['updated_at'] = datetime.now().isoformat()
            book['updated_by'] = current_user.get('username') if current_user else 'system'
            
            save_data(BOOK_FILE, books)
            return {'success': True, 'message': 'Book updated successfully'}
    
    return {'success': False, 'message': 'Book not found'}


# ==================== Borrow Operations ====================

def borrow_book(username: str, isbn: str, current_user: Optional[Dict] = None) -> Dict:
    """
    Borrow a book from the library system.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        current_user: The logged in user
        
    Returns:
        Dictionary with success status and message
    """
    # Check if user is logged in
    if current_user is None:
        return {'success': False, 'message': 'Please login to borrow books.'}
    
    # Students can only borrow for themselves
    role = current_user.get('role', '')
    if role == 'student':
        if username != current_user.get('username'):
            return {'success': False, 'message': 'Students can only borrow books for themselves.'}
    
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
                    'return_date': return_date.isoformat(),
                    'status': 'active'
                }
                records.append(record)
                save_data(BORROW_FILE, records)

                return {'success': True, 'message': 'Book borrowed successfully'}
            else:
                return {'success': False, 'message': 'Book not available'}
    
    return {'success': False, 'message': 'Book not found'}


def return_book(username: str, isbn: str, current_user: Optional[Dict] = None) -> Dict:
    """
    Return a borrowed book.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        current_user: The logged in user
        
    Returns:
        Dictionary with success status and message
    """
    # Check if user is logged in
    if current_user is None:
        return {'success': False, 'message': 'Please login to return books.'}
    
    # Students can only return their own books
    role = current_user.get('role', '')
    if role == 'student':
        if username != current_user.get('username'):
            return {'success': False, 'message': 'Students can only return their own books.'}
    
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


def get_borrowed_books(username: str, current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get all books borrowed by a user.
    
    Args:
        username: Username to get borrowed books for
        current_user: The logged in user
        
    Returns:
        List of borrowed book dictionaries
    """
    # Check if user is logged in
    if current_user is None:
        return []
    
    # Students can only view their own borrowed books
    role = current_user.get('role', '')
    if role == 'student':
        if username != current_user.get('username'):
            return []
    
    books = load_data(BOOK_FILE)
    borrowed = []
    
    for book in books:
        borrowed_by = book.get('borrowed_by', [])
        for record in borrowed_by:
            if record.get('user') == username:
                borrowed.append(book)
                break
    
    return borrowed


def get_overdue_books(current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get all overdue books. Admins and librarians can view all.
    
    Args:
        current_user: The logged in user
        
    Returns:
        List of overdue book dictionaries
    """
    # Check if user is logged in
    if current_user is None:
        return []
    
    role = current_user.get('role', '')
    if role not in ['admin', 'librarian']:
        return []
    
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

