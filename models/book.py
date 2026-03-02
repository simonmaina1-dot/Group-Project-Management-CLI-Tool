"""
Book model for the Library Management System.

This module implements the Book class with full OOP principles including:
- Encapsulation using @property and @setter
- Class methods for object creation/retrieval
- Proper __str__ and __repr__ methods
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict


class Book:
    """
    Represents a book in the library system.
    
    Attributes:
        title: Book title
        author: Book author
        isbn: Unique ISBN (10 or 13 digits)
        total_copies: Total number of copies available
        available_copies: Number of copies currently available
        borrowed_copies: Number of copies currently borrowed
        borrowed_by: List of users who have borrowed copies
        due_date: Return due date for borrowed books
        is_available: Whether the book is available for borrowing
        is_borrowed: Whether any copy is currently borrowed
        is_overdue: Whether any borrowed copy is overdue
        is_reserved: Whether the book is reserved
        is_renewed: Whether any borrow has been renewed
        is_lost: Whether any copy is lost
        is_damaged: Whether any copy is damaged
    """
    
    # Class-level attributes
    _book_id_counter: int = 0
    _all_books: List[Dict] = []
    
    # Book status constants
    STATUS_AVAILABLE = "available"
    STATUS_BORROWED = "borrowed"
    STATUS_RESERVED = "reserved"
    STATUS_OVERDUE = "overdue"
    STATUS_LOST = "lost"
    STATUS_DAMAGED = "damaged"
    
    def __init__(self, title: str, author: str, isbn: str, total_copies: int):
        """
        Initialize a new book.
        
        Args:
            title: Book title
            author: Book author name
            isbn: Unique ISBN (10 or 13 digits)
            total_copies: Total number of copies
        """
        # Validate inputs
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        if not author or not author.strip():
            raise ValueError("Author cannot be empty.")
        
        # Private attributes (encapsulation)
        self._title = title.strip()
        self._author = author.strip()
        self._isbn = isbn
        self._total_copies = total_copies
        self._available_copies = total_copies
        self._borrowed_copies = 0
        self._borrowed_by: List[Dict] = []
        self._due_date: Optional[datetime] = None
        self._is_available = True
        self._is_borrowed = False
        self._is_overdue = False
        self._is_reserved = False
        self._is_renewed = False
        self._is_lost = False
        self._is_damaged = False
        
        # Increment class-level book ID counter
        Book._book_id_counter += 1
        self._book_id = Book._book_id_counter
        self._created_at = datetime.now()
    
    # ==================== Properties ====================
    
    @property
    def book_id(self) -> int:
        """Get the unique book ID."""
        return self._book_id
    
    @property
    def title(self) -> str:
        """Get the book title."""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Set book title with validation."""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty.")
        self._title = value.strip()
    
    @property
    def author(self) -> str:
        """Get the book author."""
        return self._author
    
    @author.setter
    def author(self, value: str):
        """Set book author with validation."""
        if not value or not value.strip():
            raise ValueError("Author cannot be empty.")
        self._author = value.strip()
    
    @property
    def isbn(self) -> str:
        """Get the book ISBN."""
        return self._isbn
    
    @isbn.setter
    def isbn(self, value: str):
        """Set book ISBN with validation."""
        isbn_clean = value.replace('-', '').replace(' ', '')
        if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
            raise ValueError("ISBN must be 10 or 13 digits.")
        if not isbn_clean.isdigit():
            raise ValueError("ISBN must contain only digits.")
        self._isbn = value
    
    @property
    def total_copies(self) -> int:
        """Get total number of copies."""
        return self._total_copies
    
    @total_copies.setter
    def total_copies(self, value: int):
        """Set total copies with validation."""
        if value < 0:
            raise ValueError("Total copies cannot be negative.")
        self._total_copies = value
        # Adjust available copies if needed
        if self._available_copies > value:
            self._available_copies = value
    
    @property
    def available_copies(self) -> int:
        """Get number of available copies."""
        return self._available_copies
    
    @property
    def borrowed_copies(self) -> int:
        """Get number of borrowed copies."""
        return self._borrowed_copies
    
    @property
    def is_available(self) -> bool:
        """Check if book is available for borrowing."""
        return self._is_available and self._available_copies > 0
    
    @property
    def is_borrowed(self) -> bool:
        """Check if any copy is currently borrowed."""
        return self._is_borrowed
    
    @property
    def is_overdue(self) -> bool:
        """Check if any borrowed copy is overdue."""
        if not self._is_borrowed or not self._due_date:
            return False
        return datetime.now() > self._due_date
    
    @property
    def is_reserved(self) -> bool:
        """Check if book is reserved."""
        return self._is_reserved
    
    @property
    def status(self) -> str:
        """Get current status of the book."""
        if self._is_lost:
            return self.STATUS_LOST
        if self._is_damaged:
            return self.STATUS_DAMAGED
        if self._is_overdue:
            return self.STATUS_OVERDUE
        if self._is_reserved:
            return self.STATUS_RESERVED
        if self._is_borrowed:
            return self.STATUS_BORROWED
        return self.STATUS_AVAILABLE
    
    @property
    def due_date(self) -> Optional[datetime]:
        """Get the due date for returns."""
        return self._due_date
    
    @property
    def borrowed_by(self) -> List[Dict]:
        """Get list of borrowers (copy for encapsulation)."""
        return self._borrowed_by.copy()
    
    @property
    def created_at(self) -> datetime:
        """Get book creation timestamp."""
        return self._created_at
    
    # ==================== Class Methods ====================
    
    @classmethod
    def create_book(cls, title: str, author: str, isbn: str, copies: int) -> 'Book':
        """
        Factory method to create a new book.
        
        Args:
            title: Book title
            author: Book author
            isbn: ISBN
            copies: Number of copies
            
        Returns:
            New Book instance
        """
        return cls(title, author, isbn, copies)
    
    @classmethod
    def get_all_books(cls) -> List[Dict]:
        """Get all books (class-level storage)."""
        return cls._all_books.copy()
    
    @classmethod
    def validate_isbn(cls, isbn: str) -> tuple:
        """
        Validate ISBN format.
        
        Args:
            isbn: ISBN to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isbn:
            return False, "ISBN cannot be empty."
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
            return False, "ISBN must be 10 or 13 digits."
        if not isbn_clean.isdigit():
            return False, "ISBN must contain only digits."
        return True, ""
    
    # ==================== Instance Methods ====================
    
    def borrow(self, user: str) -> bool:
        """
        Borrow a book from the library.
        
        Args:
            user: Username of the borrower
            
        Returns:
            True if successful, False otherwise
        """
        if self.is_available and self._available_copies > 0:
            self._is_available = False
            self._is_borrowed = True
            self._available_copies -= 1
            self._borrowed_copies += 1
            self._due_date = datetime.now() + timedelta(days=14)
            self._borrowed_by.append({
                'user': user,
                'borrow_date': datetime.now(),
                'due_date': self._due_date
            })
            return True
        return False
    
    def return_book(self, user: str) -> bool:
        """
        Return a borrowed book.
        
        Args:
            user: Username of the borrower
            
        Returns:
            True if successful, False otherwise
        """
        for record in self._borrowed_by:
            if record['user'] == user:
                self._borrowed_by.remove(record)
                self._available_copies += 1
                self._borrowed_copies -= 1
                
                if self._borrowed_copies == 0:
                    self._is_borrowed = False
                    self._is_available = True
                    self._due_date = None
                return True
        return False
    
    def extend_due_date(self, days: int = 7) -> bool:
        """
        Extend the due date for borrowed books.
        
        Args:
            days: Number of days to extend
            
        Returns:
            True if successful
        """
        if self._due_date:
            self._due_date = self._due_date + timedelta(days=days)
            self._is_renewed = True
            return True
        return False
    
    def reserve(self) -> bool:
        """Reserve the book."""
        if not self._is_reserved and self._is_available:
            self._is_reserved = True
            return True
        return False
    
    def cancel_reservation(self) -> bool:
        """Cancel book reservation."""
        if self._is_reserved:
            self._is_reserved = False
            return True
        return False
    
    def mark_lost(self) -> bool:
        """Mark a copy as lost."""
        if self._available_copies > 0:
            self._available_copies -= 1
            self._is_lost = True
            return True
        return False
    
    def mark_damaged(self) -> bool:
        """Mark a copy as damaged."""
        if self._available_copies > 0:
            self._available_copies -= 1
            self._is_damaged = True
            return True
        return False
    
    def add_copies(self, count: int) -> bool:
        """
        Add more copies of the book.
        
        Args:
            count: Number of copies to add
            
        Returns:
            True if successful
        """
        if count > 0:
            self._total_copies += count
            self._available_copies += count
            return True
        return False
    
    def remove_copies(self, count: int) -> bool:
        """
        Remove copies of the book.
        
        Args:
            count: Number of copies to remove
            
        Returns:
            True if successful
        """
        if count > 0 and self._total_copies >= count:
            new_available = self._available_copies - count
            if new_available >= 0 and self._borrowed_copies <= (self._total_copies - count):
                self._total_copies -= count
                self._available_copies = max(0, new_available)
                return True
        return False
    
    def to_dict(self) -> Dict:
        """
        Convert book object to dictionary for JSON storage.
        
        Returns:
            Dictionary representation of the book
        """
        return {
            'book_id': self._book_id,
            'title': self._title,
            'author': self._author,
            'isbn': self._isbn,
            'total_copies': self._total_copies,
            'available_copies': self._available_copies,
            'borrowed_copies': self._borrowed_copies,
            'borrowed_by': [
                {
                    'user': b['user'],
                    'borrow_date': b['borrow_date'].isoformat() if b.get('borrow_date') else None,
                    'due_date': b['due_date'].isoformat() if b.get('due_date') else None
                }
                for b in self._borrowed_by
            ],
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'is_available': self._is_available,
            'is_borrowed': self._is_borrowed,
            'is_overdue': self._is_overdue,
            'is_reserved': self._is_reserved,
            'is_renewed': self._is_renewed,
            'is_lost': self._is_lost,
            'is_damaged': self._is_damaged,
            'created_at': self._created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        """
        Create a Book instance from a dictionary.
        
        Args:
            data: Dictionary with book data
            
        Returns:
            Book instance
        """
        book = cls(
            title=data.get('title', ''),
            author=data.get('author', ''),
            isbn=data.get('isbn', ''),
            total_copies=data.get('total_copies', 1)
        )
        
        # Restore additional attributes
        book._book_id = data.get('book_id', Book._book_id_counter)
        book._available_copies = data.get('available_copies', book._total_copies)
        book._borrowed_copies = data.get('borrowed_copies', 0)
        book._is_available = data.get('is_available', True)
        book._is_borrowed = data.get('is_borrowed', False)
        book._is_overdue = data.get('is_overdue', False)
        book._is_reserved = data.get('is_reserved', False)
        book._is_renewed = data.get('is_renewed', False)
        book._is_lost = data.get('is_lost', False)
        book._is_damaged = data.get('is_damaged', False)
        
        # Restore borrowed_by
        borrowed_by = data.get('borrowed_by', [])
        book._borrowed_by = []
        for b in borrowed_by:
            record = {'user': b.get('user', '')}
            if b.get('borrow_date'):
                record['borrow_date'] = datetime.fromisoformat(b['borrow_date'])
            if b.get('due_date'):
                record['due_date'] = datetime.fromisoformat(b['due_date'])
            book._borrowed_by.append(record)
        
        # Restore due_date
        if data.get('due_date'):
            book._due_date = datetime.fromisoformat(data['due_date'])
        
        # Restore created_at
        if data.get('created_at'):
            book._created_at = datetime.fromisoformat(data['created_at'])
        
        return book
    
    # ==================== Magic Methods ====================
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"Book(title='{self._title}', author='{self._author}', isbn='{self._isbn}')"
    
    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (f"Book(title='{self._title}', author='{self._author}', "
                f"isbn='{self._isbn}', available={self._available_copies}/{self._total_copies})")
    
    def __eq__(self, other) -> bool:
        """Check equality based on ISBN."""
        if not isinstance(other, Book):
            return False
        return self._isbn == other._isbn
    
    def __hash__(self) -> int:
        """Return hash based on ISBN."""
        return hash(self._isbn)

