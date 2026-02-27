"""User model for the library CLI."""
from typing import Optional, List
from datetime import datetime, timedelta
from .base_model import BaseModel


class User(BaseModel):
    """Represents a user in the library system."""

    def __init__(self, name: str, email: str, phone: str = "", address: str = ""):
        """Initialize a user instance.

        Args:
            name: Name of the user
            email: Email of the user
            phone: Phone number of the user (optional)
            address: Address of the user (optional)
        """
        super().__init__()
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.membership_date = datetime.now()
        self.membership_expiry = datetime.now() + timedelta(days=365)
        self.is_active = True
        self.borrowed_books: List[str] = []

    def to_dict(self) -> dict:
        """Convert user to dictionary.

        Returns:
            Dictionary representation of the user.
        """
        data = super().to_dict()
        data.update({
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'membership_date': self.membership_date.isoformat() if isinstance(self.membership_date, datetime) else self.membership_date,
            'membership_expiry': self.membership_expiry.isoformat() if isinstance(self.membership_expiry, datetime) else self.membership_expiry,
            'is_active': self.is_active,
            'borrowed_books': self.borrowed_books,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user instance from dictionary.

        Args:
            data: Dictionary containing user data.

        Returns:
            User instance.
        """
        # Create instance without calling __init__ to avoid required args
        instance = cls.__new__(cls)
        BaseModel.load_from_dict(instance, data)
        instance.name = data.get('name', '')
        instance.email = data.get('email', '')
        instance.phone = data.get('phone', '')
        instance.address = data.get('address', '')
        
        membership_date = data.get('membership_date')
        if membership_date:
            instance.membership_date = membership_date if isinstance(membership_date, datetime) else datetime.fromisoformat(membership_date)
        
        membership_expiry = data.get('membership_expiry')
        if membership_expiry:
            instance.membership_expiry = membership_expiry if isinstance(membership_expiry, datetime) else datetime.fromisoformat(membership_expiry)
        
        instance.is_active = data.get('is_active', True)
        instance.borrowed_books = data.get('borrowed_books', [])
        return instance

    def is_membership_valid(self) -> bool:
        """Check if the user's membership is valid.

        Returns:
            True if membership is valid, False otherwise.
        """
        return self.is_active and self.membership_expiry > datetime.now()

    def renew_membership(self, days: int = 365):
        """Renew the user's membership.

        Args:
            days: Number of days to extend membership.
        """
        self.membership_expiry = datetime.now() + timedelta(days=days)
        self.update()

    def borrow_book(self, book_id: str) -> bool:
        """Add a book to the user's borrowed list.

        Args:
            book_id: ID of the book being borrowed.

        Returns:
            True if successful, False if already borrowed.
        """
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
            self.update()
            return True
        return False

    def return_book(self, book_id: str) -> bool:
        """Remove a book from the user's borrowed list.

        Args:
            book_id: ID of the book being returned.

        Returns:
            True if successful, False if not in borrowed list.
        """
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            self.update()
            return True
        return False

    def __str__(self) -> str:
        """Return string representation of the user."""
        return f"{self.name} ({self.email})"

    def __repr__(self) -> str:
        """Return detailed string representation of the user."""
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', active={self.is_active})"

