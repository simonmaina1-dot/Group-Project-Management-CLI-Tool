"""
BorrowRecord model for the Library Management System.

This module implements the BorrowRecord class with full OOP principles.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict


class BorrowRecord:
    """
    Records a book borrowing activity in the library system.
    
    This class tracks:
    - Which user borrowed which book
    - When the book was borrowed
    - When it should be returned
    - Whether it's overdue
    - Any extensions or renewals
    """
    
    # Class-level counter
    _record_id_counter: int = 0
    
    # Status constants
    STATUS_ACTIVE = "active"
    STATUS_RETURNED = "returned"
    STATUS_OVERDUE = "overdue"
    STATUS_LOST = "lost"
    
    def __init__(self, book_title: str, user_name: str, isbn: str, 
                 borrow_date: Optional[datetime] = None, 
                 return_days: int = 14):
        """
        Initialize a new borrow record.
        
        Args:
            book_title: Title of the borrowed book
            user_name: Username of the borrower
            isbn: ISBN of the book
            borrow_date: When the book was borrowed (defaults to now)
            return_days: Number of days before return is due
        """
        self._book_title = book_title
        self._user_name = user_name
        self._isbn = isbn
        self._borrow_date = borrow_date or datetime.now()
        self._return_date = self._borrow_date + timedelta(days=return_days)
        self._actual_return_date: Optional[datetime] = None
        self._is_renewed = False
        self._renewal_count = 0
        self._status = self.STATUS_ACTIVE
        
        # Increment class-level record ID counter
        BorrowRecord._record_id_counter += 1
        self._record_id = BorrowRecord._record_id_counter
    
    # ==================== Properties ====================
    
    @property
    def record_id(self) -> int:
        """Get the unique record ID."""
        return self._record_id
    
    @property
    def book_title(self) -> str:
        """Get the book title."""
        return self._book_title
    
    @property
    def user_name(self) -> str:
        """Get the borrower username."""
        return self._user_name
    
    @property
    def isbn(self) -> str:
        """Get the book ISBN."""
        return self._isbn
    
    @property
    def borrow_date(self) -> datetime:
        """Get the borrow date."""
        return self._borrow_date
    
    @property
    def return_date(self) -> datetime:
        """Get the scheduled return date."""
        return self._return_date
    
    @property
    def actual_return_date(self) -> Optional[datetime]:
        """Get the actual return date (None if not returned)."""
        return self._actual_return_date
    
    @property
    def is_overdue(self) -> bool:
        """Check if the book is overdue."""
        if self._actual_return_date:
            return False  # Already returned
        return datetime.now() > self._return_date
    
    @property
    def is_renewed(self) -> bool:
        """Check if the borrow has been renewed."""
        return self._is_renewed
    
    @property
    def renewal_count(self) -> int:
        """Get the number of times this borrow was renewed."""
        return self._renewal_count
    
    @property
    def status(self) -> str:
        """Get the current status of the borrow record."""
        if self._actual_return_date:
            return self.STATUS_RETURNED
        if self.is_overdue:
            return self.STATUS_OVERDUE
        if self._is_renewed and self._return_date < datetime.now():
            return self.STATUS_OVERDUE
        return self.STATUS_ACTIVE
    
    @property
    def days_until_due(self) -> int:
        """Get number of days until due date (negative if overdue)."""
        delta = self._return_date - datetime.now()
        return delta.days
    
    # ==================== Instance Methods ====================
    
    def extend_return_date(self, days: int = 7) -> bool:
        """
        Extend the return date by a given number of days.
        
        Args:
            days: Number of days to extend
            
        Returns:
            True if successful
        """
        if self._actual_return_date:
            return False  # Can't extend after return
        
        self._return_date = self._return_date + timedelta(days=days)
        self._is_renewed = True
        self._renewal_count += 1
        return True
    
    def return_book(self) -> bool:
        """
        Mark the book as returned.
        
        Returns:
            True if successful
        """
        if not self._actual_return_date:
            self._actual_return_date = datetime.now()
            return True
        return False
    
    def calculate_late_fee(self, daily_rate: float = 0.50) -> float:
        """
        Calculate late fee if book is overdue.
        
        Args:
            daily_rate: Fee per day overdue
            
        Returns:
            Late fee amount (0 if not overdue)
        """
        if not self.is_overdue:
            return 0.0
        
        if self._actual_return_date:
            days_late = (self._actual_return_date - self._return_date).days
        else:
            days_late = (datetime.now() - self._return_date).days
        
        return max(0, days_late * daily_rate)
    
    def to_dict(self) -> Dict:
        """
        Convert borrow record to dictionary for JSON storage.
        
        Returns:
            Dictionary representation
        """
        return {
            'record_id': self._record_id,
            'book_title': self._book_title,
            'user_name': self._user_name,
            'isbn': self._isbn,
            'borrow_date': self._borrow_date.isoformat(),
            'return_date': self._return_date.isoformat(),
            'actual_return_date': self._actual_return_date.isoformat() if self._actual_return_date else None,
            'is_renewed': self._is_renewed,
            'renewal_count': self._renewal_count,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BorrowRecord':
        """
        Create a BorrowRecord from a dictionary.
        
        Args:
            data: Dictionary with record data
            
        Returns:
            BorrowRecord instance
        """
        record = cls(
            book_title=data.get('book_title', ''),
            user_name=data.get('user_name', ''),
            isbn=data.get('isbn', ''),
            borrow_date=datetime.fromisoformat(data['borrow_date']) if data.get('borrow_date') else None,
            return_days=14  # Default, will be overwritten
        )
        
        # Restore additional attributes
        record._record_id = data.get('record_id', BorrowRecord._record_id_counter)
        record._return_date = datetime.fromisoformat(data['return_date']) if data.get('return_date') else datetime.now()
        record._actual_return_date = datetime.fromisoformat(data['actual_return_date']) if data.get('actual_return_date') else None
        record._is_renewed = data.get('is_renewed', False)
        record._renewal_count = data.get('renewal_count', 0)
        
        return record
    
    # ==================== Magic Methods ====================
    
    def __str__(self) -> str:
        """Return string representation."""
        return (f"BorrowRecord(book='{self._book_title}', user='{self._user_name}', "
                f"due={self._return_date.date()})")
    
    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (f"BorrowRecord(record_id={self._record_id}, book_title='{self._book_title}', "
                f"user_name='{self._user_name}', isbn='{self._isbn}', "
                f"borrow_date={self._borrow_date.date()}, return_date={self._return_date.date()}, "
                f"status='{self.status}')")

