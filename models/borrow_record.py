"""Borrow record model for the library CLI."""
from datetime import datetime, timedelta
from typing import Optional
from .base_model import BaseModel


class BorrowRecord(BaseModel):
    """Represents a borrow record in the library system."""

    STATUS_BORROWED = "borrowed"
    STATUS_RETURNED = "returned"
    STATUS_OVERDUE = "overdue"

    def __init__(self, user_id: str, book_id: str, due_days: int = 14):
        """Initialize a borrow record instance.

        Args:
            user_id: ID of the user borrowing the book
            book_id: ID of the book being borrowed
            due_days: Number of days before the book is due (default: 14)
        """
        super().__init__()
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = datetime.now()
        self.due_date = datetime.now() + timedelta(days=due_days)
        self.return_date: Optional[datetime] = None
        self.status = self.STATUS_BORROWED

    def to_dict(self) -> dict:
        """Convert borrow record to dictionary.

        Returns:
            Dictionary representation of the borrow record.
        """
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date.isoformat() if isinstance(self.borrow_date, datetime) else self.borrow_date,
            'due_date': self.due_date.isoformat() if isinstance(self.due_date, datetime) else self.due_date,
            'return_date': self.return_date.isoformat() if isinstance(self.return_date, datetime) else self.return_date,
            'status': self.status,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'BorrowRecord':
        """Create borrow record instance from dictionary.

        Args:
            data: Dictionary containing borrow record data.

        Returns:
            BorrowRecord instance.
        """
        # Create instance without calling __init__ to avoid required args
        instance = cls.__new__(cls)
        BaseModel.load_from_dict(instance, data)
        instance.user_id = data.get('user_id', '')
        instance.book_id = data.get('book_id', '')
        
        borrow_date = data.get('borrow_date')
        if borrow_date:
            instance.borrow_date = borrow_date if isinstance(borrow_date, datetime) else datetime.fromisoformat(borrow_date)
        
        due_date = data.get('due_date')
        if due_date:
            instance.due_date = due_date if isinstance(due_date, datetime) else datetime.fromisoformat(due_date)
        
        return_date = data.get('return_date')
        if return_date:
            instance.return_date = return_date if isinstance(return_date, datetime) else datetime.fromisoformat(return_date)
        
        instance.status = data.get('status', cls.STATUS_BORROWED)
        return instance

    def return_book(self):
        """Mark the book as returned."""
        self.return_date = datetime.now()
        self.status = self.STATUS_RETURNED
        self.update()

    def is_overdue(self) -> bool:
        """Check if the borrow record is overdue.

        Returns:
            True if overdue, False otherwise.
        """
        if self.status == self.STATUS_RETURNED:
            return False
        return datetime.now() > self.due_date

    def update_status(self):
        """Update the status based on return date and due date."""
        if self.return_date is not None:
            self.status = self.STATUS_RETURNED
        elif self.is_overdue():
            self.status = self.STATUS_OVERDUE
        else:
            self.status = self.STATUS_BORROWED

    def get_days_borrowed(self) -> int:
        """Get the number of days the book was borrowed.

        Returns:
            Number of days borrowed.
        """
        end_date = self.return_date if self.return_date else datetime.now()
        return (end_date - self.borrow_date).days

    def get_days_until_due(self) -> int:
        """Get the number of days until the book is due.

        Returns:
            Number of days until due (negative if overdue).
        """
        return (self.due_date - datetime.now()).days

    def __str__(self) -> str:
        """Return string representation of the borrow record."""
        return f"BorrowRecord(user={self.user_id}, book={self.book_id}, status={self.status})"

    def __repr__(self) -> str:
        """Return detailed string representation of the borrow record."""
        return f"BorrowRecord(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status='{self.status}')"

