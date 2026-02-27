"""Borrow record model for the library CLI."""

# Import datetime and timedelta for date handling
from datetime import datetime, timedelta
# Import Optional for type hints
from typing import Optional
# Import BaseModel from the models package
from .base_model import BaseModel


class BorrowRecord(BaseModel):
    """Represents a borrow record in the library system."""

    # Class constants for borrow record status
    STATUS_BORROWED = "borrowed"   # Book is currently borrowed
    STATUS_RETURNED = "returned"   # Book has been returned
    STATUS_OVERDUE = "overdue"     # Book is overdue (not returned in time)

    def __init__(self, user_id: str, book_id: str, due_days: int = 14):
        """Initialize a borrow record instance.

        Args:
            user_id: ID of the user borrowing the book
            book_id: ID of the book being borrowed
            due_days: Number of days before the book is due (default: 14)
        """
        # Call parent class constructor to initialize id, created_at, updated_at
        super().__init__()
        # Set user and book IDs
        self.user_id = user_id
        self.book_id = book_id
        # Set borrow date to current time
        self.borrow_date = datetime.now()
        # Calculate due date based on borrow date plus due days
        self.due_date = datetime.now() + timedelta(days=due_days)
        # Initialize return date as None (not yet returned)
        self.return_date: Optional[datetime] = None
        # Set initial status to borrowed
        self.status = self.STATUS_BORROWED

    def to_dict(self) -> dict:
        """Convert borrow record to dictionary.

        Returns:
            Dictionary representation of the borrow record.
        """
        # Get base model attributes from parent class
        data = super().to_dict()
        # Add borrow record-specific attributes to the dictionary
        data.update({
            'user_id': self.user_id,
            'book_id': self.book_id,
            # Convert datetime to ISO format string for JSON serialization
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
        # Load base model attributes from the data
        BaseModel.load_from_dict(instance, data)
        # Load user and book IDs
        instance.user_id = data.get('user_id', '')
        instance.book_id = data.get('book_id', '')
        
        # Load and parse borrow date if present
        borrow_date = data.get('borrow_date')
        if borrow_date:
            instance.borrow_date = borrow_date if isinstance(borrow_date, datetime) else datetime.fromisoformat(borrow_date)
        
        # Load and parse due date if present
        due_date = data.get('due_date')
        if due_date:
            instance.due_date = due_date if isinstance(due_date, datetime) else datetime.fromisoformat(due_date)
        
        # Load and parse return date if present
        return_date = data.get('return_date')
        if return_date:
            instance.return_date = return_date if isinstance(return_date, datetime) else datetime.fromisoformat(return_date)
        
        # Default to borrowed status if not specified
        instance.status = data.get('status', cls.STATUS_BORROWED)
        return instance

    def return_book(self):
        """Mark the book as returned."""
        # Set return date to current time
        self.return_date = datetime.now()
        # Update status to returned
        self.status = self.STATUS_RETURNED
        # Update the updated_at timestamp
        self.update()

    def is_overdue(self) -> bool:
        """Check if the borrow record is overdue.

        Returns:
            True if overdue, False otherwise.
        """
        # If already returned, cannot be overdue
        if self.status == self.STATUS_RETURNED:
            return False
        # Check if current time is past the due date
        return datetime.now() > self.due_date

    def update_status(self):
        """Update the status based on return date and due date."""
        # If return date is set, book has been returned
        if self.return_date is not None:
            self.status = self.STATUS_RETURNED
        # Check if book is overdue
        elif self.is_overdue():
            self.status = self.STATUS_OVERDUE
        # Otherwise, book is still borrowed
        else:
            self.status = self.STATUS_BORROWED

    def get_days_borrowed(self) -> int:
        """Get the number of days the book was borrowed.

        Returns:
            Number of days borrowed.
        """
        # Use return date if available, otherwise use current date
        end_date = self.return_date if self.return_date else datetime.now()
        # Calculate difference in days
        return (end_date - self.borrow_date).days

    def get_days_until_due(self) -> int:
        """Get the number of days until the book is due.

        Returns:
            Number of days until due (negative if overdue).
        """
        # Calculate difference between due date and current time
        return (self.due_date - datetime.now()).days

    def __str__(self) -> str:
        """Return string representation of the borrow record."""
        # Return human-readable format with key details
        return f"BorrowRecord(user={self.user_id}, book={self.book_id}, status={self.status})"

    def __repr__(self) -> str:
        """Return detailed string representation of the borrow record."""
        # Return developer-friendly format with all key attributes
        return f"BorrowRecord(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status='{self.status}')"

